import requests
from fastapi import HTTPException
from api.database import get_connection
from api.core.security import hash_chave_privada

TAXA_CONVERSAO = 0.005  # 0.5%


def _validar_carteira(endereco: str, chave_privada: str):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute("SELECT hash_chave_privada FROM CARTEIRA WHERE endereco_carteira = %s", (endereco,))
        carteira = cur.fetchone()

        if not carteira:
            raise HTTPException(404, "Carteira não encontrada")

        if carteira["hash_chave_privada"] != hash_chave_privada(chave_privada):
            raise HTTPException(403, "Chave privada inválida")

    finally:
        cur.close()
        conn.close()


def _buscar_id_moeda(codigo: str):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute("SELECT id_moeda FROM MOEDA WHERE codigo = %s", (codigo,))
        moeda = cur.fetchone()
        if not moeda:
            raise HTTPException(404, f"Moeda {codigo} não encontrada")
        return moeda["id_moeda"]
    finally:
        cur.close()
        conn.close()


def _buscar_saldo(endereco: str, id_moeda: int) -> float:
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT saldo FROM SALDO_CARTEIRA
            WHERE endereco_carteira = %s AND id_moeda = %s
        """, (endereco, id_moeda))
        row = cur.fetchone()
        return float(row[0]) if row else 0.0
    finally:
        cur.close()
        conn.close()


def _atualizar_saldo(endereco: str, id_moeda: int, novo_saldo: float):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO SALDO_CARTEIRA (endereco_carteira, id_moeda, saldo)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE saldo = %s
        """, (endereco, id_moeda, novo_saldo, novo_saldo))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def _registrar_conversao(endereco, id_origem, id_destino, valor_origem, valor_destino, taxa_percentual, taxa_valor, cotacao):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO CONVERSAO 
            (endereco_carteira, id_moeda_origem, id_moeda_destino, valor_origem, valor_destino, taxa_percentual, taxa_valor, cotacao_utilizada)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (endereco, id_origem, id_destino, valor_origem, valor_destino, taxa_percentual, taxa_valor, cotacao))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def _buscar_cotacao(moeda_origem: str, moeda_destino: str) -> float:
    try:
        url = f"https://api.coinbase.com/v2/exchange-rates?currency={moeda_origem}"
        response = requests.get(url).json()
        rates = response["data"]["rates"]

        if moeda_destino not in rates:
            raise HTTPException(400, "Par de conversão não permitido")

        return float(rates[moeda_destino])
    except:
        raise HTTPException(500, "Erro ao consultar cotação externa")


def converter(endereco, moeda_origem, moeda_destino, valor, chave_privada):
    if moeda_origem == moeda_destino:
        raise HTTPException(400, "Moedas devem ser diferentes")

    _validar_carteira(endereco, chave_privada)

    id_origem = _buscar_id_moeda(moeda_origem)
    id_destino = _buscar_id_moeda(moeda_destino)

    saldo_origem = _buscar_saldo(endereco, id_origem)

    taxa = valor * TAXA_CONVERSAO
    total = valor + taxa

    if saldo_origem < total:
        raise HTTPException(400, "Saldo insuficiente para conversão")

    cotacao = _buscar_cotacao(moeda_origem, moeda_destino)
    valor_convertido = valor * cotacao

    _atualizar_saldo(endereco, id_origem, saldo_origem - total)

    saldo_destino = _buscar_saldo(endereco, id_destino)
    _atualizar_saldo(endereco, id_destino, saldo_destino + valor_convertido)

    _registrar_conversao(
        endereco,
        id_origem,
        id_destino,
        valor,
        valor_convertido,
        TAXA_CONVERSAO,
        taxa,
        cotacao
    )

    return {
        "tipo": "conversao",
        "endereco": endereco,
        "origem": moeda_origem,
        "destino": moeda_destino,
        "valor_origem": valor,
        "valor_convertido": valor_convertido,
        "cotacao": cotacao,
        "taxa": taxa,
        "mensagem": "Conversão realizada com sucesso!"
    }
