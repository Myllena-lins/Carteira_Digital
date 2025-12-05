from fastapi import APIRouter, HTTPException
from api.services.carteiras_service import criar_carteira, buscar_carteira, buscar_saldos

router = APIRouter(prefix="/carteiras", tags=["Carteiras"])

@router.post("/")
def criar():
    return criar_carteira()

@router.get("/{endereco}")
def get_carteira(endereco: str):
    carteira = buscar_carteira(endereco)
    if not carteira:
        raise HTTPException(404, "Carteira não encontrada")
    return carteira

@router.get("/{endereco}/saldos")
def get_saldos(endereco: str):
    saldos = buscar_saldos(endereco)
    return saldos
