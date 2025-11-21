"""
Parser Agent - Extracts structured information from resumes
"""
from typing import Dict, Any
from .base_agent import BaseAgent
from ..services.llm_service import llm_service
from ..services.document_service import document_service
from ..models.schemas import ResumeData
import json
import re

class ParserAgent(BaseAgent):
    def __init__(self):
        super().__init__("ParserAgent")
    
    async def process(self, file_content: bytes, filename: str) -> ResumeData:
        """Extract and parse resume into structured format"""
        self.log_info(f"Parsing resume: {filename}")
        
        # Extract text
        text = document_service.extract_text(file_content, filename)
        
        if not text:
            self.log_error("Could not extract text from document")
            return ResumeData(raw_text="")
        
        # Use LLM to parse into structured format
        structured_data = await self._parse_with_llm(text)
        
        # Convert to ResumeData model
        try:
            resume_data = ResumeData(**structured_data, raw_text=text)
            self.log_info("Successfully parsed resume")
            return resume_data
        except Exception as e:
            self.log_error(f"Error creating ResumeData: {e}")
            return ResumeData(raw_text=text)
    
    async def _parse_with_llm(self, text: str) -> Dict[str, Any]:
        """Use LLM to parse resume into structured JSON"""
        
        prompt = f"""You are an expert resume parser specializing in Agentic AI and ML engineering roles.

Analyze the following resume and extract structured information in JSON format.

Resume:
{text[:4000]}  # Limit context

Extract the following information:
1. name: Full name
2. email: Email address
3. phone: Phone number
4. summary: Professional summary (2-3 sentences)
5. experience: List of work experiences, each with:
   - company: Company name
   - role: Job title
   - duration: Time period (e.g., "Jan 2020 - Present")
   - description: What they did
   - achievements: Specific accomplishments
   - technologies: List of technologies used
6. education: List of degrees with:
   - institution: University/School name
   - degree: Degree type (BS, MS, PhD, etc.)
   - field: Field of study
   - year: Graduation year
7. skills: Categorized skills as:
   - programming_languages: []
   - frameworks: []
   - ml_tools: []
   - agentic_frameworks: [] (LangChain, AutoGPT, CrewAI, etc.)
   - vector_databases: []
   - other: []
8. projects: List of projects with name, description, technologies
9. publications: List of paper titles or blog posts
10. github: GitHub profile URL
11. linkedin: LinkedIn profile URL

Return ONLY valid JSON, no markdown formatting or additional text.
If a field is not found, use null or empty list.

Example format:
{{
  "name": "John Doe",
  "email": "john@example.com",
  "experience": [{{"company": "TechCorp", "role": "AI Engineer", ...}}],
  "skills": {{"programming_languages": ["Python", "JavaScript"], ...}},
  ...
}}"""

        response = await llm_service.generate_structured(prompt)
        
        # Validate and clean response
        if "raw_response" in response:
            # Fallback: extract basic info with regex
            return self._fallback_parse(text)
        
        return response
    
    def _fallback_parse(self, text: str) -> Dict[str, Any]:
        """Fallback parsing using regex when LLM fails"""
        self.log_info("Using fallback parsing")
        
        data = {
            "name": None,
            "email": None,
            "phone": None,
            "summary": None,
            "experience": [],
            "education": [],
            "skills": {
                "programming_languages": [],
                "frameworks": [],
                "ml_tools": [],
                "agentic_frameworks": [],
                "vector_databases": [],
                "other": []
            },
            "projects": [],
            "publications": [],
            "github": None,
            "linkedin": None
        }
        
        # Extract email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if email_match:
            data["email"] = email_match.group()
        
        # Extract phone
        phone_match = re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)
        if phone_match:
            data["phone"] = phone_match.group()
        
        # Extract GitHub
        github_match = re.search(r'github\.com/([A-Za-z0-9_-]+)', text, re.IGNORECASE)
        if github_match:
            data["github"] = f"https://github.com/{github_match.group(1)}"
        
        # Extract LinkedIn
        linkedin_match = re.search(r'linkedin\.com/in/([A-Za-z0-9_-]+)', text, re.IGNORECASE)
        if linkedin_match:
            data["linkedin"] = f"https://linkedin.com/in/{linkedin_match.group(1)}"
        
        return data