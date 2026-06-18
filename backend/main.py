from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.cashback import calcular_cashback
from backend.database import Base, engine, get_db
from backend.models import ConsultaCashback


Base.metadata.create_all(bind=engine)


def garantir_colunas_novas():
    with engine.connect() as connection:
        tipo_banco = engine.dialect.name

        if tipo_banco == "postgresql":
            connection.execute(
                text(
                    "ALTER TABLE consultas_cashback "
                    "ADD COLUMN IF NOT EXISTS percentual_desconto DOUBLE PRECISION DEFAULT 0"
                )
            )

            connection.execute(
                text(
                    "ALTER TABLE consultas_cashback "
                    "ADD COLUMN IF NOT EXISTS valor_final DOUBLE PRECISION"
                )
            )

            connection.execute(
                text(
                    "UPDATE consultas_cashback "
                    "SET percentual_desconto = 0 "
                    "WHERE percentual_desconto IS NULL"
                )
            )

            connection.execute(
                text(
                    "UPDATE consultas_cashback "
                    "SET valor_final = valor_compra "
                    "WHERE valor_final IS NULL"
                )
            )

            connection.commit()

        if tipo_banco == "sqlite":
            colunas = connection.execute(
                text("PRAGMA table_info(consultas_cashback)")
            ).fetchall()

            nomes_colunas = [coluna[1] for coluna in colunas]

            if "percentual_desconto" not in nomes_colunas:
                connection.execute(
                    text(
                        "ALTER TABLE consultas_cashback "
                        "ADD COLUMN percentual_desconto FLOAT DEFAULT 0"
                    )
                )

            if "valor_final" not in nomes_colunas:
                connection.execute(
                    text(
                        "ALTER TABLE consultas_cashback "
                        "ADD COLUMN valor_final FLOAT"
                    )
                )

            connection.execute(
                text(
                    "UPDATE consultas_cashback "
                    "SET percentual_desconto = 0 "
                    "WHERE percentual_desconto IS NULL"
                )
            )

            connection.execute(
                text(
                    "UPDATE consultas_cashback "
                    "SET valor_final = valor_compra "
                    "WHERE valor_final IS NULL"
                )
            )

            connection.commit()


garantir_colunas_novas()


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CashbackRequest(BaseModel):
    valor_compra: float = Field(gt=0)
    percentual_desconto: float = Field(default=0, ge=0, le=100)
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
        percentual_desconto=dados.percentual_desconto,
        cliente_vip=dados.cliente_vip
    )

    ip_usuario = request.client.host

    nova_consulta = ConsultaCashback(
        ip_usuario=ip_usuario,
        cliente_vip=resultado["cliente_vip"],
        valor_compra=resultado["valor_compra"],
        percentual_desconto=resultado["percentual_desconto"],
        valor_final=resultado["valor_final"],
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