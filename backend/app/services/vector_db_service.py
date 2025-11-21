"""
Service for vector database operations using Qdrant
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import logging
from ..config import settings

logger = logging.getLogger(__name__)

class VectorDBService:
    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )
        self.collection_name = settings.QDRANT_COLLECTION
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.dimension = settings.EMBEDDING_DIMENSION
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Create collection if it doesn't exist"""
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            
            if not exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.dimension,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error ensuring collection: {e}")
    
    def encode_text(self, text: str) -> List[float]:
        """Generate embedding for text"""
        return self.embedding_model.encode(text).tolist()
    
    def store_candidate(
        self,
        candidate_id: str,
        resume_text: str,
        metadata: Dict
    ) -> bool:
        """Store candidate resume in vector database"""
        try:
            embedding = self.encode_text(resume_text)
            
            # Generate numeric ID from string
            point_id = abs(hash(candidate_id)) % (2**63)
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload={
                            "candidate_id": candidate_id,
                            "resume_snippet": resume_text[:1000],
                            "metadata": metadata
                        }
                    )
                ]
            )
            logger.info(f"Stored candidate {candidate_id} in vector DB")
            return True
            
        except Exception as e:
            logger.error(f"Error storing candidate: {e}")
            return False
    
    def search_candidates(
        self,
        query_text: str,
        top_k: int = 10,
        min_score: float = 0.0
    ) -> List[Dict]:
        """Search for matching candidates"""
        try:
            query_embedding = self.encode_text(query_text)
            
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                score_threshold=min_score
            )
            
            return [
                {
                    "candidate_id": hit.payload["candidate_id"],
                    "similarity_score": float(hit.score),
                    "metadata": hit.payload.get("metadata", {})
                }
                for hit in results
            ]
            
        except Exception as e:
            logger.error(f"Error searching candidates: {e}")
            return []
    
    def delete_candidate(self, candidate_id: str) -> bool:
        """Delete candidate from vector database"""
        try:
            point_id = abs(hash(candidate_id)) % (2**63)
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[point_id]
            )
            return True
        except Exception as e:
            logger.error(f"Error deleting candidate: {e}")
            return False
    
    def check_health(self) -> bool:
        """Check if Qdrant service is available"""
        try:
            self.client.get_collections()
            return True
        except:
            return False

vector_db_service = VectorDBService()