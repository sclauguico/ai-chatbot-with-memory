import os
from typing import Optional
from langchain_postgres import PostgresChatMessageHistory
from langchain_core.messages import BaseMessage
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.db_url = self._build_db_url()
        self.engine = create_engine(self.db_url)
        self._initialize_database()
    
    def _build_db_url(self) -> str:
        user = os.getenv('POSTGRES_USER', 'chatbot_user')
        password = os.getenv('POSTGRES_PASSWORD', 'your_secure_password')
        host = os.getenv('POSTGRES_HOST', 'localhost')
        port = os.getenv('POSTGRES_PORT', '5432')
        db = os.getenv('POSTGRES_DB', 'chatbot_db')
        
        return f"postgresql://{user}:{password}@{host}:{port}/{db}"
    
    def _initialize_database(self):
        """Initialize database tables if they don't exist"""
        try:
            with self.engine.connect() as conn:
                # Test connection
                conn.execute(text("SELECT 1"))
            print("Database connection successful")
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise
    
    def get_chat_history(self, session_id: str) -> PostgresChatMessageHistory:
        """Get chat history for a specific session"""
        return PostgresChatMessageHistory(
            connection_string=self.db_url,
            session_id=session_id,
            table_name="chat_history"
        )
    
    def clear_history(self, session_id: str):
        """Clear chat history for a specific session"""
        history = self.get_chat_history(session_id)
        history.clear()