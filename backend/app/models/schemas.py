"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class ExperienceLevel(str, Enum):
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    PRINCIPAL = "principal"

class JobDescription(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10)
    responsibilities: List[str] = Field(..., min_items=1)
    required_skills: List[str] = Field(..., min_items=1)
    preferred_skills: List[str] = Field(default_factory=list)
    experience_level: ExperienceLevel = ExperienceLevel.MID
    company: Optional[str] = None
    
    @validator('responsibilities', 'required_skills', 'preferred_skills')
    def clean_list_items(cls, v):
        return [item.strip() for item in v if item.strip()]

class JobCreate(JobDescription):
    pass

class Job(JobDescription):
    id: str
    created_at: datetime = Field(default_factory=datetime.now)

class WorkExperience(BaseModel):
    company: str
    role: str
    duration: str
    description: str
    achievements: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)

class Education(BaseModel):
    institution: str
    degree: str
    field: str
    year: Optional[str] = None

class Skills(BaseModel):
    programming_languages: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    ml_tools: List[str] = Field(default_factory=list)
    agentic_frameworks: List[str] = Field(default_factory=list)
    vector_databases: List[str] = Field(default_factory=list)
    other: List[str] = Field(default_factory=list)

class Project(BaseModel):
    name: str
    description: str
    technologies: List[str] = Field(default_factory=list)
    url: Optional[str] = None

class ResumeData(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    summary: Optional[str] = None
    experience: List[WorkExperience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    skills: Skills = Field(default_factory=Skills)
    projects: List[Project] = Field(default_factory=list)
    publications: List[str] = Field(default_factory=list)
    github: Optional[str] = None
    linkedin: Optional[str] = None
    raw_text: str = ""

class CandidateUpload(BaseModel):
    candidate_id: str
    name: Optional[str] = None
    filename: str
    upload_time: datetime = Field(default_factory=datetime.now)

class SemanticScores(BaseModel):
    experience_match: float = Field(ge=0.0, le=1.0)
    skills_match: float = Field(ge=0.0, le=1.0)
    project_relevance: float = Field(ge=0.0, le=1.0)

class TechnicalAreaScores(BaseModel):
    llm_expertise: float = Field(ge=0.0, le=1.0)
    agent_frameworks: float = Field(ge=0.0, le=1.0)
    tool_use: float = Field(ge=0.0, le=1.0)
    planning_reasoning: float = Field(ge=0.0, le=1.0)
    vector_dbs: float = Field(ge=0.0, le=1.0)
    orchestration: float = Field(ge=0.0, le=1.0)

class CandidateScore(BaseModel):
    candidate_id: str
    overall_score: float = Field(ge=0.0, le=1.0)
    semantic_match: float = Field(ge=0.0, le=1.0)
    technical_depth: float = Field(ge=0.0, le=1.0)
    experience_quality: float = Field(ge=0.0, le=1.0)
    agentic_capabilities: float = Field(ge=0.0, le=1.0)
    detailed_analysis: Dict[str, Any]
    strengths: List[str]
    gaps: List[str]
    reasoning: str
    timestamp: datetime = Field(default_factory=datetime.now)

class MatchRequest(BaseModel):
    job_id: str
    top_k: int = Field(default=10, ge=1, le=50)
    min_score: float = Field(default=0.0, ge=0.0, le=1.0)

class MatchResponse(BaseModel):
    job_id: str
    total_candidates: int
    matches: List[CandidateScore]
    processing_time_seconds: float

class HealthCheck(BaseModel):
    status: str
    version: str
    services: Dict[str, bool]
    statistics: Dict[str, int]