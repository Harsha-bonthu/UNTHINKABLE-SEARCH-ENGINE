import numpy as np
import faiss
import pickle
from pathlib import Path
from typing import List, Tuple, Dict, Any
import asyncio
from sentence_transformers import SentenceTransformer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    """Vector database for storing and searching document embeddings"""

    def __init__(self, 
                 model_name: str = "all-MiniLM-L6-v2",
                 index_path: str = "vector_index.faiss",
                 metadata_path: str = "vector_metadata.pkl"):

        self.model_name = model_name
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.dimension = 384  # all-MiniLM-L6-v2 embedding dimension

        # Initialize sentence transformer
        logger.info(f"Loading embedding model: {model_name}")
        self.encoder = SentenceTransformer(model_name)

        # Initialize FAISS index
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity

        # Store metadata for each vector
        self.metadata = []
        self.texts = []

        # Load existing index if available
        self._load_index()

    async def add_documents(self, texts: List[str], metadatas: List[Dict[str, Any]]):
        """Add documents to the vector store"""

        if len(texts) != len(metadatas):
            raise ValueError("Number of texts and metadatas must match")

        if not texts:
            return

        logger.info(f"Adding {len(texts)} documents to vector store")

        # Generate embeddings
        embeddings = await self._generate_embeddings(texts)

        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)

        # Add to FAISS index
        self.index.add(embeddings)

        # Store texts and metadata
        self.texts.extend(texts)
        self.metadata.extend(metadatas)

        # Save updated index
        self._save_index()

        logger.info(f"Successfully added {len(texts)} documents. Total vectors: {self.index.ntotal}")

    async def similarity_search(self, 
                              query: str, 
                              k: int = 5) -> List[Tuple[str, Dict[str, Any], float]]:
        """Search for similar documents"""

        if self.index.ntotal == 0:
            return []

        # Generate query embedding
        query_embeddings = await self._generate_embeddings([query])
        query_embedding = query_embeddings[0:1]  # Keep as 2D array

        # Normalize query embedding
        faiss.normalize_L2(query_embedding)

        # Search
        k = min(k, self.index.ntotal)  # Don't search for more than available
        scores, indices = self.index.search(query_embedding, k)

        # Format results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.texts) and idx != -1:  # Valid index
                results.append((
                    self.texts[idx],
                    self.metadata[idx],
                    float(score)
                ))

        return results

    async def _generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for texts"""

        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()

        def encode_texts():
            return self.encoder.encode(
                texts, 
                convert_to_numpy=True,
                show_progress_bar=False
            )

        embeddings = await loop.run_in_executor(None, encode_texts)
        return embeddings.astype('float32')

    def _save_index(self):
        """Save FAISS index and metadata to disk"""
        try:
            # Save FAISS index
            faiss.write_index(self.index, self.index_path)

            # Save metadata and texts
            with open(self.metadata_path, 'wb') as f:
                pickle.dump({
                    'metadata': self.metadata,
                    'texts': self.texts,
                    'model_name': self.model_name
                }, f)

            logger.info(f"Saved vector index with {self.index.ntotal} vectors")

        except Exception as e:
            logger.error(f"Error saving index: {str(e)}")

    def _load_index(self):
        """Load FAISS index and metadata from disk"""
        try:
            index_path = Path(self.index_path)
            metadata_path = Path(self.metadata_path)

            if index_path.exists() and metadata_path.exists():
                # Load FAISS index
                self.index = faiss.read_index(self.index_path)

                # Load metadata and texts
                with open(self.metadata_path, 'rb') as f:
                    data = pickle.load(f)
                    self.metadata = data.get('metadata', [])
                    self.texts = data.get('texts', [])
                    saved_model = data.get('model_name', self.model_name)

                if saved_model != self.model_name:
                    logger.warning(f"Model mismatch: saved={saved_model}, current={self.model_name}")

                logger.info(f"Loaded vector index with {self.index.ntotal} vectors")
            else:
                logger.info("No existing index found, starting fresh")

        except Exception as e:
            logger.error(f"Error loading index: {str(e)}")
            logger.info("Starting with fresh index")
            self.index = faiss.IndexFlatIP(self.dimension)
            self.metadata = []
            self.texts = []

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        return {
            'total_vectors': int(self.index.ntotal),
            'dimension': self.dimension,
            'model_name': self.model_name,
            'total_texts': len(self.texts),
            'total_metadata': len(self.metadata)
        }

    def clear(self):
        """Clear all vectors and metadata"""
        self.index = faiss.IndexFlatIP(self.dimension)
        self.metadata = []
        self.texts = []

        # Remove saved files
        for path in [self.index_path, self.metadata_path]:
            if Path(path).exists():
                Path(path).unlink()

        logger.info("Cleared vector store")