from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class AdvancedRetriever:
    def __init__(self, vector_store_manager, db_config):
        self.vector_store = vector_store_manager
        self.db_config = db_config
    
    def retrieve_context(self, query: str, k: int = 5) -> Dict:
        # Get similar documents
        docs = self.vector_store.similarity_search(query, k=k)
        
        # Organize by valid sources (tickets removed)
        context = {
            'knowledgebase': [],
            'projects': [],
            'all_docs': docs
        }
        
        for doc in docs:
            source = doc.metadata.get('source', 'unknown')
            
            if source in context:
                context[source].append(doc)
        
        return context
    


    def suggest_troubleshooting_steps(self, query: str, context: Dict) -> List[str]:
        """
        Generate troubleshooting suggestions based on knowledgebase + projects.
        Ticket-based suggestions are removed.
        """
        suggestions = []

        # Knowledge Base SOP suggestions
        sops = [
            doc for doc in context['knowledgebase']
            if doc.metadata.get('category') == 'sop'
        ]
        if sops:
            suggestions.append("Follow relevant SOP procedures")

        # Knowledge Base FAQ suggestions
        faqs = [
            doc for doc in context['knowledgebase']
            if doc.metadata.get('category') == 'faq'
        ]
        if faqs:
            suggestions.append("Check FAQ for common solutions")

        # Project information may give hints
        if context['projects']:
            suggestions.append("Review related project documentation")

        # Generic fallback suggestions
        if not suggestions:
            suggestions.extend([
                "Verify system configurations",
                "Check application logs for errors",
                "Test in an isolated environment",
                "Confirm environment variables",
                "Escalate to senior support if issue persists"
            ])

        return suggestions[:5]  # Top 5 suggestions
