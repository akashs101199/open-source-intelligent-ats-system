"""
Orchestrator Agent - Coordinates all agents and produces final scoring
"""
from typing import Dict, Any
import asyncio
import numpy as np
from .base_agent import BaseAgent
from .parser_agent import ParserAgent
from .semantic_analyzer_agent import SemanticAnalyzerAgent
from .technical_evaluator_agent import TechnicalEvaluatorAgent
from .experience_synthesizer_agent import ExperienceSynthesizerAgent
from ..services.llm_service import llm_service
from ..models.schemas import (
    ResumeData, JobDescription, CandidateScore
)
from ..config import settings

class OrchestratorAgent(BaseAgent):
    # Provide a minimal implementation for the abstract `process` method required by BaseAgent
    async def process(self, *args, **kwargs) -> Dict[str, Any]:
        """Placeholder process method.
        The orchestrator primarily uses `process_candidate`; this method is only
        needed to satisfy the abstract base class contract. It logs the call
        and returns an empty dict.
        """
        self.log_debug("OrchestratorAgent.process called with args=%s, kwargs=%s" % (args, kwargs))
        return {}
    def __init__(self):
        super().__init__("OrchestratorAgent")
        self.parser = ParserAgent()
        self.semantic_analyzer = SemanticAnalyzerAgent()
        self.technical_evaluator = TechnicalEvaluatorAgent()
        self.experience_synthesizer = ExperienceSynthesizerAgent()

    def _sanitize(self, obj):
        """Recursively convert numpy arrays to plain Python types for Pydantic serialization."""
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, dict):
            return {k: self._sanitize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._sanitize(v) for v in obj]
        return obj
    
    async def process_candidate(
        self,
        file_content: bytes,
        filename: str,
        job_desc: JobDescription,
        candidate_id: str
    ) -> CandidateScore:
        """Orchestrate all agents to evaluate candidate"""
        self.log_info(f"Processing candidate {candidate_id} for job {job_desc.title}")
        
        # Step 1: Parse resume
        resume_data = await self.parser.process(file_content, filename)
        
        # Step 2: Run agents in parallel
        semantic_result, technical_result, experience_result = await asyncio.gather(
            self.semantic_analyzer.process(resume_data, job_desc),
            self.technical_evaluator.process(resume_data, job_desc),
            self.experience_synthesizer.process(resume_data, job_desc)
        )
        
        # Step 3: Calculate composite score
        scores = self._calculate_composite_score(
            semantic_result,
            technical_result,
            experience_result
        )
        
        # Step 4: Identify strengths and gaps
        strengths, gaps = self._identify_strengths_and_gaps(
            resume_data,
            semantic_result,
            technical_result,
            experience_result,
            job_desc
        )
        
        # Step 5: Generate final reasoning
        reasoning = await self._generate_final_reasoning(
            resume_data,
            job_desc,
            scores,
            strengths,
            gaps
        )
        
        # Ensure all parts of the detailed analysis are JSON‑serialisable
        sanitized_semantic = self._sanitize(semantic_result)
        sanitized_technical = self._sanitize(technical_result)
        sanitized_experience = self._sanitize(experience_result)
        sanitized_resume = self._sanitize(resume_data.dict())

        return CandidateScore(
            candidate_id=candidate_id,
            overall_score=scores["overall"],
            semantic_match=scores["semantic"],
            technical_depth=scores["technical"],
            experience_quality=scores["experience"],
            agentic_capabilities=scores["agentic"],
            detailed_analysis={
                "semantic": sanitized_semantic,
                "technical": sanitized_technical,
                "experience": sanitized_experience,
                "resume_data": sanitized_resume,
            },
            strengths=strengths,
            gaps=gaps,
            reasoning=reasoning,
        )
    
    def _calculate_composite_score(
        self,
        semantic_result: Dict,
        technical_result: Dict,
        experience_result: Dict
    ) -> Dict[str, float]:
        """Calculate weighted composite score"""
        
        # Extract individual scores
        semantic_scores = semantic_result["semantic_scores"]
        semantic_avg = sum(semantic_scores.values()) / len(semantic_scores)
        
        technical_score = technical_result["overall_technical_score"]
        experience_score = experience_result["experience_quality_score"]
        agentic_score = experience_result["agentic_capability_score"]
        
        # Weighted combination for Agentic AI roles
        # Prioritize: Agentic capabilities > Technical depth > Semantic match > Experience duration
        overall = (
            agentic_score * settings.WEIGHT_AGENTIC +
            technical_score * settings.WEIGHT_TECHNICAL +
            semantic_avg * settings.WEIGHT_SEMANTIC +
            experience_score * settings.WEIGHT_EXPERIENCE
        )
        
        return {
            "overall": round(overall, 3),
            "semantic": round(semantic_avg, 3),
            "technical": round(technical_score, 3),
            "experience": round(experience_score, 3),
            "agentic": round(agentic_score, 3)
        }
    
    def _identify_strengths_and_gaps(
        self,
        resume_data: ResumeData,
        semantic_result: Dict,
        technical_result: Dict,
        experience_result: Dict,
        job_desc: JobDescription
    ) -> tuple:
        """Identify key strengths and gaps"""
        
        strengths = []
        gaps = []
        
        # Agentic capabilities
        agentic_score = experience_result["agentic_capability_score"]
        if agentic_score > 0.7:
            evidence = experience_result.get("autonomous_system_evidence", [])
            if evidence:
                strengths.append(f"Strong agentic AI experience: {evidence[0][:80]}")
        elif agentic_score < 0.4:
            gaps.append("Limited evidence of building autonomous agent systems")
        
        # Technical depth
        tech_scores = technical_result.get("technical_area_scores", {})
        strong_areas = [area.replace('_', ' ').title() 
                       for area, score in tech_scores.items() if score > 0.6]
        weak_areas = [area.replace('_', ' ').title() 
                     for area, score in tech_scores.items() if score < 0.3]
        
        if strong_areas:
            strengths.append(f"Strong technical expertise: {', '.join(strong_areas[:3])}")
        if weak_areas and len(weak_areas) >= 2:
            gaps.append(f"Limited experience in: {', '.join(weak_areas[:3])}")
        
        # Semantic fit
        semantic_scores = semantic_result["semantic_scores"]
        if semantic_scores["experience_match"] > 0.75:
            strengths.append("Highly relevant work experience for this role")
        elif semantic_scores["experience_match"] < 0.5:
            gaps.append("Work experience not closely aligned with role requirements")
        
        # Experience quality
        exp_score = experience_result["experience_quality_score"]
        if exp_score > 0.7:
            strengths.append("High-impact experience with demonstrated results")
        
        # Deep assessment insights
        deep_assessment = technical_result.get("deep_assessment", {})
        if isinstance(deep_assessment, dict):
            evidence = deep_assessment.get("evidence", [])
            concerns = deep_assessment.get("concerns", [])
            
            for ev in evidence[:2]:
                if len(strengths) < 5:
                    strengths.append(ev[:100])
            
            for concern in concerns[:2]:
                if len(gaps) < 5:
                    gaps.append(concern[:100])
        
        return strengths[:5], gaps[:5]
    
    async def _generate_final_reasoning(
        self,
        resume_data: ResumeData,
        job_desc: JobDescription,
        scores: Dict[str, float],
        strengths: list,
        gaps: list
    ) -> str:
        """Generate human-readable reasoning for the score"""
        
        strengths_text = "\n".join(f"- {s}" for s in strengths)
        gaps_text = "\n".join(f"- {g}" for g in gaps)
        
        prompt = f"""Generate a concise evaluation summary for this Agentic AI role candidate.

Job: {job_desc.title}

Candidate Scores:
- Overall: {scores['overall']:.0%}
- Agentic Capabilities: {scores['agentic']:.0%}
- Technical Depth: {scores['technical']:.0%}
- Semantic Match: {scores['semantic']:.0%}
- Experience Quality: {scores['experience']:.0%}

Key Strengths:
{strengths_text}

Areas for Consideration:
{gaps_text}

Write a 3-4 sentence evaluation that:
1. Summarizes why this score was given
2. Highlights the most important factors
3. Provides a clear recommendation (Strong Recommend, Recommend, Consider, or Pass)
4. Focuses on substance and specific capabilities, not generic statements

Be direct and actionable."""

        response = await llm_service.generate(prompt, temperature=0.3)
        return response[:600]  # Limit length