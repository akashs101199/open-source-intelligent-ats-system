"""
In-memory database for POC
Replace with PostgreSQL/MongoDB for production
"""
from typing import Dict, List, Optional
from datetime import datetime
import json
from ..models.schemas import Job, ResumeData, CandidateScore

class InMemoryDatabase:
    def __init__(self):
        self.jobs: Dict[str, Job] = {}
        self.candidates: Dict[str, Dict] = {}
        self.scores: Dict[str, CandidateScore] = {}
        self.resume_data: Dict[str, ResumeData] = {}
        
    # Jobs
    def create_job(self, job_id: str, job: Job) -> Job:
        self.jobs[job_id] = job
        return job
    
    def get_job(self, job_id: str) -> Optional[Job]:
        return self.jobs.get(job_id)
    
    def list_jobs(self) -> List[Job]:
        return list(self.jobs.values())
    
    def delete_job(self, job_id: str) -> bool:
        if job_id in self.jobs:
            del self.jobs[job_id]
            return True
        return False
    
    # Candidates
    def create_candidate(self, candidate_id: str, data: Dict) -> Dict:
        self.candidates[candidate_id] = data
        return data
    
    def get_candidate(self, candidate_id: str) -> Optional[Dict]:
        return self.candidates.get(candidate_id)
    
    def list_candidates(self) -> List[Dict]:
        return list(self.candidates.values())
    
    def store_resume_data(self, candidate_id: str, resume_data: ResumeData):
        self.resume_data[candidate_id] = resume_data
    
    def get_resume_data(self, candidate_id: str) -> Optional[ResumeData]:
        return self.resume_data.get(candidate_id)
    
    # Scores
    def store_score(self, job_id: str, candidate_id: str, score: CandidateScore):
        key = f"{job_id}_{candidate_id}"
        self.scores[key] = score
    
    def get_score(self, job_id: str, candidate_id: str) -> Optional[CandidateScore]:
        key = f"{job_id}_{candidate_id}"
        return self.scores.get(key)
    
    def get_job_scores(self, job_id: str) -> List[CandidateScore]:
        return [
            score for key, score in self.scores.items()
            if key.startswith(f"{job_id}_")
        ]
    
    # Statistics
    def get_statistics(self) -> Dict[str, int]:
        return {
            "total_jobs": len(self.jobs),
            "total_candidates": len(self.candidates),
            "total_scores": len(self.scores)
        }
    
    # Persistence (optional)
    def save_to_file(self, filepath: str):
        data = {
            "jobs": {k: v.dict() for k, v in self.jobs.items()},
            "candidates": self.candidates,
            "scores": {k: v.dict() for k, v in self.scores.items()}
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, default=str)
    
    def load_from_file(self, filepath: str):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.jobs = {k: Job(**v) for k, v in data.get("jobs", {}).items()}
                self.candidates = data.get("candidates", {})
                self.scores = {k: CandidateScore(**v) for k, v in data.get("scores", {}).items()}
        except FileNotFoundError:
            pass

# Global database instance
db = InMemoryDatabase()