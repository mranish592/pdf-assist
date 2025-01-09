from langchain_huggingface import HuggingFaceEmbeddings
from annoy import AnnoyIndex
import numpy as np
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        logger.info("Initializing VectorStore")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.index = None
        self.documents = []
        self.dimension = None
        
    def add_documents(self, documents: List[Dict]):
        """Add documents to the vector store."""
        texts = [doc['content'] for doc in documents]
        embeddings = self.embeddings.embed_documents(texts)
        
        # Initialize Annoy index
        self.dimension = len(embeddings[0])
        self.index = AnnoyIndex(self.dimension, 'angular')
        
        # Add items to index
        for i, embedding in enumerate(embeddings):
            self.index.add_item(i, embedding)
            
        # Build the index
        self.index.build(10)  # 10 trees - higher is more accurate but slower
        self.documents = documents
        
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar documents."""
        if not self.documents or self.index is None:
            return []
            
        query_embedding = self.embeddings.embed_query(query)
        similar_item_ids = self.index.get_nns_by_vector(query_embedding, k)
        
        return [self.documents[i] for i in similar_item_ids]