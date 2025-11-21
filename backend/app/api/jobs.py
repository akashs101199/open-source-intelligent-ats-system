"""
API routes for job management
"""
from fastapi import APIRouter, HTTPException
from typing import List
from ..models.schemas import JobDescription, Job, JobCreate
from ..models.database import db
from datetime import datetime

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

@router.post("", response_model=dict)
async def create_job(job: JobCreate):
    """Create a new job description"""
    job_id = f"job_{len(db.jobs) + 1}_{int(datetime.now().timestamp())}"
    
    job_obj = Job(
        id=job_id,
        **job.dict()
    )
    
    db.create_job(job_id, job_obj)
    
    return {
        "job_id": job_id,
        "status": "created",
        "message": f"Job '{job.title}' created successfully"
    }

@router.get("", response_model=dict)
async def list_jobs():
    """List all job descriptions"""
    jobs = db.list_jobs()
    return {
        "jobs": [job.dict() for job in jobs],
        "count": len(jobs)
    }

@router.get("/{job_id}", response_model=Job)
async def get_job(job_id: str):
    """Get a specific job description"""
    job = db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.delete("/{job_id}")
async def delete_job(job_id: str):
    """Delete a job description"""
    success = db.delete_job(job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {"status": "deleted", "job_id": job_id}