import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Cargar variables
load_dotenv()

def process_document_to_vectorstore(file_path):
    """
    Carga PDF, divide y vectoriza usando librerías modernas.
    """
    # 1. Cargar
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # 2. Dividir
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    
    # 3. Embeddings (Local CPU)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # 4. Vectorstore
    vectorstore = FAISS.from_documents(splits, embeddings)
    return vectorstore

def generate_response(vectorstore, query):
    """
    Genera respuesta y devuelve también las fuentes (páginas exactas).
    """
    # 1. Configurar componentes
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) # Traer 3 fragmentos
    
    # 2. Recuperar documentos (Paso explícito para guardar las fuentes)
    docs = retriever.invoke(query)
    
    # 3. Preparar contexto
    def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])
    
    context_text = format_docs(docs)
    
    # 4. Generar respuesta
    template = """
    Eres un asistente legal experto. Analiza el siguiente fragmento del documento legal:
    
    {context}
    
    Pregunta: {question}
    
    Si no sabes la respuesta, di que no aparece en el documento.
    Respuesta profesional:
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    
    answer = chain.invoke({"context": context_text, "question": query})
    
    # 5. RETORNAR DICCIONARIO CON RESPUESTA Y FUENTES
    # Extraemos solo la página de los metadatos para enviarla limpia
    sources_list = [doc.metadata.get("page", 0) for doc in docs]
    
    return {
        "answer": answer,
        "sources": sources_list
    }