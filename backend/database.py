import os
import uuid
from typing import Optional
from langchain_postgres import PostgresChatMessageHistory
from langchain_core.messages import BaseMessage
from sqlalchemy import create_engine, text
import psycopg
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.db_url = self._build_db_url()
        self.engine = create_engine(self.db_url)
        self._initialize_database()
        self._create_chat_history_table()
    
    def _build_db_url(self) -> str:
        user = os.getenv('POSTGRES_USER', 'chatbot_user')
        password = os.getenv('POSTGRES_PASSWORD', 'chatbot_password')
        host = os.getenv('POSTGRES_HOST', 'localhost')
        port = os.getenv('POSTGRES_PORT', '5434')
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
    
    def _create_chat_history_table(self):
        """Create the chat_history table if it doesn't exist"""
        try:
            # Create a temporary PostgresChatMessageHistory to initialize the table
            temp_connection = psycopg.connect(self.db_url)
            temp_uuid = str(uuid.uuid4())
            
            # This will create the table automatically
            temp_history = PostgresChatMessageHistory(
                "chat_history",
                temp_uuid,
                sync_connection=temp_connection
            )
            
            # Close the temporary connection
            temp_connection.close()
            print("Chat history table initialized")
            
        except Exception as e:
            print(f"Error creating chat history table: {e}")
    
    def _ensure_valid_uuid(self, session_id: str) -> str:
        """Convert session_id to valid UUID format"""
        try:
            # Try to parse as UUID
            uuid.UUID(session_id)
            return session_id
        except ValueError:
            # Create a deterministic UUID from the string
            namespace = uuid.NAMESPACE_DNS
            return str(uuid.uuid5(namespace, session_id))
    
    def get_chat_history(self, session_id: str) -> PostgresChatMessageHistory:
        """Get chat history for a specific session"""
        # Convert to valid UUID
        valid_session_id = self._ensure_valid_uuid(session_id)
        
        # Create psycopg connection
        connection = psycopg.connect(self.db_url)
        
        return PostgresChatMessageHistory(
            "chat_history",  # table_name as first positional argument
            valid_session_id,      # session_id as UUID
            sync_connection=connection
        )
    
    def clear_history(self, session_id: str):
        """Clear chat history for a specific session"""
        history = self.get_chat_history(session_id)
        history.clear()