from fastapi import APIRouter, HTTPException
from api.services.carteiras_service import (
    criar_carteira,
    buscar_carteira,
    buscar_saldos
)

router = APIRouter(prefix="/carteiras", tags=["Carteiras"])


@router.post("/")
def criar():
    return criar_carteira()


@router.get("/{endereco_carteira}")
def get_carteira(endereco_carteira: str):
    carteira = buscar_carteira(endereco_carteira)
    if not carteira:
        raise HTTPException(404, "Carteira não encontrada")
    return carteira


@router.get("/{endereco_carteira}/saldos")
def get_saldos(endereco_carteira: str):
    return buscar_saldos(endereco_carteira)
