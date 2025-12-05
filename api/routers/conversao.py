from fastapi import APIRouter
from pydantic import BaseModel
from api.services.conversao_service import converter


router = APIRouter(prefix="/conversao", tags=["Conversão"])


class ConversaoRequest(BaseModel):
    endereco: str
    moeda_origem: str
    moeda_destino: str
    valor: float
    chave_privada: str


@router.post("/")
def fazer_conversao(req: ConversaoRequest):
    return converter(
        req.endereco,
        req.moeda_origem,
        req.moeda_destino,
        req.valor,
        req.chave_privada
    )
