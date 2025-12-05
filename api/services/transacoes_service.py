from fastapi import HTTPException
from api.database import get_connection
from api.core.security import hash_chave_privada


TAXA_SAQUE = 0.01  # 1%


def _validar_carteira(endereco: str, chave_privada: str):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute("SELECT hash_chave_privada FROM CARTEIRA WHERE endereco_carteira = %s", (endereco,))
        carteira = cur.fetchone()

        if not carteira:
            raise HTTPException(404, "Carteira não encontrada")

        hash_enviado = hash_chave_privada(chave_privada)
        if carteira["hash_chave_privada"] != hash_enviado:
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
            raise HTTPException(404, "Moeda não encontrada")
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


def _registrar_movimento(endereco: str, id_moeda: int, tipo: str, valor: float, taxa: float):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO DEPOSITO_SAQUE (endereco_carteira, id_moeda, tipo, valor, taxa_valor)
            VALUES (%s, %s, %s, %s, %s)
        """, (endereco, id_moeda, tipo.upper(), valor, taxa))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def depositar(endereco: str, codigo: str, valor: float, chave_privada: str):
    _validar_carteira(endereco, chave_privada)
    id_moeda = _buscar_id_moeda(codigo)

    saldo_atual = _buscar_saldo(endereco, id_moeda)
    novo_saldo = saldo_atual + valor

    _atualizar_saldo(endereco, id_moeda, novo_saldo)
    _registrar_movimento(endereco, id_moeda, "DEP", valor, 0.0)

    return {
        "tipo": "deposito",
        "endereco": endereco,
        "codigo": codigo,
        "valor": valor,
        "taxa": 0.0,
        "saldo_atual": novo_saldo,
        "mensagem": "Depósito realizado com sucesso!"
    }


def sacar(endereco: str, codigo: str, valor: float, chave_privada: str):
    _validar_carteira(endereco, chave_privada)
    id_moeda = _buscar_id_moeda(codigo)

    saldo_atual = _buscar_saldo(endereco, id_moeda)
    taxa = valor * TAXA_SAQUE
    total = valor + taxa

    if saldo_atual < total:
        raise HTTPException(400, "Saldo insuficiente")

    novo_saldo = saldo_atual - total

    _atualizar_saldo(endereco, id_moeda, novo_saldo)
    _registrar_movimento(endereco, id_moeda, "SAQ", valor, taxa)

    return {
        "tipo": "saque",
        "endereco": endereco,
        "codigo": codigo,
        "valor": valor,
        "taxa": taxa,
        "saldo_atual": novo_saldo,
        "mensagem": "Saque realizado com sucesso!"
    }
