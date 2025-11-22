"""
Service for interacting with Ollama LLM
"""
import requests
import logging
from typing import Optional, Dict, Any
from ..config import settings

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.url = settings.OLLAMA_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = settings.OLLAMA_TIMEOUT
    
    async def generate(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 2000,
        system_prompt: Optional[str] = None
    ) -> str:
        """Generate text using Ollama"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            response = requests.post(
                f"{self.url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            return response.json()["response"]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API error: {e}")
            return ""
        except Exception as e:
            logger.error(f"Unexpected error in LLM generation: {e}")
            return ""
    
    async def generate_structured(
        self,
        prompt: str,
        temperature: float = 0.1
    ) -> Dict[str, Any]:
        """Generate structured JSON output"""
        response = await self.generate(prompt, temperature=temperature)
        
        # Extract JSON from response
        import re
        import json
        
        try:
            # Try to find JSON block
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            logger.warning("Could not parse JSON from LLM response")
        
        return {"raw_response": response}
    
    def check_health(self) -> bool:
        """Check if Ollama service is available"""
        try:
            response = requests.get(f"{self.url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

llm_service = LLMService()

