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
    Genera respuesta usando LCEL (LangChain Expression Language).
    Esta es la forma moderna que evita errores de 'langchain.chains'.
    """
    # 1. Configurar LLM
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile", 
        temperature=0
    )
    
    # 2. Configurar Retriever (Buscador)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # 3. Prompt (Instrucciones)
    template = """
    Eres un auditor legal experto. Analiza el siguiente contexto del contrato:
    
    {context}
    
    Pregunta: {question}
    
    Si no sabes la respuesta, di que no aparece en el documento.
    Respuesta profesional:
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    # 4. Función auxiliar para formatear docs
    def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])

    # 5. CADENA LCEL (La clave de la actualización)
    # Recupera Docs -> Formatea -> Pasa al Prompt -> LLM -> Texto
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # 6. Ejecutar
    return rag_chain.invoke(query)