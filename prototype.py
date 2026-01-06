"""
CloudWalk Level 2.3 - Music Generator Company

Small prototype to validate the architecture. External services are mocked 
on purpose. The focus is on agent orchestration and decision flow, not 
production readiness.
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any


class KnowledgeBase:
    """Simple in-memory RAG store"""
    
    def __init__(self, filepath: str = "knowledge_base.json"):
        with open(filepath, 'r') as f:
            self.data = json.load(f)['knowledge_base']
    
    def get(self, key: str) -> Any:
        return self.data.get(key, [])
    
    def add_track(self, track: Dict[str, str]):
        self.data['recent_tracks'].append(track)
        self.data['recent_genres'].append(track['genre'])
        self.data['recent_genres'] = self.data['recent_genres'][-5:]


class MusicAgent:
    """Generates music daily, avoiding repetition"""
    
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
    
    def generate_track(self) -> Dict[str, str]:
        # Avoid repeating recently used genres
        recent_genres = self.kb.get('recent_genres')
        all_genres = list(self.kb.get('genre_characteristics').keys())
        available_genres = [g for g in all_genres if g not in recent_genres[-3:]]
        
        # Pick mood based on time of day
        hour = datetime.now().hour
        time_of_day = "morning" if 6 <= hour < 12 else "afternoon" if 12 <= hour < 18 else "evening"
        suggested_moods = self.kb.get('mood_by_time').get(time_of_day, ["happy"])
        
        genre = random.choice(available_genres) if available_genres else random.choice(all_genres)
        mood = random.choice(suggested_moods)
        
        track = {
            "title": self._generate_title(genre, mood),
            "genre": genre,
            "mood": mood,
            "timestamp": datetime.now().isoformat()
        }
        
        self.kb.add_track(track)
        return track
    
    def _generate_title(self, genre: str, mood: str) -> str:
        prefixes = {
            "uplifting": ["Rising", "Bright", "Soaring"],
            "energetic": ["Electric", "Dynamic", "Pulsing"],
            "calm": ["Peaceful", "Serene", "Gentle"],
            "happy": ["Joyful", "Sunny", "Cheerful"]
        }
        prefix = random.choice(prefixes.get(mood, ["New"]))
        suffix = random.choice(["Light", "Waves", "Vibes", "Dreams", "Flow"])
        return f"{prefix} {suffix}"


class BillingAgent:
    """Handles $1/month subscriptions - simple deterministic logic"""
    
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
    
    def process_monthly_billing(self) -> Dict[str, Any]:
        users = self.kb.get('users')
        active_users = [u for u in users if u['status'] == 'active']
        
        successful = 0
        failed = 0
        
        for user in active_users:
            if random.random() < 0.95:  # 95% success rate
                successful += 1
            else:
                failed += 1
        
        return {
            "total_users": len(active_users),
            "successful": successful,
            "failed": failed,
            "revenue": successful * 1.0
        }


class MarketingAgent:
    """Promotes music using patterns that worked before"""
    
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
    
    def create_post(self, track: Dict[str, str]) -> Dict[str, str]:
        # Find template with best engagement
        templates = self.kb.get('marketing_templates')
        best_template = max(templates, key=lambda t: t['engagement'])
        
        # Get hashtags for this genre
        hashtags = self.kb.get('hashtags_by_genre').get(track['genre'], ["#Music"])
        
        content = best_template['pattern'].format(
            genre=track['genre'].capitalize(),
            title=track['title'],
            mood=track['mood']
        )
        content += " " + " ".join(hashtags[:2])
        
        return {
            "content": content,
            "platform": "twitter",
            "engagement_score": best_template['engagement'],
            "scheduled_time": best_template['best_time']
        }


class MusicCompany:
    """Orchestrates the three agents"""
    
    def __init__(self):
        self.kb = KnowledgeBase()
        self.music_agent = MusicAgent(self.kb)
        self.billing_agent = BillingAgent(self.kb)
        self.marketing_agent = MarketingAgent(self.kb)
    
    def run_daily_operations(self):
        print("="*60)
        print("AUTONOMOUS MUSIC COMPANY - Daily Operations")
        print("="*60)
        print()
        
        # Generate tracks
        print("🎵 MUSIC AGENT")
        print("-" * 60)
        track = self.music_agent.generate_track()
        print(f"Generated: '{track['title']}'")
        print(f"Genre: {track['genre']} | Mood: {track['mood']}")
        print(f"Context: Avoided {self.kb.get('recent_genres')[-3:]} (recently used)")
        print()
        
        # Process billing
        print("💳 BILLING AGENT")
        print("-" * 60)
        billing_result = self.billing_agent.process_monthly_billing()
        print(f"Processed {billing_result['total_users']} subscriptions")
        print(f"Success: {billing_result['successful']} | Failed: {billing_result['failed']}")
        print(f"Revenue: ${billing_result['revenue']:.2f}")
        print()
        
        # Create marketing post
        print("📱 MARKETING AGENT")
        print("-" * 60)
        post = self.marketing_agent.create_post(track)
        print(f"Created post: {post['content']}")
        print(f"Platform: {post['platform']} | Best time: {post['scheduled_time']}")
        print(f"Context: Using template with {post['engagement_score']}+ engagement")
        print()
        
        print("="*60)
        print("✅ Daily operations completed")
        print("="*60)
        print()
        print("System summary:")
        print("- Music generation adapts based on recent history")
        print("- Marketing decisions reuse high-performing patterns")
        print("- Billing remains deterministic and simple")


def main():
    company = MusicCompany()
    company.run_daily_operations()


if __name__ == "__main__":
    main()
