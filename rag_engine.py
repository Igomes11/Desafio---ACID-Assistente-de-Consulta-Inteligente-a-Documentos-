import os
import glob
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from google import genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None
    print("Aviso: GEMINI_API_KEY não encontrada no arquivo .env")

def carregar_documentos(diretorio="documentos"):
    """Lê todos os arquivos .txt do diretório e retorna uma lista de dicionários."""
    documentos = []
    caminho_busca = os.path.join(diretorio, "*.txt")
    
    for caminho_arquivo in glob.glob(caminho_busca):
        nome_arquivo = os.path.basename(caminho_arquivo)
        with open(caminho_arquivo, "r", encoding="utf-8") as file:
            conteudo = file.read()
            documentos.append({
                "nome": nome_arquivo,
                "conteudo": conteudo
            })
    return documentos

def buscar_documento_relevante(pergunta, documentos):
    """Usa TF-IDF e Similaridade de Cosseno para achar o documento mais aderente à pergunta."""
    if not documentos:
        return None
        
    textos = [doc["conteudo"] for doc in documentos]
    textos.append(pergunta)
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(textos)
    
    similaridades = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    indice_mais_relevante = similaridades.argsort()[0][-1]
    
    # Define um limite mínimo de similaridade 
    if similaridades[0][indice_mais_relevante] == 0:
        return None
        
    return documentos[indice_mais_relevante]

def gerar_resposta(pergunta):
    """Executa o fluxo completo do RAG."""
    documentos = carregar_documentos()
    doc_relevante = buscar_documento_relevante(pergunta, documentos)
    
    if not doc_relevante:
        return "Desculpe, não encontrei essa informação nos documentos corporativos.", "Sem fonte"

    # prompt
    nome_arquivo = doc_relevante['nome'].lower()
    if "manual" in nome_arquivo or "procedimento" in nome_arquivo:
        instrucao_formato = "Estruture sua resposta em um formato de passo a passo numerado, se possível."
    else:
        instrucao_formato = "Responda de forma clara e em parágrafos curtos."

    prompt = f"""
    Atue como o Assistente Inteligente Corporativo do Grupo A.
    
    Sua tarefa é responder à pergunta do usuário baseando-se EXCLUSIVAMENTE nas informações contidas no documento fonte abaixo.
    
    REGRAS OBRIGATÓRIAS:
    - Não utilize conhecimentos prévios ou externos.
    - Se a resposta não estiver no documento, diga exatamente: "Desculpe, não encontrei essa informação nos documentos corporativos."
    - {instrucao_formato}

    DOCUMENTO FONTE ({doc_relevante['nome']}):
    {doc_relevante['conteudo']}

    PERGUNTA DO USUÁRIO:
    {pergunta}
    """
    
    if not client:
         return "Erro: Cliente da IA não inicializado (Verifique a chave de API).", doc_relevante['nome']

    max_tentativas = 3
    texto_resposta = ""
    
    for tentativa in range(max_tentativas):
        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
            )
            texto_resposta = response.text
            break 
            
        except Exception as e:
            erro_str = str(e)
            if "503" in erro_str and tentativa < (max_tentativas - 1):
                time.sleep(2)
                continue
            
            texto_resposta = f"Erro ao comunicar com a IA após {tentativa + 1} tentativas: {erro_str}"
            break
        
    return texto_resposta, doc_relevante['nome']