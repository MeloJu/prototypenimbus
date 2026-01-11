# LLM service abstraction using LangChain and Ollama.

import logging
import requests
from typing import Optional

try:
    from langchain.llms import Ollama
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    logging.warning("LangChain not available, using simple LLM service")

from config import OLLAMA_MODEL, OLLAMA_TEMPERATURE

logger = logging.getLogger(__name__)


class LLMService:
    # Handles LLM operations using LangChain and Ollama.
    
    def __init__(self, model: str = OLLAMA_MODEL, temperature: float = OLLAMA_TEMPERATURE):
        self.model = model
        self.temperature = temperature
        self.base_url = "http://localhost:11434"
        
        if LANGCHAIN_AVAILABLE:
            self._init_langchain()
        else:
            self._init_simple()
    
    def _init_langchain(self):
        # Initialize LangChain with Ollama.
        try:
            self.llm = Ollama(
                model=self.model,
                temperature=self.temperature,
                base_url=self.base_url
            )
            
            # Test connection
            if self._test_connection():
                self.available = True
                logger.info(f"LangChain + Ollama initialized with model {self.model}")
            else:
                logger.warning("Ollama not responding, falling back to simple mode")
                self._init_simple()
                
        except Exception as e:
            logger.error(f"Failed to initialize LangChain: {e}")
            self._init_simple()
    
    def _init_simple(self):
        # Initialize simple direct API mode.
        self.llm = None
        if self._test_connection():
            self.available = True
            logger.info(f"Simple Ollama API mode with model {self.model}")
        else:
            self.available = False
            logger.warning("Ollama not available")
    
    def _test_connection(self) -> bool:
        # Test if Ollama is responding.
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return any(self.model in m.get('name', '') for m in models)
            return False
        except Exception:
            return False
    
    def create_chain(self, prompt_template):
        # Create a LangChain chain with the given prompt template.
        if not self.available or not LANGCHAIN_AVAILABLE:
            return None
        
        try:
            if isinstance(prompt_template, str):
                prompt = PromptTemplate(
                    input_variables=[],
                    template=prompt_template
                )
            else:
                prompt = prompt_template
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            return chain
            
        except Exception as e:
            logger.error(f"Failed to create chain: {e}")
            return None
    
    def generate(self, prompt: str) -> Optional[str]:
        # Generate text using Ollama API directly.
        if not self.available:
            return None
        
        try:
            logger.info(f"Generating with Ollama model {self.model}...")
            
            if LANGCHAIN_AVAILABLE and self.llm:
                # Use LangChain
                response = self.llm(prompt)
                logger.info("Generation completed successfully")
                return response
            else:
                # Use direct API
                response = requests.post(
                    f"{self.base_url}/api/generate",
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
    
    def is_available(self) -> bool:
        return self.available
