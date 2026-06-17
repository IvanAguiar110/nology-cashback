from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from backend.database import Base


class ConsultaCashback(Base):
    __tablename__ = "consultas_cashback"

    id = Column(Integer, primary_key=True, index=True)
    ip_usuario = Column(String, index=True)
    cliente_vip = Column(Boolean)
    valor_compra = Column(Float)
    cashback_base = Column(Float)
    bonus_vip = Column(Float)
    cashback_total = Column(Float)
    criado_em = Column(DateTime, default=datetime.utcnow)