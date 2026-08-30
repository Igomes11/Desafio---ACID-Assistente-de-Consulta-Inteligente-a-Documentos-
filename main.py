from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import database
import models
import rag_engine

#Cria a tabela no banco de dados
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Assistente Corporativo MVP",
    description="API RAG para responder perguntas com base em documentos internos.",
    version="1.0.0"
)

#Dependência do Banco de Dados
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Rota principal: Fazer a pergunta
@app.post("/perguntar", response_model=models.RespostaResponse)
def perguntar(request: models.PerguntaRequest, db: Session = Depends(get_db)):
    if not request.pergunta.strip():
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")

    #Executa a lógica
    texto_resposta, fonte_utilizada = rag_engine.gerar_resposta(request.pergunta)

    #Salvando no banco de dados SQLite
    nova_consulta = models.HistoricoConsulta(
        pergunta=request.pergunta,
        resposta=texto_resposta,
        documento_fonte=fonte_utilizada
    )
    db.add(nova_consulta)
    db.commit()
    db.refresh(nova_consulta)

    return models.RespostaResponse(
        pergunta=request.pergunta,
        resposta=texto_resposta,
        fonte=fonte_utilizada
    )

#Rota para consultar o banco de dados
@app.get("/historico")
def ler_historico(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    consultas = db.query(models.HistoricoConsulta).offset(skip).limit(limit).all()
    return consultas