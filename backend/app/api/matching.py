"""
API routes for candidate matching
"""
from fastapi import APIRouter, HTTPException
from typing import List
import time
from ..models.schemas import MatchRequest, MatchResponse, CandidateScore
from ..models.database import db
from ..services.vector_db_service import vector_db_service
from ..agents.orchestrator_agent import OrchestratorAgent
from ..config import settings
import logging

router = APIRouter(prefix="/api/match", tags=["matching"])
logger = logging.getLogger(__name__)

orchestrator = OrchestratorAgent()

@router.post("", response_model=MatchResponse)
async def match_candidates(request: MatchRequest):
    """Match candidates to a job description"""
    
    start_time = time.time()
    
    # Validate job exists
    job = db.get_job(request.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Step 1: Vector search for initial candidates
    logger.info(f"Searching for candidates matching job {request.job_id}")
    
    query_text = f"{job.title} {job.description} {' '.join(job.responsibilities)} {' '.join(job.required_skills)}"
    
    vector_matches = vector_db_service.search_candidates(
        query_text=query_text,
        top_k=min(request.top_k * 2, settings.MAX_CANDIDATES_PER_MATCH),
        min_score=request.min_score
    )
    
    if not vector_matches:
        return MatchResponse(
            job_id=request.job_id,
            total_candidates=0,
            matches=[],
            processing_time_seconds=time.time() - start_time
        )
    
    logger.info(f"Found {len(vector_matches)} candidates via vector search")
    
    # Step 2: Deep evaluation of top candidates
    scores: List[CandidateScore] = []
    
    for match in vector_matches[:request.top_k]:
        candidate_id = match["candidate_id"]
        candidate_data = db.get_candidate(candidate_id)
        
        if not candidate_data:
            logger.warning(f"Candidate {candidate_id} not found in database")
            continue
        
        try:
            # Get stored file content (in production, store this properly)
            # For now, use resume_text
            resume_text = candidate_data.get("resume_text", "")
            filename = candidate_data.get("filename", "resume.txt")
            
            # Convert text to bytes for processing
            file_content = resume_text.encode('utf-8')
            
            score = await orchestrator.process_candidate(
                file_content=file_content,
                filename=filename,
                job_desc=job,
                candidate_id=candidate_id
            )
            
            # Store score
            db.store_score(request.job_id, candidate_id, score)
            scores.append(score)
            
            logger.info(f"Processed {candidate_id}: score={score.overall_score:.3f}")
            
        except Exception as e:
            logger.error(f"Error processing candidate {candidate_id}: {e}")
            continue
    
    # Sort by overall score
    scores.sort(key=lambda x: x.overall_score, reverse=True)
    
    processing_time = time.time() - start_time
    
    logger.info(f"Matched {len(scores)} candidates in {processing_time:.2f}s")
    
    return MatchResponse(
        job_id=request.job_id,
        total_candidates=len(scores),
        matches=scores,
        processing_time_seconds=round(processing_time, 2)
    )

@router.get("/{job_id}/{candidate_id}", response_model=CandidateScore)
async def get_match_score(job_id: str, candidate_id: str):
    """Get detailed score for a candidate-job pair"""
    
    score = db.get_score(job_id, candidate_id)
    if not score:
        raise HTTPException(
            status_code=404,
            detail="Score not found. Run matching first."
        )
    
    return score

@router.get("/{job_id}/scores")
async def get_job_scores(job_id: str):
    """Get all scores for a job"""
    
    job = db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    scores = db.get_job_scores(job_id)
    
    return {
        "job_id": job_id,
        "job_title": job.title,
        "total_matches": len(scores),
        "scores": [score.dict() for score in scores]
    }