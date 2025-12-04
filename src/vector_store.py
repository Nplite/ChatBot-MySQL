from langchain_community.embeddings import HuggingFaceEmbeddings 
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from typing import List, Dict
import torch
import os




class VectorStoreManager:
    def __init__(self, embedding_model: str):
        print(f"Initializing embeddings model: {embedding_model}")

        device = "cuda" if torch.cuda.is_available() else "cpu"

        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={
                "device": device,
                "trust_remote_code": True  # REQUIRED for EmbeddingGemma
            },
            encode_kwargs={
                "normalize_embeddings": True
            }
        )

        self.vector_store = None
        self.persist_directory = "vector_db"
    
    def create_vector_store(self, documents: List[Dict]) -> None:
        """
        Create vector store from documents.
        NOTE: Ticket-related documents should NOT be included.
        Only knowledgebase + projects should be processed.
        """
        print("\nCreating vector embeddings...")

        langchain_docs = []
        
        for doc in documents:
            # Skip ticket entries if present
            if doc.get("type") == "ticket":
                # Comment: Tickets are intentionally excluded
                continue
            
            langchain_doc = Document(
                page_content=doc['text'],
                metadata={k: v for k, v in doc.items() if k != 'text'}
            )

            # langchain_doc = Document(
            #     page_content=doc['text'],
            #     metadata={
            #         'id': doc.get('id'),
            #         'source': doc.get('source'),
            #         'title': doc.get('title') or doc.get('project_name')
            #     }
            # )

            langchain_docs.append(langchain_doc)
        
        # Create FAISS vector store
        self.vector_store = FAISS.from_documents(
            langchain_docs,
            self.embeddings
        )
        
        print(f"✓ Vector store created with {len(langchain_docs)} documents (tickets excluded)")
    
    def save_vector_store(self) -> None:
        """Save vector store to disk"""
        if self.vector_store:
            os.makedirs(self.persist_directory, exist_ok=True)
            self.vector_store.save_local(self.persist_directory)
            print(f"✓ Vector store saved to {self.persist_directory}")
    
    def load_vector_store(self) -> bool:
        """Load vector store from disk"""
        try:
            if os.path.exists(self.persist_directory):
                self.vector_store = FAISS.load_local(
                    self.persist_directory,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                print(f"✓ Vector store loaded from {self.persist_directory}")
                return True
            return False
        except Exception as e:
            print(f"✗ Failed to load vector store: {e}")
            return False
    
    def similarity_search(self, query: str, k: int = 5, filter_dict: Dict = None) -> List[Document]:
        """
        Search for similar documents.
        This will NEVER return ticket documents because they are not stored.
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        
        if filter_dict:
            results = self.vector_store.similarity_search(
                query,
                k=k,
                filter=filter_dict
            )
        else:
            results = self.vector_store.similarity_search(query, k=k)
        
        return results
    
    def get_retriever(self, k: int = 5):
        """
        Get a retriever object for the vector store.
        Again, no ticket documents exist here.
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        
        return self.vector_store.as_retriever(
            search_kwargs={"k": k}
        )
