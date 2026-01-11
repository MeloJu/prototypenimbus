# LLM service abstraction - simple version without LangChain.

import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)


class LLMService:
    # Handles LLM operations with Ollama API.
    
    def __init__(self, model: str = "llama2", temperature: float = 0.7):
        self.model = model
        self.temperature = temperature
        self.base_url = "http://localhost:11434/api"
        self._check_availability()
    
    def _check_availability(self):
        try:
            response = requests.get(f"{self.base_url}/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                if any(self.model in m.get('name', '') for m in models):
                    logger.info(f"Ollama is available with model {self.model}")
                    self.available = True
                else:
                    logger.warning(f"Model {self.model} not found in Ollama")
                    self.available = False
            else:
                self.available = False
        except Exception as e:
            logger.warning(f"Ollama not available: {e}")
            self.available = False
    
    def generate(self, prompt: str) -> Optional[str]:
        # Generate text using Ollama API.
        if not self.available:
            return None
        
        try:
            logger.info(f"Generating with Ollama model {self.model}...")
            response = requests.post(
                f"{self.base_url}/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.temperature
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json().get('response', '')
                logger.info("Generation completed successfully")
                return result
            return None
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return None
    
    def create_chain(self, prompt_template):
        return None
    
    def is_available(self) -> bool:
        return self.available



