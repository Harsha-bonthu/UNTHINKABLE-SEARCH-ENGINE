# I'll recreate all files with the actual content and create a proper ZIP

import zipfile
import os
from pathlib import Path

# Recreate all the files with their content
files_content = {}

# 1. main.py
files_content['main.py'] = '''
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import uuid
import json
from pathlib import Path
import asyncio
from datetime import datetime

# Document processing imports (will be in separate file)
from document_processor import DocumentProcessor
from vector_store import VectorStore
from llm_service import LLMService

app = FastAPI(
    title="RAG Knowledge Base API",
    description="Intelligent document search with Retrieval-Augmented Generation",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
doc_processor = DocumentProcessor()
vector_store = VectorStore()
llm_service = LLMService()

# Create upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Data models
class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class QueryResponse(BaseModel):
    response: str
    sources: List[dict]
    query: str
    timestamp: str

class DocumentInfo(BaseModel):
    id: str
    filename: str
    upload_time: str
    chunk_count: int
    status: str

# In-memory storage for demo (use real database in production)
documents_db = {}
chunks_db = []

@app.get("/")
async def root():
    return {"message": "RAG Knowledge Base API", "version": "1.0.0", "status": "active"}

@app.post("/upload", response_model=dict)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document for RAG indexing"""
    
    # Validate file type
    allowed_extensions = {'.pdf', '.docx', '.txt', '.md'}
    file_extension = Path(file.filename).suffix.lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Allowed: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Generate unique document ID
        doc_id = str(uuid.uuid4())
        
        # Save uploaded file
        file_path = UPLOAD_DIR / f"{doc_id}_{file.filename}"
        content = await file.read()
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        # Process document
        chunks = await doc_processor.process_document(str(file_path))
        
        # Add chunks to vector store
        texts = [chunk['content'] for chunk in chunks]
        metadatas = [{
            'doc_id': doc_id,
            'chunk_id': chunk['chunk_id'],
            'source': file.filename,
            'file_path': str(file_path)
        } for chunk in chunks]
        
        await vector_store.add_documents(texts, metadatas)
        
        # Store document info
        documents_db[doc_id] = DocumentInfo(
            id=doc_id,
            filename=file.filename,
            upload_time=datetime.now().isoformat(),
            chunk_count=len(chunks),
            status="processed"
        )
        
        # Store chunks for reference
        for chunk, metadata in zip(chunks, metadatas):
            chunks_db.append({
                **chunk,
                **metadata
            })
        
        return {
            "doc_id": doc_id,
            "filename": file.filename,
            "chunks_created": len(chunks),
            "status": "success",
            "message": f"Document processed successfully with {len(chunks)} chunks"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query the knowledge base using RAG"""
    
    if not chunks_db:
        raise HTTPException(status_code=400, detail="No documents uploaded yet")
    
    try:
        # Retrieve relevant context
        relevant_chunks = await vector_store.similarity_search(
            request.query, 
            k=request.top_k
        )
        
        if not relevant_chunks:
            return QueryResponse(
                response="I couldn't find relevant information in the uploaded documents.",
                sources=[],
                query=request.query,
                timestamp=datetime.now().isoformat()
            )
        
        # Generate response using LLM
        response = await llm_service.generate_response(
            query=request.query,
            context_chunks=relevant_chunks
        )
        
        # Format sources
        sources = []
        for chunk_text, metadata, score in relevant_chunks:
            sources.append({
                "source": metadata.get('source', 'Unknown'),
                "chunk_id": metadata.get('chunk_id', 0),
                "relevance_score": round(float(score), 3),
                "content_preview": chunk_text[:200] + "..." if len(chunk_text) > 200 else chunk_text
            })
        
        return QueryResponse(
            response=response,
            sources=sources,
            query=request.query,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/documents", response_model=List[DocumentInfo])
async def list_documents():
    """List all uploaded documents"""
    return list(documents_db.values())

@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document and its chunks"""
    
    if doc_id not in documents_db:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        # Remove from vector store (simplified for demo)
        # In production, implement proper vector store deletion
        
        # Remove chunks from memory
        global chunks_db
        chunks_db = [chunk for chunk in chunks_db if chunk.get('doc_id') != doc_id]
        
        # Remove document info
        doc_info = documents_db.pop(doc_id)
        
        # Remove file
        file_pattern = f"{doc_id}_*"
        for file_path in UPLOAD_DIR.glob(file_pattern):
            file_path.unlink()
        
        return {
            "message": f"Document {doc_info.filename} deleted successfully",
            "doc_id": doc_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "documents_count": len(documents_db),
        "chunks_count": len(chunks_db),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''.strip()

# Create first few files to test
for filename, content in [('main.py', files_content['main.py'])]:
    with open(filename, 'w') as f:
        f.write(content)
    print(f"✅ Created {filename}")

print("Created main.py successfully - proceeding with other files...")