from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os

# IMPORTACIÓN RELATIVA LIMPIA
# El punto (.) significa: "busca en este mismo paquete/carpeta"
from .logic import process_document_to_vectorstore, generate_response

app = FastAPI()

# --- CONFIGURACIÓN CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------

VECTORSTORE_GLOBAL = None

class QuestionRequest(BaseModel):
    query: str

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    global VECTORSTORE_GLOBAL
    try:
        os.makedirs("data", exist_ok=True)
        file_location = f"data/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        VECTORSTORE_GLOBAL = process_document_to_vectorstore(file_location)
        return {"status": "success", "message": "Documento procesado. Ya puedes preguntar."}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    global VECTORSTORE_GLOBAL
    if VECTORSTORE_GLOBAL is None:
        raise HTTPException(status_code=400, detail="Primero debes subir un documento.")
    try:
        # Recibimos el dict completo {answer, sources}
        result = generate_response(VECTORSTORE_GLOBAL, request.query)
        
        return {
            "answer": result["answer"],
            "sources": result["sources"] # Pasamos la lista de páginas [1, 3, 5]
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))