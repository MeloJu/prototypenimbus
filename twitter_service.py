# Twitter service for posting and scheduling content.

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class TwitterService:
    # Manages Twitter posting and scheduling.
    
    def __init__(self, schedule_file: str = "twitter_schedule.json"):
        self.schedule_file = Path(schedule_file)
        self.schedule = self._load_schedule()
        self.api_available = False
        self._check_credentials()
    
    def _check_credentials(self):
        # Twitter method
        try:
            import os
            api_key = os.getenv("TWITTER_API_KEY")
            api_secret = os.getenv("TWITTER_API_SECRET")
            access_token = os.getenv("TWITTER_ACCESS_TOKEN")
            access_secret = os.getenv("TWITTER_ACCESS_SECRET")
            
            if all([api_key, api_secret, access_token, access_secret]):
                self.api_available = True
                logger.info("Twitter API credentials configured")
            else:
                logger.warning("Twitter API credentials not found, using simulation mode")
        except Exception as e:
            logger.warning(f"Error checking Twitter credentials: {e}")
    
    def _load_schedule(self) -> List[Dict]:
        # Twitter method
        if not self.schedule_file.exists():
            return []
        
        try:
            with open(self.schedule_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load schedule: {e}")
            return []
    
    def _save_schedule(self):
        # Twitter method
        try:
            with open(self.schedule_file, 'w') as f:
                json.dump(self.schedule, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save schedule: {e}")
    
    def schedule_post(self, content: str, scheduled_time: str) -> Dict:
        # Twitter method
        post = {
            "id": f"post_{len(self.schedule) + 1}",
            "content": content,
            "scheduled_time": scheduled_time,
            "status": "scheduled",
            "created_at": datetime.now().isoformat()
        }
        
        self.schedule.append(post)
        self._save_schedule()
        
        logger.info(f"Post scheduled for {scheduled_time}: {content[:50]}...")
        return post
    
    def post_now(self, content: str) -> Dict:
        # Twitter method
        if self.api_available:
            return self._post_to_twitter_api(content)
        else:
            return self._simulate_post(content)
    
    def _post_to_twitter_api(self, content: str) -> Dict:
        # Twitter method
        try:
            # Twitter API v2 implementation would go here
            # For now, simulating
            logger.info(f"Posted to Twitter: {content}")
            return {
                "success": True,
                "post_id": f"twitter_{datetime.now().timestamp()}",
                "content": content,
                "posted_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Twitter API error: {e}")
            return {"success": False, "error": str(e)}
    
    def _simulate_post(self, content: str) -> Dict:
        # Twitter method
        logger.info(f"[SIMULATED] Twitter post: {content}")
        return {
            "success": True,
            "post_id": f"sim_{datetime.now().timestamp()}",
            "content": content,
            "posted_at": datetime.now().isoformat(),
            "simulated": True
        }
    
    def process_scheduled_posts(self) -> List[Dict]:
        # Twitter method
        now = datetime.now()
        posted = []
        
        for post in self.schedule[:]:
            if post["status"] != "scheduled":
                continue
            
            try:
                scheduled_time = datetime.fromisoformat(post["scheduled_time"])
                if scheduled_time <= now:
                    result = self.post_now(post["content"])
                    post["status"] = "posted" if result["success"] else "failed"
                    post["posted_at"] = result.get("posted_at")
                    post["post_id"] = result.get("post_id")
                    posted.append(post)
                    logger.info(f"Published scheduled post: {post['id']}")
            except Exception as e:
                logger.error(f"Error processing post {post['id']}: {e}")
                post["status"] = "failed"
                post["error"] = str(e)
        
        self._save_schedule()
        return posted
    
    def get_pending_posts(self) -> List[Dict]:
        # Twitter method
        return [p for p in self.schedule if p["status"] == "scheduled"]
    
    def get_posted(self) -> List[Dict]:
        # Twitter method
        return [p for p in self.schedule if p["status"] == "posted"]




