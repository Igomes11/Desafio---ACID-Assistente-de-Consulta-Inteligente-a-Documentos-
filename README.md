# Assistente Inteligente Corporativo - MVP (RAG)

## Sobre o Projeto
Primeira versão funcional (MVP) de um Assistente Inteligente Corporativo baseado na arquitetura RAG (Retrieval-Augmented Generation). A aplicação responde a perguntas em linguagem natural utilizando exclusivamente documentos internos (políticas, manuais e normas) como fonte de conhecimento, citando a origem da informação e mitigando o risco de alucinações.

## Arquitetura e Tecnologias
* **Linguagem:** Python 3.11+
* **API REST:** FastAPI (com Uvicorn)
* **Validação:** Pydantic
* **Busca (Retrieval):** Scikit-learn (TF-IDF e Similaridade de Cosseno)
* **IA Generativa:** Google Gemini API (gemini-3.6-flash)
* **Persistência:** SQLite com SQLAlchemy

## Estrutura do Projeto
* `/documentos`: Diretório com os arquivos `.txt` da base de conhecimento.
* `database.py`: Configuração da conexão com o banco de dados.
* `main.py`: Inicialização do FastAPI e definição de rotas.
* `models.py`: Modelos do banco (SQLAlchemy) e validação da API (Pydantic).
* `rag_engine.py`: Motor RAG (leitura, similaridade e comunicação com a IA).

## Como Executar

**1. Configuração do Ambiente**
Crie e ative um ambiente virtual na raiz do projeto:

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
```

**2. Instalação de Dependências**

```bash
pip install -r requirements.txt
```

**3. Variáveis de Ambiente**
Crie um arquivo `.env` na raiz do projeto com a sua chave de API:

```text
GEMINI_API_KEY=sua_chave_de_api_aqui
```

**4. Inicialização do Servidor**

```bash
python -m uvicorn main:app --reload
```

## Testando a API
Com o servidor rodando, acesse a documentação interativa (Swagger UI) pelo navegador no endereço `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)`.

* **`POST /perguntar`**: Recebe um JSON com a `pergunta`, executa o RAG e retorna a `resposta` e a `fonte`.
* **`GET /historico`**: Retorna todas as consultas armazenadas no banco SQLite.

---
**Autor:** Igor Luiz Gomes Pedrosa
