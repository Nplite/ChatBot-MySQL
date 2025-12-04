
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class DatabaseConfig:
    def __init__(self):
        self.host = os.getenv('MYSQL_HOST', 'localhost')
        self.port = os.getenv('MYSQL_PORT', '3306')
        self.user = os.getenv('MYSQL_USER')
        self.password = os.getenv('MYSQL_PASSWORD')
        self.database = os.getenv('MYSQL_DATABASE')
        
        # URL encode password to handle special characters
        encoded_password = quote_plus(self.password)
        
        self.connection_string = (
            f"mysql+pymysql://{self.user}:{encoded_password}@"
            f"{self.host}:{self.port}/{self.database}"
        )
        
        self.engine = create_engine(
            self.connection_string,
            pool_pre_ping=True,
            pool_recycle=3600
        )
        
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
    
    def get_session(self):
        return self.SessionLocal()
    
    def test_connection(self):
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("✓ Database connection successful")
                return True
        except Exception as e:
            print(f"✗ Database connection failed: {e}")
            return False