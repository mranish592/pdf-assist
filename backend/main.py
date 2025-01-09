from dotenv import load_dotenv
import os
import logging
import sys
import faulthandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('backend.log')
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables first
load_dotenv()
logger.info("Environment variables loaded")

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pdf_processor import PDFProcessor
from database import VectorStore
from rag_pipeline import RAGPipeline

# Verify API key
if not os.getenv("GROQ_API_KEY"):
    logger.error("GROQ_API_KEY not found in environment variables")
    raise ValueError("GROQ_API_KEY not found in environment variables")

app = FastAPI()

# Initialize components
pdf_processor = PDFProcessor()
vector_store = VectorStore()
rag_pipeline = RAGPipeline()
logger.info("Application components initialized")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    text: str

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    """Upload and process a PDF file."""
    logger.info(f"Receiving file upload: {file.filename}")
    try:
        documents = pdf_processor.process_pdf(file.file, filename=file.filename)
        logger.info(f"Processed {len(documents)} text chunks from PDF")
        
        batch_size = 10
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            vector_store.add_documents(batch)
        logger.info("Documents added to vector store")
        
        return {"message": "File processed successfully"}
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
def search(query: Query):
    """Search for relevant text passages."""
    logger.info(f"Received search query: {query.text}")
    try:
        results = vector_store.search(query.text)
        logger.info(f"Found {len(results)} matching passages")
        return results
    except Exception as e:
        logger.error(f"Error during search: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
def ask_question(query: Query):
    """Answer questions using RAG."""
    logger.info(f"Received question: {query.text}")
    try:
        context_docs = vector_store.search(query.text, k=5)
        logger.info(f"Retrieved {len(context_docs)} context documents")
        
        answer = rag_pipeline.generate_answer(query.text, context_docs)
        logger.info("Generated answer using RAG pipeline")
        
        return {
            "answer": answer,
            "sources": context_docs
        }
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000    
    ) 

faulthandler.enable() 