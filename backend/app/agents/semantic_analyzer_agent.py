"""
Semantic Analyzer Agent - Deep semantic understanding of candidate fit
"""
from typing import Dict, Any
from .base_agent import BaseAgent
from ..services.llm_service import llm_service
from ..services.vector_db_service import vector_db_service
from ..models.schemas import ResumeData, JobDescription, SemanticScores
import numpy as np

class SemanticAnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__("SemanticAnalyzerAgent")
    
    async def process(
        self,
        resume_data: ResumeData,
        job_desc: JobDescription
    ) -> Dict[str, Any]:
        """Perform deep semantic analysis of candidate fit"""
        self.log_info("Analyzing semantic fit")
        
        # Create rich text representations
        resume_context = self._create_resume_context(resume_data)
        job_context = self._create_job_context(job_desc)
        
        # Generate embeddings for different aspects
        embeddings = self._generate_embeddings(resume_context, job_context)
        
        # Calculate semantic similarities
        semantic_scores = self._calculate_semantic_scores(embeddings)
        
        # LLM-based contextual analysis
        contextual_analysis = await self._contextual_reasoning(
            resume_context,
            job_context
        )
        
        return {
            "semantic_scores": semantic_scores.dict(),
            "contextual_analysis": contextual_analysis,
            "embeddings": embeddings
        }
    
    def _create_resume_context(self, resume_data: ResumeData) -> Dict[str, str]:
        """Create rich textual contexts from resume"""
        experience_texts = []
        for exp in resume_data.experience:
            exp_text = f"{exp.role} at {exp.company}: {exp.description}"
            if exp.achievements:
                exp_text += f" Achievements: {exp.achievements}"
            experience_texts.append(exp_text)
        
        skills_list = (
            resume_data.skills.programming_languages +
            resume_data.skills.frameworks +
            resume_data.skills.ml_tools +
            resume_data.skills.agentic_frameworks +
            resume_data.skills.vector_databases
        )
        
        project_texts = []
        for proj in resume_data.projects:
            proj_text = f"{proj.name}: {proj.description}"
            if proj.technologies:
                proj_text += f" (Tech: {', '.join(proj.technologies)})"
            project_texts.append(proj_text)
        
        return {
            "experience": " ".join(experience_texts),
            "skills": ", ".join(skills_list),
            "projects": " ".join(project_texts),
            "full_context": f"{resume_data.summary or ''} {' '.join(experience_texts)} {' '.join(project_texts)}"
        }
    
    def _create_job_context(self, job_desc: JobDescription) -> Dict[str, str]:
        """Create rich textual contexts from job description"""
        return {
            "responsibilities": " ".join(job_desc.responsibilities),
            "skills": ", ".join(job_desc.required_skills + job_desc.preferred_skills),
            "full_context": f"{job_desc.description} {' '.join(job_desc.responsibilities)}"
        }
    
    def _generate_embeddings(
        self,
        resume_context: Dict[str, str],
        job_context: Dict[str, str]
    ) -> Dict[str, np.ndarray]:
        """Generate embeddings for semantic comparison"""
        return {
            "resume_experience": np.array(vector_db_service.encode_text(resume_context["experience"])),
            "resume_skills": np.array(vector_db_service.encode_text(resume_context["skills"])),
            "resume_projects": np.array(vector_db_service.encode_text(resume_context["projects"])),
            "job_responsibilities": np.array(vector_db_service.encode_text(job_context["responsibilities"])),
            "job_skills": np.array(vector_db_service.encode_text(job_context["skills"]))
        }
    
    def _calculate_semantic_scores(self, embeddings: Dict[str, np.ndarray]) -> SemanticScores:
        """Calculate cosine similarities between different aspects"""
        def cosine_similarity(a, b):
            return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
        
        return SemanticScores(
            experience_match=cosine_similarity(
                embeddings["resume_experience"],
                embeddings["job_responsibilities"]
            ),
            skills_match=cosine_similarity(
                embeddings["resume_skills"],
                embeddings["job_skills"]
            ),
            project_relevance=cosine_similarity(
                embeddings["resume_projects"],
                embeddings["job_responsibilities"]
            )
        )
    
    async def _contextual_reasoning(
        self,
        resume_context: Dict[str, str],
        job_context: Dict[str, str]
    ) -> str:
        """Use LLM for deep contextual understanding"""
        
        prompt = f"""Analyze the semantic fit between this candidate and job role for an Agentic AI position.

Candidate Experience:
{resume_context["experience"][:1500]}

Candidate Projects:
{resume_context["projects"][:1000]}

Job Responsibilities:
{job_context["responsibilities"][:1000]}

Required Skills:
{job_context["skills"][:500]}

Analyze:
1. How well does the candidate's ACTUAL WORK align with job requirements (not just keywords)?
2. What is the depth of their relevant experience?
3. What evidence exists of agentic AI capabilities (autonomous systems, multi-agent, tool use, planning)?
4. What transferable skills and adaptability do they demonstrate?

Provide a 2-3 sentence analysis focusing on substance over buzzwords. Be specific about what makes them a good or poor fit."""

        response = await llm_service.generate(prompt, temperature=0.3)
        return response[:500]  # Limit length