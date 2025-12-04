import os
from dotenv import load_dotenv
from config.database import DatabaseConfig
from src.data_loader import DataLoader
from src.vector_store import VectorStoreManager
from src.retriever import AdvancedRetriever   
from src.chatbot import SupportChatbot

def initialize_system(force_reload=False):
    """Initialize all system components"""
    print("="*60)
    print("AI Support Assistant - Initialization")
    print("="*60)
    
    # Load environment variables
    load_dotenv()
    
    # 1. Database connection
    db_config = DatabaseConfig()
    if not db_config.test_connection():
        raise Exception("Database connection failed")
    
    # 2. Vector store (KB + Projects only)
    embedding_model = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    vector_store = VectorStoreManager(embedding_model)
    
    # 3. Try to load existing vector store
    if not force_reload and vector_store.load_vector_store():
        print("Using existing vector store")
    else:
        print("Creating new vector store...")
        data_loader = DataLoader(db_config)
        
        # This must return ONLY KB + Projects
        all_documents = data_loader.load_all_data()  
        
        # Create vector embeddings
        vector_store.create_vector_store(all_documents)
        
        # Save for future use
        vector_store.save_vector_store()
    
    retriever = AdvancedRetriever(vector_store, db_config)  
    
    model_name = os.getenv('OLLAMA_MODEL', 'llama3.1')
    chatbot = SupportChatbot(retriever, model_name)
    
    # print("\n✓ All components initialized successfully!")
    return chatbot

def main():
    """Main application entry point"""
    try:
        # Check if we should force reload data
        import sys
        force_reload = '--reload' in sys.argv
        
        if force_reload:
            print("\n⚠️  Force reload enabled - rebuilding vector store...\n")
        
        # Initialize system
        chatbot = initialize_system(force_reload=force_reload)
        
        # Start interactive chat
        chatbot.chat()
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye! 👋")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()





