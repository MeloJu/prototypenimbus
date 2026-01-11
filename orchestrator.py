# Company orchestrator - coordinates all agents and operations.

import logging
from typing import Dict, Any

try:
    from knowledge import KnowledgeBase
except ImportError:
    from knowledge_simple import KnowledgeBase

try:
    from llm_service import LLMService
except ImportError:
    from llm_service_simple import LLMService

from agents import MusicAgent, BillingAgent, MarketingAgent

logger = logging.getLogger(__name__)


class MusicCompany:
    # Orchestrates music generation, billing, and marketing operations.
    
    def __init__(self, knowledge_base: KnowledgeBase, llm_service: LLMService):
        self.kb = knowledge_base
        self.llm = llm_service
        
        logger.info("Initializing agents...")
        self.music_agent = MusicAgent(knowledge_base, llm_service)
        self.billing_agent = BillingAgent(knowledge_base)
        self.marketing_agent = MarketingAgent(knowledge_base, llm_service)
        logger.info("All agents initialized successfully")
    
    def run_daily_operations(self) -> Dict[str, Any]:
        logger.info("Starting daily operations")
        
        results = {}
        
        try:
            track = self._run_music_generation()
            results['track'] = track
            
            billing = self._run_billing()
            results['billing'] = billing
            
            marketing = self._run_marketing(track)
            results['marketing'] = marketing
            
            logger.info("Daily operations completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Daily operations failed: {e}")
            raise
    
    def _run_music_generation(self) -> Dict[str, str]:
        logger.info("Generating music track")
        track = self.music_agent.generate_track()
        logger.info(f"Generated track: {track['title']} ({track['genre']})")
        return track
    
    def _run_billing(self) -> Dict[str, Any]:
        logger.info("Processing monthly billing")
        result = self.billing_agent.process_monthly_billing()
        logger.info(f"Billing processed: ${result['revenue']:.2f} revenue")
        return result
    
    def _run_marketing(self, track: Dict[str, str]) -> Dict[str, str]:
        logger.info("Creating marketing content")
        post = self.marketing_agent.create_post(track)
        logger.info(f"Marketing post created for {track['title']}")
        return post



