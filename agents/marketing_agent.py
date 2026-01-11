# Marketing agent for social media content generation.

import logging
from typing import Dict, Optional

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

logger = logging.getLogger(__name__)


class MarketingAgent:
    # Generates marketing content using LLM and performance data.
    
    MARKETING_PROMPT_TEMPLATE = """You are a social media marketing expert for a music streaming platform.

Create an engaging social media post for:
Track: {track_title}
Genre: {genre}
Mood: {mood}

High-performing template example: {best_template}
Suggested hashtags: {hashtags}

Create a short, engaging post (1-2 lines max) that promotes this track. Include 2-3 relevant hashtags.
Keep it casual, exciting, and authentic. Use emojis sparingly."""
    
    def __init__(self, knowledge_base: KnowledgeBase, llm_service: LLMService):
        self.kb = knowledge_base
        self.llm = llm_service
        self.chain = self._create_chain()
    
    def _create_chain(self):
        if not self.llm.is_available() or not PromptTemplate:
            logger.warning("LLM not available, using template-based generation")
            return None
        
        prompt = PromptTemplate(
            input_variables=["track_title", "genre", "mood", "best_template", "hashtags"],
            template=self.MARKETING_PROMPT_TEMPLATE
        )
        return self.llm.create_chain(prompt)
    
    def create_post(self, track: Dict[str, str]) -> Dict[str, str]:
        template_data = self._get_best_template(track['genre'])
        hashtags = self._get_hashtags(track['genre'])
        
        if self.chain:
            content = self._generate_with_llm(track, template_data, hashtags)
            if content:
                return self._build_post_response(content, template_data)
        
        content = self._generate_from_template(track, template_data, hashtags)
        return self._build_post_response(content, template_data)
    
    def _get_best_template(self, genre: str) -> Dict:
        results = self.kb.query_marketing_templates(genre)
        
        if results['documents'] and results['documents'][0]:
            metadata = results['metadatas'][0][0] if results['metadatas'] else {}
            return {
                "pattern": results['documents'][0][0],
                "engagement": metadata.get('engagement', 0),
                "best_time": metadata.get('best_time', '9am')
            }
        
        templates = self.kb.get('marketing_templates', [])
        if templates:
            best = max(templates, key=lambda t: t['engagement'])
            return best
        
        return {
            "pattern": "New {genre} track: {title}! #{genre} #Music",
            "engagement": 0,
            "best_time": "9am"
        }
    
    def _get_hashtags(self, genre: str) -> str:
        hashtags = self.kb.get('hashtags_by_genre', {}).get(genre, ["#Music"])
        return " ".join(hashtags[:3])
    
    def _generate_with_llm(self, track: Dict, template_data: Dict, hashtags: str) -> Optional[str]:
        try:
            content = self.chain.run(
                track_title=track['title'],
                genre=track['genre'].capitalize(),
                mood=track['mood'],
                best_template=template_data['pattern'],
                hashtags=hashtags
            )
            return content.strip()
        except Exception as e:
            logger.error(f"LLM content generation failed: {e}")
            return None
    
    def _generate_from_template(self, track: Dict, template_data: Dict, hashtags: str) -> str:
        try:
            content = template_data['pattern'].format(
                genre=track['genre'].capitalize(),
                title=track['title'],
                mood=track['mood']
            )
            return f"{content} {hashtags}"
        except Exception as e:
            logger.error(f"Template formatting failed: {e}")
            return f"Check out our new {track['genre']} track: {track['title']}! {hashtags}"
    
    def _build_post_response(self, content: str, template_data: Dict) -> Dict[str, str]:
        return {
            "content": content,
            "platform": "twitter",
            "engagement_score": template_data['engagement'],
            "scheduled_time": template_data['best_time']
        }



