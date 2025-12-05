import os
import hashlib
import secrets

def gerar_chaves(private_size: int, public_size: int):
    chave_privada = secrets.token_hex(private_size)
    chave_publica = secrets.token_hex(public_size)
    return chave_publica, chave_privada

def hash_chave_privada(chave_privada: str):
    return hashlib.sha256(chave_privada.encode()).hexdigest()
