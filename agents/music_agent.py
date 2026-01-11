# Music generation agent with LLM and RAG capabilities.

import random
import logging
from datetime import datetime
from typing import Dict, List, Optional

try:
    from langchain.prompts import PromptTemplate
except ImportError:
    PromptTemplate = None

try:
    from knowledge import KnowledgeBase
except ImportError:
    from knowledge_simple import KnowledgeBase

try:
    from llm_service import LLMService
except ImportError:
    from llm_service_simple import LLMService

from config import GENRE_AVOIDANCE_WINDOW

logger = logging.getLogger(__name__)


class MusicAgent:
    # Generates music tracks using LLM and contextual data.
    
    MUSIC_PROMPT_TEMPLATE = """You are a creative music producer. Based on the following context, suggest a music track.

Recent genres used (avoid these): {recent_genres}
Time of day: {time_of_day}
Available genres: {available_genres}
Mood suggestions for this time: {mood_suggestions}

Generate a creative track with:
1. A genre (pick from available, avoid recent ones)
2. A mood (from suggestions)
3. A creative title (2-3 words)

Format your response EXACTLY as:
Genre: [genre]
Mood: [mood]
Title: [title]

Keep it simple and creative."""
    
    TITLE_PREFIXES = {
        "uplifting": ["Rising", "Bright", "Soaring", "Elevate"],
        "energetic": ["Electric", "Dynamic", "Pulsing", "Charged"],
        "calm": ["Peaceful", "Serene", "Gentle", "Still"],
        "happy": ["Joyful", "Sunny", "Cheerful", "Radiant"],
        "focused": ["Sharp", "Clear", "Intent", "Precise"],
        "relaxing": ["Soft", "Mellow", "Tranquil", "Easy"]
    }
    
    TITLE_SUFFIXES = ["Light", "Waves", "Vibes", "Dreams", "Flow", "Sound", "Echo", "Path"]
    
    def __init__(self, knowledge_base: KnowledgeBase, llm_service: LLMService):
        self.kb = knowledge_base
        self.llm = llm_service
        self.chain = self._create_chain()
    
    def _create_chain(self):
        if not self.llm.is_available():
            logger.warning("LLM not available, using fallback generation")
            return None
        return True
    
    def generate_track(self) -> Dict[str, str]:
        context = self._build_context()
        
        if self.chain and self.llm.is_available():
            track = self._generate_with_llm(context)
            if track:
                self.kb.add_track(track)
                return track
        
        track = self._generate_fallback(context)
        self.kb.add_track(track)
        return track
    
    def _build_context(self) -> Dict:
        recent_genres = self.kb.get('recent_genres', [])
        all_genres = list(self.kb.get('genre_characteristics', {}).keys())
        available_genres = [g for g in all_genres if g not in recent_genres[-GENRE_AVOIDANCE_WINDOW:]]
        
        hour = datetime.now().hour
        time_of_day = self._determine_time_of_day(hour)
        suggested_moods = self.kb.get('mood_by_time', {}).get(time_of_day, ["happy"])
        
        similar_tracks = self.kb.query_similar_tracks(f"{time_of_day} {', '.join(suggested_moods)}")
        
        return {
            "recent_genres": recent_genres,
            "all_genres": all_genres,
            "available_genres": available_genres if available_genres else all_genres,
            "time_of_day": time_of_day,
            "suggested_moods": suggested_moods,
            "similar_tracks_count": len(similar_tracks['documents'][0]) if similar_tracks['documents'] else 0
        }
    
    def _determine_time_of_day(self, hour: int) -> str:
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        else:
            return "evening"
    
    def _generate_with_llm(self, context: Dict) -> Optional[Dict[str, str]]:
        try:
            prompt = self.MUSIC_PROMPT_TEMPLATE.format(
                recent_genres=", ".join(context['recent_genres'][-3:]) if context['recent_genres'] else "none",
                time_of_day=context['time_of_day'],
                available_genres=", ".join(context['available_genres']),
                mood_suggestions=", ".join(context['suggested_moods'])
            )
            
            response = self.llm.generate(prompt)
            if response:
                return self._parse_llm_response(response, context)
            return None
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return None
    
    def _parse_llm_response(self, response: str, context: Dict) -> Dict[str, str]:
        track = {
            "title": "Untitled",
            "genre": "pop",
            "mood": "happy",
            "timestamp": datetime.now().isoformat(),
            "generation_method": "llm"
        }
        
        for line in response.strip().split('\n'):
            if line.startswith("Genre:"):
                genre = line.split(":", 1)[1].strip().lower()
                if genre in context['all_genres']:
                    track["genre"] = genre
            elif line.startswith("Mood:"):
                track["mood"] = line.split(":", 1)[1].strip().lower()
            elif line.startswith("Title:"):
                title = line.split(":", 1)[1].strip()
                if title:
                    track["title"] = title
        
        return track
    
    def _generate_fallback(self, context: Dict) -> Dict[str, str]:
        genre = random.choice(context['available_genres'])
        mood = random.choice(context['suggested_moods'])
        
        return {
            "title": self._generate_title(mood),
            "genre": genre,
            "mood": mood,
            "timestamp": datetime.now().isoformat(),
            "generation_method": "fallback"
        }
    
    def _generate_title(self, mood: str) -> str:
        prefix = random.choice(self.TITLE_PREFIXES.get(mood, ["New"]))
        suffix = random.choice(self.TITLE_SUFFIXES)
        return f"{prefix} {suffix}"



