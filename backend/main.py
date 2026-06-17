from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.cashback import calcular_cashback
from backend.database import Base, engine, get_db
from backend.models import ConsultaCashback


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CashbackRequest(BaseModel):
    valor_compra: float
    cliente_vip: bool


@app.get("/")
def home():
    return {
        "mensagem": "API de Cashback Nology funcionando"
    }


@app.post("/calcular-cashback")
def calcular_cashback_api(
    dados: CashbackRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    resultado = calcular_cashback(
        valor_compra=dados.valor_compra,
        cliente_vip=dados.cliente_vip
    )

    ip_usuario = request.client.host

    nova_consulta = ConsultaCashback(
        ip_usuario=ip_usuario,
        cliente_vip=resultado["cliente_vip"],
        valor_compra=resultado["valor_compra"],
        cashback_base=resultado["cashback_base"],
        bonus_vip=resultado["bonus_vip"],
        cashback_total=resultado["cashback_total"]
    )

    db.add(nova_consulta)
    db.commit()
    db.refresh(nova_consulta)

    return resultado


@app.get("/historico")
def listar_historico(
    request: Request,
    db: Session = Depends(get_db)
):
    ip_usuario = request.client.host

    consultas = (
        db.query(ConsultaCashback)
        .filter(ConsultaCashback.ip_usuario == ip_usuario)
        .order_by(ConsultaCashback.criado_em.desc())
        .all()
    )

    return consultas