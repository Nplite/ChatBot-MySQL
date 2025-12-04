from sqlalchemy import text
from typing import List, Dict
import json

class DataLoader:
    def __init__(self, db_config):
        self.db_config = db_config
    
    def load_knowledgebase(self) -> List[Dict]:
        """Load all knowledge base articles"""
        query = """
        SELECT id, title, content, category, tags, 
               DATE_FORMAT(created_at, '%Y-%m-%d') as created_date
        FROM knowledgebase
        """
        
        with self.db_config.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()
            
            documents = []
            for row in rows:
                doc = {
                    'id': row[0],
                    'title': row[1],
                    'content': row[2],
                    'category': row[3],
                    'tags': row[4],
                    'created_date': row[5],
                    'source': 'knowledgebase',
                    'text': f"Title: {row[1]}\nCategory: {row[3]}\n\n{row[2]}"
                }
                documents.append(doc)
            
            return documents
    
    def load_projects(self) -> List[Dict]:
        """Load all project information"""
        query = """
        SELECT id, project_name, description, tech_stack, 
               status, DATE_FORMAT(start_date, '%Y-%m-%d') as start_date,
               metadata
        FROM projects
        """
        
        with self.db_config.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()
            
            documents = []
            for row in rows:
                metadata_json = row[6] if row[6] else '{}'
                doc = {
                    'id': row[0],
                    'project_name': row[1],
                    'description': row[2],
                    'tech_stack': row[3],
                    'status': row[4],
                    'start_date': row[5],
                    'metadata': metadata_json,
                    'source': 'projects',
                    'text': f"Project: {row[1]}\nStatus: {row[4]}\nTech Stack: {row[3]}\n\nDescription: {row[2]}"
                }
                documents.append(doc)
            
            return documents

    def load_all_data(self) -> List[Dict]:
        """Load all data from all sources"""
        print("Loading knowledge base...")
        kb_docs = self.load_knowledgebase()
        print(f"✓ Loaded {len(kb_docs)} knowledge base articles")
        
        print("Loading projects...")
        project_docs = self.load_projects()
        print(f"✓ Loaded {len(project_docs)} projects")
        
        # print("Loading tickets...")
        # ticket_docs = self.load_tickets()
        # print(f"✓ Loaded {len(ticket_docs)} tickets")
        
        all_docs = kb_docs + project_docs # + ticket_docs
        print(f"\n✓ Total documents loaded: {len(all_docs)}")
        
        return all_docs
    