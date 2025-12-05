from fastapi import APIRouter
from pydantic import BaseModel
from api.services.transacoes_service import depositar, sacar

router = APIRouter(prefix="/transacoes", tags=["Transações"])


class MovimentoRequest(BaseModel):
    endereco: str
    codigo: str
    valor: float
    chave_privada: str


@router.post("/deposito")
def fazer_deposito(req: MovimentoRequest):
    return depositar(req.endereco, req.codigo, req.valor, req.chave_privada)


@router.post("/saque")
def fazer_saque(req: MovimentoRequest):
    return sacar(req.endereco, req.codigo, req.valor, req.chave_privada)
