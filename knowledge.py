# Vector database management using ChromaDB for RAG.

import os
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logging.warning("ChromaDB not available, falling back to simple storage")

from config import CHROMA_DB_PATH, GENRE_CHARACTERISTICS, MOOD_BY_TIME

logger = logging.getLogger(__name__)


class KnowledgeBase:
    # Manages music knowledge using ChromaDB for semantic search and retrieval.
    
    def __init__(self, persist_directory: str = CHROMA_DB_PATH):
        self.persist_directory = persist_directory
        
        if CHROMADB_AVAILABLE:
            self._init_chromadb()
        else:
            self._init_fallback()
    
    def _init_chromadb(self):
        # Initialize ChromaDB client and collections.
        try:
            self.client = chromadb.Client(Settings(
                persist_directory=self.persist_directory,
                anonymized_telemetry=False
            ))
            
            self.tracks_collection = self.client.get_or_create_collection(
                name="music_tracks",
                metadata={"description": "Generated music tracks"}
            )
            
            self.context_collection = self.client.get_or_create_collection(
                name="music_context",
                metadata={"description": "Music generation context and rules"}
            )
            
            self._seed_initial_knowledge()
            logger.info("ChromaDB initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            self._init_fallback()
    
    def _init_fallback(self):
        # Fallback to simple JSON storage.
        self.client = None
        self.tracks_collection = None
        self.context_collection = None
        self.fallback_data = {
            'tracks': [],
            'genre_characteristics': GENRE_CHARACTERISTICS,
            'mood_by_time': MOOD_BY_TIME,
            'recent_genres': []
        }
        logger.info("Using fallback JSON storage")
    
    def _seed_initial_knowledge(self):
        # Seed ChromaDB with initial music knowledge.
        if not self.context_collection:
            return
        
        try:
            count = self.context_collection.count()
            if count > 0:
                return
            
            # Add genre characteristics
            for genre, chars in GENRE_CHARACTERISTICS.items():
                text = f"Genre {genre}: {chars['description']}"
                self.context_collection.add(
                    documents=[text],
                    metadatas=[{"type": "genre", "genre": genre, **chars}],
                    ids=[f"genre_{genre}"]
                )
            
            # Add mood mappings
            for time_period, moods in MOOD_BY_TIME.items():
                text = f"Time period {time_period} suggests moods: {', '.join(moods)}"
                self.context_collection.add(
                    documents=[text],
                    metadatas=[{"type": "mood_mapping", "time": time_period, "moods": json.dumps(moods)}],
                    ids=[f"mood_{time_period}"]
                )
            
            logger.info("Initial knowledge seeded to ChromaDB")
            
        except Exception as e:
            logger.error(f"Failed to seed knowledge: {e}")
    
    def add_track(self, track: Dict[str, str]):
        # Add a generated track to the knowledge base.
        try:
            if self.tracks_collection:
                text = f"{track['genre']} music with {track['mood']} mood: {track['title']}"
                self.tracks_collection.add(
                    documents=[text],
                    metadatas=[track],
                    ids=[f"track_{datetime.now().timestamp()}"]
                )
                logger.info(f"Track added to ChromaDB: {track['title']}")
            else:
                self.fallback_data['tracks'].append(track)
                if track['genre'] not in self.fallback_data['recent_genres']:
                    self.fallback_data['recent_genres'].append(track['genre'])
                logger.info(f"Track added to fallback: {track['title']}")
                
        except Exception as e:
            logger.error(f"Failed to add track: {e}")
    
    def query_similar_tracks(self, query: str, n_results: int = 5) -> Dict:
        # Query for similar tracks using semantic search.
        try:
            if self.tracks_collection:
                results = self.tracks_collection.query(
                    query_texts=[query],
                    n_results=n_results
                )
                return results
            else:
                # Simple fallback search
                return {
                    'documents': [[]],
                    'metadatas': [[]],
                    'distances': [[]]
                }
                
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return {'documents': [[]], 'metadatas': [[]], 'distances': [[]]}
    
    def get(self, key: str, default=None):
        # Get data from knowledge base.
        if self.client:
            try:
                if key == 'recent_genres':
                    results = self.tracks_collection.get()
                    if results and results['metadatas']:
                        return [m['genre'] for m in results['metadatas'][-10:]]
                    return []
                elif key == 'genre_characteristics':
                    return GENRE_CHARACTERISTICS
                elif key == 'mood_by_time':
                    return MOOD_BY_TIME
            except Exception as e:
                logger.error(f"Failed to get {key}: {e}")
        
        return self.fallback_data.get(key, default)
