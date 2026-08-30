from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from pydantic import BaseModel
from database import Base

#Modelos do Banco de Dados
class HistoricoConsulta(Base):
    __tablename__ = "historico_consultas"

    id = Column(Integer, primary_key=True, index=True)
    pergunta = Column(String, index=True)
    resposta = Column(String)
    documento_fonte = Column(String)
    data_hora = Column(DateTime, default=datetime.utcnow)


#Modelos de Validação da API

class PerguntaRequest(BaseModel):
    pergunta: str

class RespostaResponse(BaseModel):
    pergunta: str
    resposta: str
    fonte: str