# Main entry point for the Music Generator Company application.

import sys
import logging
from pathlib import Path

from config import LOG_LEVEL, LOG_FORMAT

try:
    from knowledge import KnowledgeBase
except ImportError:
    from knowledge_simple import KnowledgeBase
    logging.warning("ChromaDB not available, using simple knowledge base")

try:
    from llm_service import LLMService
except ImportError:
    from llm_service_simple import LLMService
    logging.warning("LangChain not available, using simple LLM service")

from orchestrator import MusicCompany


def setup_logging():
        logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def check_ollama_availability(llm_service: LLMService) -> bool:
    if not llm_service.is_available():
        logging.warning("=" * 60)
        logging.warning("Ollama LLM not available")
        logging.warning("Running with fallback generation mode")
        logging.warning("=" * 60)
        logging.warning("")
        logging.warning("For full LLM features:")
        logging.warning("  1. Install Ollama: https://ollama.ai")
        logging.warning("  2. Run: ollama pull llama2")
        logging.warning("  3. Restart this application")
        logging.warning("")
        return False
    return True


def print_results(results: dict):
    print("\n" + "=" * 60)
    print("DAILY OPERATIONS SUMMARY")
    print("=" * 60)
    
    if 'track' in results:
        track = results['track']
        print(f"\n[MUSIC] Music Generation")
        print(f"   Track: {track['title']}")
        print(f"   Genre: {track['genre']}")
        print(f"   Mood: {track['mood']}")
        print(f"   Method: {track.get('generation_method', 'unknown')}")
    
    if 'billing' in results:
        billing = results['billing']
        print(f"\n[BILLING] Billing")
        print(f"   Processed: {billing['successful']}/{billing['total_users']} users")
        print(f"   Revenue: ${billing['revenue']:.2f}")
        print(f"   Failed: {billing['failed']}")
    
    if 'marketing' in results:
        marketing = results['marketing']
        print(f"\n[MARKETING] Marketing")
        print(f"   Platform: {marketing['platform']}")
        print(f"   Post: {marketing['content']}")
        print(f"   Scheduled: {marketing['scheduled_time']}")
        print(f"   Engagement Score: {marketing['engagement_score']}")
    
    print("\n" + "=" * 60)
    print("[OK] Operations completed")
    print("=" * 60 + "\n")


def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Initializing Music Generator Company")
        
        kb = KnowledgeBase()
        llm_service = LLMService()
        
        check_ollama_availability(llm_service)
        
        company = MusicCompany(kb, llm_service)
        results = company.run_daily_operations()
        
        print_results(results)
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()



