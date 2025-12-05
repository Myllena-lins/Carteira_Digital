from api.database import get_connection
from api.core.security import gerar_chaves, hash_chave_privada
from api.core.config import settings
from fastapi import HTTPException

def criar_carteira():
    public_key, private_key = gerar_chaves(
        settings.PRIVATE_KEY_SIZE,
        settings.PUBLIC_KEY_SIZE
    )
    hashed_private = hash_chave_privada(private_key)

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO CARTEIRA (endereco_carteira, hash_chave_privada)
        VALUES (%s, %s)
    """

    try:
        cursor.execute(insert_query, (public_key, hashed_private))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    return {
        "endereco_carteira": public_key,
        "chave_privada": private_key  # só retorna aqui
    }


def buscar_carteira(endereco: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT endereco_carteira, data_criacao, status
        FROM CARTEIRA
        WHERE endereco_carteira = %s
    """

    try:
        cursor.execute(query, (endereco,))
        data = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

    return data


def buscar_saldos(endereco: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            M.codigo AS moeda,
            S.saldo
        FROM SALDO_CARTEIRA S
        JOIN MOEDA M ON S.id_moeda = M.id_moeda
        WHERE S.endereco_carteira = %s
    """

    try:
        cursor.execute(query, (endereco,))
        result = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return result or []
