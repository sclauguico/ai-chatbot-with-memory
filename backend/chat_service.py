from typing import List, Tuple
from langchain_core.messages import HumanMessage, AIMessage
from .database import DatabaseManager
from .llm_handler import OllamaLLM

class ChatService:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.llm = OllamaLLM()
    
    def get_conversation_context(self, session_id: str, max_messages: int = 10) -> str:
        """Get recent conversation context"""
        history = self.db_manager.get_chat_history(session_id)
        messages = history.messages[-max_messages:] if len(history.messages) > max_messages else history.messages
        
        context = ""
        for message in messages:
            if isinstance(message, HumanMessage):
                context += f"Human: {message.content}\n"
            elif isinstance(message, AIMessage):
                context += f"Assistant: {message.content}\n"
        
        return context
    
    def chat(self, message: str, session_id: str = "default") -> str:
        """Process chat message and return response"""
        # Get conversation context
        context = self.get_conversation_context(session_id)
        
        # Generate response
        response = self.llm.generate_response(message, context)
        
        # Save to database
        history = self.db_manager.get_chat_history(session_id)
        history.add_user_message(message)
        history.add_ai_message(response)
        
        return response
    
    def get_chat_history(self, session_id: str = "default") -> List[Tuple[str, str]]:
        """Get chat history as list of (human_message, ai_response) tuples"""
        history = self.db_manager.get_chat_history(session_id)
        
        chat_pairs = []
        messages = history.messages
        
        for i in range(0, len(messages) - 1, 2):
            if (i + 1 < len(messages) and 
                isinstance(messages[i], HumanMessage) and 
                isinstance(messages[i + 1], AIMessage)):
                chat_pairs.append((messages[i].content, messages[i + 1].content))
        
        return chat_pairs
    
    def clear_history(self, session_id: str = "default"):
        """Clear chat history for session"""
        self.db_manager.clear_history(session_id)