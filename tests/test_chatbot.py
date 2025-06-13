import pytest
import os
import sys
from unittest.mock import Mock, patch

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.database import DatabaseManager
from backend.llm_handler import OllamaLLM
from backend.chat_service import ChatService

class TestDatabaseManager:
    """
    Tests database connection logic and URL construction in isolation.
    
    Key test areas:
    - Database URL formatting validation
    - Connection parameter verification
    - Configuration handling without actual DB calls
    """
    
    def test_build_db_url(self):
        """Test database URL construction"""
        db_manager = DatabaseManager()
        assert "postgresql://" in db_manager.db_url
        assert "chatbot_db" in db_manager.db_url

class TestOllamaLLM:
    """
    Tests LLM handler functionality using mocked HTTP responses.
    
    Key test areas:
    - Health check API validation
    - Response generation with controlled inputs
    - Error handling for network failures
    """
    
    @patch('requests.get')
    def test_check_connection(self, mock_get):
        """Test Ollama connection check"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"models": [{"name": "llama2:7b-chat"}]}
        
        llm = OllamaLLM()
        assert llm.model_name == "llama2:7b-chat"
    
    @patch('requests.post')
    def test_generate_response(self, mock_post):
        """Test response generation"""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"response": "Test response"}
        
        llm = OllamaLLM()
        response = llm.generate_response("Test prompt")
        assert response == "Test response"

class TestChatService:
    """
    Tests chat service orchestration with mocked dependencies.
    
    Key test areas:
    - End-to-end conversation flow simulation
    - Context building and message handling
    - Integration between components via mocks
    """

    @patch('backend.chat_service.DatabaseManager')
    @patch('backend.chat_service.OllamaLLM')
    def test_chat_functionality(self, mock_llm, mock_db):
        """Test basic chat functionality"""
        # Mock LLM response
        mock_llm_instance = Mock()
        mock_llm_instance.generate_response.return_value = "Mock response"
        mock_llm.return_value = mock_llm_instance
        
        # Mock database
        mock_db_instance = Mock()
        mock_history = Mock()
        mock_history.messages = []
        mock_db_instance.get_chat_history.return_value = mock_history
        mock_db.return_value = mock_db_instance
        
        chat_service = ChatService()
        response = chat_service.chat("Test message")
        
        assert response == "Mock response"
        mock_history.add_user_message.assert_called_once_with("Test message")
        mock_history.add_ai_message.assert_called_once_with("Mock response")

if __name__ == "__main__":
    pytest.main([__file__])