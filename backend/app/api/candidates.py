"""
API routes for candidate management
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional
from ..models.database import db
from ..services.vector_db_service import vector_db_service
from ..services.document_service import document_service
from datetime import datetime
from ..config import settings
from ..models.schemas import CandidateCreate

router = APIRouter(prefix="/api/candidates", tags=["candidates"])

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    candidate_name: Optional[str] = Form(None)
):
    """Upload and index a resume"""
    
    # Validate file size
    content = await file.read()
    if len(content) > settings.MAX_RESUME_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds {settings.MAX_RESUME_SIZE_MB}MB limit"
        )
    
    # Validate file type
    allowed_extensions = ['.pdf', '.docx', '.txt']
    if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Allowed: PDF, DOCX, TXT"
        )
    
    # Extract text
    text = document_service.extract_text(content, file.filename)
    if not text:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from file"
        )
    
    # Generate candidate ID
    candidate_id = f"candidate_{len(db.candidates) + 1}_{int(datetime.now().timestamp())}"
    
    # Store candidate info
    candidate_data = {
        "id": candidate_id,
        "name": candidate_name or file.filename.rsplit('.', 1)[0],
        "resume_text": text,
        "filename": file.filename,
        "upload_time": datetime.now().isoformat(),
        "file_size_kb": len(content) / 1024
    }
    
    db.create_candidate(candidate_id, candidate_data)
    
    # Store in vector database
    metadata = {
        "name": candidate_data["name"],
        "filename": file.filename,
        "upload_time": candidate_data["upload_time"]
    }
    
    success = vector_db_service.store_candidate(candidate_id, text, metadata)
    
    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to index resume in vector database"
        )
    
    return {
        "candidate_id": candidate_id,
        "name": candidate_data["name"],
        "status": "uploaded",
        "indexed": success
    }

@router.post("", response_model=dict)
async def create_candidate(candidate: CandidateCreate):
    """Manually create a candidate"""
    
    # Store candidate info
    candidate_data = {
        "id": candidate.candidate_id,
        "name": candidate.name or "Unknown",
        "resume_text": candidate.resume_text,
        "filename": "manual_entry.txt",
        "upload_time": datetime.now().isoformat(),
        "file_size_kb": len(candidate.resume_text.encode('utf-8')) / 1024
    }
    
    db.create_candidate(candidate.candidate_id, candidate_data)
    
    # Store in vector database
    success = vector_db_service.store_candidate(
        candidate.candidate_id, 
        candidate.resume_text, 
        candidate.metadata
    )
    
    return {
        "status": "stored",
        "candidate_id": candidate.candidate_id,
        "indexed": success
    }

@router.get("")
async def list_candidates():
    """List all candidates"""
    candidates = db.list_candidates()
    return {
        "candidates": candidates,
        "count": len(candidates)
    }

@router.get("/{candidate_id}")
async def get_candidate(candidate_id: str):
    """Get candidate details"""
    candidate = db.get_candidate(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Remove full resume text for summary view
    summary = candidate.copy()
    if "resume_text" in summary:
        summary["resume_text_preview"] = summary["resume_text"][:200] + "..."
        del summary["resume_text"]
    
    return summary

@router.delete("/{candidate_id}")
async def delete_candidate(candidate_id: str):
    """Delete a candidate"""
    candidate = db.get_candidate(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Delete from vector DB
    vector_db_service.delete_candidate(candidate_id)
    
    # Delete from database (in production, implement this in db class)
    # For now, we'll just mark as deleted
    
    return {"status": "deleted", "candidate_id": candidate_id}