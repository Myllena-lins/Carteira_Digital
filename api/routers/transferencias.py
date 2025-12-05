from fastapi import APIRouter
from pydantic import BaseModel
from api.services.transferencia_service import transferir

router = APIRouter(prefix="/transferencias", tags=["Transferências"])


class TransferenciaRequest(BaseModel):
    endereco_origem: str
    endereco_destino: str
    moeda: str
    valor: float
    chave_privada: str


@router.post("/")
def realizar_transferencia(req: TransferenciaRequest):
    return transferir(
        req.endereco_origem,
        req.endereco_destino,
        req.moeda,
        req.valor,
        req.chave_privada
    )
