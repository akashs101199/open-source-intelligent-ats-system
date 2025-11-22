"""
Experience Synthesizer Agent - Evaluates quality and impact of work experience
"""
from typing import Dict, Any
from .base_agent import BaseAgent
from ..services.llm_service import llm_service
from ..models.schemas import ResumeData, JobDescription
import json

class ExperienceSynthesizerAgent(BaseAgent):
    def __init__(self):
        super().__init__("ExperienceSynthesizerAgent")
    
    async def process(
        self,
        resume_data: ResumeData,
        job_desc: JobDescription
    ) -> Dict[str, Any]:
        """Evaluate experience quality beyond years"""
        self.log_info("Synthesizing experience quality")
        
        # Analyze experience quality
        experience_analysis = await self._analyze_experience_quality(resume_data)
        
        # Assess agentic capabilities
        agentic_capabilities = await self._assess_agentic_capabilities(resume_data)
        
        return {
            "experience_quality_score": experience_analysis.get("quality_score", 0.5),
            "agentic_capability_score": agentic_capabilities.get("agentic_score", 0.5),
            "impact_assessment": experience_analysis.get("impact", ""),
            "autonomous_system_evidence": agentic_capabilities.get("evidence", []),
            "agent_types_built": agentic_capabilities.get("agent_types_built", [])
        }
    
    async def _analyze_experience_quality(self, resume_data: ResumeData) -> Dict[str, Any]:
        """Analyze the quality and impact of experience"""
        
        if not resume_data.experience:
            return {"quality_score": 0.0, "impact": "No experience data"}
        
        # Prepare experience context
        exp_texts = []
        for exp in resume_data.experience:
            exp_text = f"""
Role: {exp.role}
Company: {exp.company}
Duration: {exp.duration}
Description: {exp.description}
Achievements: {exp.achievements or 'Not specified'}
Technologies: {', '.join(exp.technologies) if exp.technologies else 'Not specified'}
"""
            exp_texts.append(exp_text)
        
        full_experience = "\n---\n".join(exp_texts[:3])  # Limit to top 3 roles
        
        prompt = f"""Analyze the quality and impact of this candidate's experience for an Agentic AI role.

Experience:
{full_experience}

Evaluate on a scale of 0-10 for each dimension:
1. complexity: Complexity of problems solved
2. scale: Scale of impact (users affected, systems deployed)
3. leadership: Technical leadership and autonomy demonstrated
4. innovation: Innovation and creativity in solutions
5. production: Production system experience vs. prototypes

Focus on WHAT they accomplished, not HOW LONG they worked.
Consider:
- Did they ship products or just experiment?
- What was the technical sophistication?
- Did they make architectural decisions?
- What measurable impact did their work have?

Return JSON:
{{
  "complexity": 8,
  "scale": 7,
  "leadership": 6,
  "innovation": 8,
  "production": 7,
  "quality_score": 7.2,
  "impact": "Brief 2-3 sentence assessment of their impact"
}}

IMPORTANT:
- High scores (8-10) should be given for demonstrable impact and strong technical ownership.
- Do not penalize for "short" duration if the impact is high.
- Look for specific metrics (e.g., "reduced latency by 60%", "delivered $180K savings")."""

        result = await llm_service.generate_structured(prompt)
        
        # Calculate quality score if not provided
        if "quality_score" not in result and "complexity" in result:
            scores = [
                result.get("complexity", 5),
                result.get("scale", 5),
                result.get("leadership", 5),
                result.get("innovation", 5),
                result.get("production", 5)
            ]
            result["quality_score"] = sum(scores) / (len(scores) * 10)  # Normalize to 0-1
        
        return result
    
    async def _assess_agentic_capabilities(self, resume_data: ResumeData) -> Dict[str, Any]:
        """Assess evidence of agentic AI capabilities"""
        
        # Prepare full context
        full_context = {
            "experience": [e.dict() for e in resume_data.experience],
            "projects": [p.dict() for p in resume_data.projects],
            "skills": resume_data.skills.dict()
        }
        
        context_json = json.dumps(full_context, indent=2)[:3000]  # Limit size
        
        prompt = f"""Assess this candidate's capabilities in building Agentic AI systems.

Candidate Profile:
{context_json}

Look for CONCRETE EVIDENCE of:
1. Building autonomous systems that can make decisions and take actions
2. Multi-agent architectures or agent collaboration/coordination
3. Tool use, function calling, external API integration in agent systems
4. Planning and reasoning capabilities in agents (ReAct, CoT, etc.)
5. Handling agent memory and state management
6. Agent evaluation, monitoring, and observability
7. Deployed agent systems in production (not just demos/prototypes)

Rate agentic capability 0-10 based on:
- Depth of agent experience (10 = extensive production agent systems)
- Breadth across different agent patterns
- Evidence of autonomous decision-making systems
- Production deployments vs. experiments

Return JSON:
{{
  "agentic_score": 7,
  "evidence": [
    "Built production chatbot using LangChain with tool use",
    "Implemented multi-agent system for data analysis"
  ],
  "agent_types_built": [
    "conversational_agents",
    "autonomous_research_agents",
    "tool_using_agents"
  ],
  "confidence": "high|medium|low",
  "reasoning": "1-2 sentence explanation"
}}"""

        result = await llm_service.generate_structured(prompt)
        
        # Normalize agentic_score to 0-1
        if "agentic_score" in result:
            result["agentic_score"] = result["agentic_score"] / 10.0
        
        return result