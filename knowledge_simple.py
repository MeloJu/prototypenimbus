# Simple knowledge base without ChromaDB dependency.
# Falls back to JSON storage only.

import json
import logging
from typing import Dict, List, Any

from config import KNOWLEDGE_BASE_PATH, MAX_RECENT_GENRES

logger = logging.getLogger(__name__)


class KnowledgeBase:
    # Manages application knowledge base with JSON storage.
    
    def __init__(self, filepath: str = str(KNOWLEDGE_BASE_PATH)):
        self.filepath = filepath
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)['knowledge_base']
        except Exception as e:
            logger.error(f"Failed to load knowledge base: {e}")
            return {}
    
    def get(self, key: str, default=None) -> Any:
        return self.data.get(key, default if default is not None else [])
    
    def add_track(self, track: Dict[str, str]):
        self.data['recent_tracks'].append(track)
        self.data['recent_genres'].append(track['genre'])
        self.data['recent_genres'] = self.data['recent_genres'][-MAX_RECENT_GENRES:]
    
    def query_similar_tracks(self, query: str, n_results: int = 3) -> Dict:
        tracks = self.data.get('recent_tracks', [])[-n_results:]
        return {"documents": [[]], "metadatas": [[]], "count": len(tracks)}
    
    def query_marketing_templates(self, genre: str) -> Dict:
        templates = self.data.get('marketing_templates', [])
        best = max(templates, key=lambda t: t['engagement']) if templates else None
        
        if best:
            return {
                "documents": [[best['pattern']]],
                "metadatas": [[{
                    "engagement": best['engagement'],
                    "best_time": best['best_time']
                }]]
            }
        return {"documents": [[]], "metadatas": [[]]}



