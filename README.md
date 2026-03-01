# ⚖️ Legal AI Agent - RAG System para Documentación Legal

Este proyecto es un agente de Inteligencia Artificial diseñado para procesar, vectorizar y consultar documentos legales complejos utilizando la arquitectura RAG (Retrieval-Augmented Generation). 

## 🎯 El Problema de Negocio
En el sector legal y de consultoría, la revisión de contratos y normativas extensas consume cientos de horas. Este proyecto nace para automatizar la extracción de información clave y responder preguntas específicas sobre documentos densos, mejorando la eficiencia y reduciendo errores humanos.

## 🛠️ Stack Tecnológico
Para construir este pipeline de datos y NLP, he utilizado las siguientes tecnologías modernas:
* **Lenguaje:** Python 3.13
* **Framework LLM:** LangChain
* **Procesamiento de Documentos:** `PyPDFLoader`, `RecursiveCharacterTextSplitter`
* **Embeddings & Vector Store:** `HuggingFaceEmbeddings` (all-MiniLM-L6-v2), `FAISS` (búsqueda vectorial en local)
* **Inferencia:** Integración con Groq (`ChatGroq`) para respuestas de ultra baja latencia.

## ⚙️ Estructura del Proyecto
* `/data`: Almacenamiento de los documentos PDF de entrada.
* `/src`: Lógica principal del pipeline de datos (`logic.py`), ingesta y particionado de texto.
* `/frontend`: Interfaz de usuario para interactuar con el agente.
