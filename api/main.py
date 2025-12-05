from fastapi import FastAPI
from api.routers.carteiras import router as carteiras_router
from api.routers.transacoes import router as transacoes_router
from api.routers.conversao import router as conversao_router
from api.routers.transferencias import router as transferencias_router

app = FastAPI()

app.include_router(carteiras_router)
app.include_router(transacoes_router)
app.include_router(conversao_router)
app.include_router(transferencias_router)

@app.get("/")
def home():
    return {"message": "Carteira Digital - Online"}
