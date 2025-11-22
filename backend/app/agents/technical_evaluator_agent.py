"""
Technical Evaluator Agent - Assesses technical depth and expertise
"""
from typing import Dict, Any
from .base_agent import BaseAgent
from ..services.llm_service import llm_service
from ..models.schemas import ResumeData, JobDescription, TechnicalAreaScores
import json

class TechnicalEvaluatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("TechnicalEvaluatorAgent")
        
        # Key technical areas for Agentic AI roles
        self.key_areas = {
            "llm_expertise": [
                "llm", "gpt", "claude", "llama", "mistral", "fine-tuning",
                "prompt engineering", "few-shot", "zero-shot", "rag"
            ],
            "agent_frameworks": [
                "langchain", "llamaindex", "autogpt", "crewai", "semantic kernel",
                "agent protocol", "haystack", "agentverse"
            ],
            "tool_use": [
                "function calling", "tool use", "api integration", "external tools",
                "tool selection", "plugins"
            ],
            "planning_reasoning": [
                "react", "chain-of-thought", "cot", "planning", "reasoning",
                "multi-step", "tree of thought", "self-ask"
            ],
            "vector_dbs": [
                "vector database", "embeddings", "pinecone", "weaviate", "qdrant",
                "chroma", "milvus", "faiss", "similarity search"
            ],
            "orchestration": [
                "workflow", "orchestration", "multi-agent", "agent coordination",
                "agent communication", "swarm", "hierarchical agents"
            ]
        }
    
    async def process(
        self,
        resume_data: ResumeData,
        job_desc: JobDescription
    ) -> Dict[str, Any]:
        """Evaluate technical capabilities for Agentic AI roles"""
        self.log_info("Evaluating technical depth")
        
        # Keyword-based initial assessment
        technical_area_scores = self._assess_technical_areas(resume_data)
        
        # LLM-based deep technical assessment
        deep_assessment = await self._deep_technical_analysis(resume_data, job_desc)
        
        # Calculate overall technical score
        overall_score = sum(technical_area_scores.dict().values()) / len(technical_area_scores.dict())
        
        return {
            "technical_area_scores": technical_area_scores.dict(),
            "overall_technical_score": overall_score,
            "deep_assessment": deep_assessment
        }
    
    def _assess_technical_areas(self, resume_data: ResumeData) -> TechnicalAreaScores:
        """Assess technical areas using keyword matching"""
        resume_text = json.dumps(resume_data.dict()).lower()
        
        scores = {}
        for area, keywords in self.key_areas.items():
            matches = sum(1 for keyword in keywords if keyword.lower() in resume_text)
            # Normalize: full score if >=3 keywords found
            scores[area] = min(matches / 3.0, 1.0)
        
        return TechnicalAreaScores(**scores)
    
    async def _deep_technical_analysis(
        self,
        resume_data: ResumeData,
        job_desc: JobDescription
    ) -> Dict[str, Any]:
        """Deep technical analysis using LLM"""
        
        # Prepare context
        skills_context = json.dumps(resume_data.skills.dict())
        projects_context = json.dumps([p.dict() for p in resume_data.projects])
        experience_context = json.dumps([e.dict() for e in resume_data.experience])
        
        prompt = f"""You are a technical evaluator for Agentic AI engineering roles.

Candidate's Technical Profile:
Skills: {skills_context}
Projects: {projects_context}
Experience: {experience_context}

Job Requirements:
{job_desc.description}
Required Skills: {', '.join(job_desc.required_skills)}

Evaluate the candidate's technical depth for this Agentic AI role across these dimensions:
1. llm_experience: Direct experience with LLMs and language models (0-10)
2. agent_building: Experience building autonomous, goal-oriented agent systems (0-10)
3. multi_agent: Multi-agent architectures or agent coordination experience (0-10)
4. tool_integration: Tool use, function calling, and API integration capabilities (0-10)
5. planning_systems: Planning, reasoning, and chain-of-thought approaches (0-10)
6. production_experience: Production deployment vs. research/experimental work (0-10)

For each area:
- Provide a rating 0-10
- List specific evidence from their background
- Note any concerns

Return JSON format:
{{
  "ratings": {{
    "llm_experience": 8,
    "agent_building": 7,
    ...
  }},
  "evidence": [
    "Built multi-agent system using LangChain",
    "Implemented ReAct pattern for tool use"
  ],
  "concerns": [
    "Limited production deployment experience"
  ],
  "overall_assessment": "Brief 1-2 sentence summary"
}}

IMPORTANT: 
- If the candidate has strong relevant experience, do not be afraid to give high scores (8-10).
- Look for equivalent technologies (e.g., if they know LangChain, they likely understand agent concepts).
- Consider the depth of their projects and experience description.

Return ONLY JSON, no additional text."""

        result = await llm_service.generate_structured(prompt)
        return result