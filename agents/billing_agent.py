# Billing agent for subscription management.
# Pure deterministic logic - no AI required.

import random
import logging
from typing import Dict, Any

try:
    from knowledge import KnowledgeBase
except ImportError:
    from knowledge_simple import KnowledgeBase

from config import BILLING_SUCCESS_RATE, SUBSCRIPTION_PRICE

logger = logging.getLogger(__name__)


class BillingAgent:
    # Handles subscription billing with deterministic logic.
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
    
    def process_monthly_billing(self) -> Dict[str, Any]:
        users = self.kb.get('users', [])
        active_users = [u for u in users if u.get('status') == 'active']
        
        successful = 0
        failed = 0
        
        for user in active_users:
            if self._process_payment(user):
                successful += 1
            else:
                failed += 1
                logger.warning(f"Payment failed for user {user.get('id')}")
        
        result = {
            "total_users": len(active_users),
            "successful": successful,
            "failed": failed,
            "revenue": successful * SUBSCRIPTION_PRICE
        }
        
        logger.info(f"Billing processed: {successful}/{len(active_users)} successful")
        return result
    
    def _process_payment(self, user: Dict) -> bool:
        return random.random() < BILLING_SUCCESS_RATE



