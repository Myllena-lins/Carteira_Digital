from fastapi import HTTPException
from api.database import get_connection
from api.core.security import hash_chave_privada

TAXA_TRANSFERENCIA = 0.01  # 1%


def _validar_carteira(endereco: str, chave_privada: str):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute("SELECT hash_chave_privada FROM CARTEIRA WHERE endereco_carteira = %s", (endereco,))
        carteira = cur.fetchone()

        if not carteira:
            raise HTTPException(404, "Carteira de origem não encontrada")

        if carteira["hash_chave_privada"] != hash_chave_privada(chave_privada):
            raise HTTPException(403, "Chave privada inválida para autorização")
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
            raise HTTPException(404, f"Moeda {codigo} não existe")
        return moeda["id_moeda"]
    finally:
        cur.close()
        conn.close()


def _buscar_saldo(endereco: str, id_moeda: int):
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


def _registrar_transferencia(endereco_origem, endereco_destino, id_moeda, valor, taxa_valor):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO TRANSFERENCIA 
            (endereco_origem, endereco_destino, id_moeda, valor, taxa_valor)
            VALUES (%s, %s, %s, %s, %s)
        """, (endereco_origem, endereco_destino, id_moeda, valor, taxa_valor))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def transferir(endereco_origem, endereco_destino, moeda, valor, chave_privada):
    if endereco_origem == endereco_destino:
        raise HTTPException(400, "A transferência deve ser entre carteiras diferentes")

    _validar_carteira(endereco_origem, chave_privada)

    id_moeda = _buscar_id_moeda(moeda)

    saldo_origem = _buscar_saldo(endereco_origem, id_moeda)

    taxa = valor * TAXA_TRANSFERENCIA
    total_origem = valor + taxa

    if saldo_origem < total_origem:
        raise HTTPException(400, "Saldo insuficiente para transferência")

    saldo_destino = _buscar_saldo(endereco_destino, id_moeda)

    _atualizar_saldo(endereco_origem, id_moeda, saldo_origem - total_origem)
    _atualizar_saldo(endereco_destino, id_moeda, saldo_destino + valor)

    _registrar_transferencia(
        endereco_origem,
        endereco_destino,
        id_moeda,
        valor,
        taxa
    )

    return {
        "tipo": "transferencia",
        "moeda": moeda,
        "origem": endereco_origem,
        "destino": endereco_destino,
        "valor": valor,
        "taxa": taxa,
        "mensagem": "Transferência realizada com sucesso!"
    }
