"""
Core RAG implementation for space mission data analysis.
Based on LlamaIndex with production-ready features.
"""

import os
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.embeddings import resolve_embed_model
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.tools import QueryEngineTool

import chromadb
from chromadb.config import Settings as ChromaSettings

logger = logging.getLogger(__name__)


class SpaceMissionRAG:
    """
    Production-ready RAG system for space mission data analysis.
    
    Features:
    - Persistent vector storage with ChromaDB
    - Configurable LLM and embedding models
    - Mission-specific data filtering
    - Production error handling and logging
    """
    
    def __init__(
        self,
        persist_dir: str = "./data/chroma_db",
        collection_name: str = "space_missions",
        llm_model: str = "gpt-4",
        embedding_model: str = "text-embedding-3-large"
    ):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.llm_model = llm_model
        self.embedding_model = embedding_model
        
        # Ensure persist directory exists
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self._setup_llama_index_settings()
        self._setup_vector_store()
        
        self.index = None
        self.query_engine = None
        
    def _setup_llama_index_settings(self):
        """Configure global LlamaIndex settings."""
        try:
            # Configure LLM
            Settings.llm = OpenAI(
                model=self.llm_model,
                temperature=0.1,
                max_tokens=1024
            )
            
            # Configure embedding model
            Settings.embed_model = resolve_embed_model(f"local:{self.embedding_model}")
            
            logger.info(f"Configured LLM: {self.llm_model}, Embeddings: {self.embedding_model}")
            
        except Exception as e:
            logger.error(f"Failed to setup LlamaIndex settings: {e}")
            raise
    
    def _setup_vector_store(self):
        """Initialize ChromaDB vector store."""
        try:
            # Create ChromaDB client with persistence
            chroma_client = chromadb.PersistentClient(
                path=self.persist_dir,
                settings=ChromaSettings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            chroma_collection = chroma_client.get_or_create_collection(
                name=self.collection_name
            )
            
            # Create LlamaIndex vector store
            self.vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
            
            logger.info(f"ChromaDB initialized with collection: {self.collection_name}")
            
        except Exception as e:
            logger.error(f"Failed to setup vector store: {e}")
            raise
    
    def load_documents(self, data_dir: str) -> List[Any]:
        """
        Load documents from directory.
        
        Args:
            data_dir: Directory containing documents (PDFs, text files, etc.)
            
        Returns:
            List of loaded documents
        """
        try:
            if not os.path.exists(data_dir):
                logger.warning(f"Data directory does not exist: {data_dir}")
                return []
            
            loader = SimpleDirectoryReader(
                input_dir=data_dir,
                recursive=True,
                required_exts=[".pdf", ".txt", ".md", ".json"]
            )
            
            documents = loader.load_data()
            logger.info(f"Loaded {len(documents)} documents from {data_dir}")
            
            return documents
            
        except Exception as e:
            logger.error(f"Failed to load documents from {data_dir}: {e}")
            raise
    
    def build_index(self, documents: Optional[List[Any]] = None, data_dir: Optional[str] = None):
        """
        Build or load vector store index.
        
        Args:
            documents: Pre-loaded documents
            data_dir: Directory to load documents from
        """
        try:
            # Check if index already exists
            if self._index_exists():
                logger.info("Loading existing index...")
                self.index = VectorStoreIndex.from_vector_store(
                    self.vector_store,
                    storage_context=self.storage_context
                )
            else:
                logger.info("Creating new index...")
                
                # Load documents if not provided
                if documents is None and data_dir is not None:
                    documents = self.load_documents(data_dir)
                elif documents is None:
                    logger.warning("No documents provided and no data_dir specified")
                    documents = []
                
                if documents:
                    self.index = VectorStoreIndex.from_documents(
                        documents,
                        storage_context=self.storage_context,
                        show_progress=True
                    )
                    logger.info(f"Created index with {len(documents)} documents")
                else:
                    # Create empty index
                    self.index = VectorStoreIndex(
                        nodes=[],
                        storage_context=self.storage_context
                    )
                    logger.info("Created empty index")
            
            # Create query engine
            self.query_engine = self.index.as_query_engine(
                similarity_top_k=5,
                response_mode="tree_summarize",
                verbose=True
            )
            
        except Exception as e:
            logger.error(f"Failed to build index: {e}")
            raise
    
    def _index_exists(self) -> bool:
        """Check if an index already exists in the vector store."""
        try:
            # Try to get collection info
            collection = self.vector_store._collection
            return collection.count() > 0
        except:
            return False
    
    def query(self, question: str, **kwargs) -> str:
        """
        Query the RAG system.
        
        Args:
            question: Natural language question
            **kwargs: Additional query parameters
            
        Returns:
            Generated response
        """
        if not self.query_engine:
            raise ValueError("Index not built. Call build_index() first.")
        
        try:
            response = self.query_engine.query(question, **kwargs)
            return str(response)
            
        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise
    
    def add_documents(self, documents: List[Any]):
        """Add new documents to existing index."""
        if not self.index:
            raise ValueError("Index not built. Call build_index() first.")
        
        try:
            for doc in documents:
                self.index.insert(doc)
            
            logger.info(f"Added {len(documents)} documents to index")
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise
    
    def get_query_engine_tool(self, name: str = "space_mission_rag", description: str = None) -> QueryEngineTool:
        """
        Create a QueryEngineTool for use with agents.
        
        Args:
            name: Tool name
            description: Tool description
            
        Returns:
            QueryEngineTool instance
        """
        if not self.query_engine:
            raise ValueError("Index not built. Call build_index() first.")
        
        if description is None:
            description = (
                "Use this tool to query space mission data, sensor telemetry, "
                "mission reports, and technical documentation. "
                "Provide detailed questions about specific missions, sensors, or procedures."
            )
        
        return QueryEngineTool.from_defaults(
            query_engine=self.query_engine,
            name=name,
            description=description
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the RAG system."""
        stats = {
            "index_exists": self.index is not None,
            "query_engine_exists": self.query_engine is not None,
            "persist_dir": self.persist_dir,
            "collection_name": self.collection_name,
            "llm_model": self.llm_model,
            "embedding_model": self.embedding_model
        }
        
        if self.vector_store:
            try:
                stats["document_count"] = self.vector_store._collection.count()
            except:
                stats["document_count"] = "unknown"
        
        return stats


def create_default_rag_system(data_dir: Optional[str] = None) -> SpaceMissionRAG:
    """
    Create a default RAG system instance.
    
    Args:
        data_dir: Optional directory containing documents to index
        
    Returns:
        Configured SpaceMissionRAG instance
    """
    # Use environment variables if available
    persist_dir = os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma_db")
    
    rag = SpaceMissionRAG(persist_dir=persist_dir)
    
    if data_dir:
        rag.build_index(data_dir=data_dir)
    else:
        rag.build_index()  # Create empty index
    
    return rag
