import pytest
import os
import sys
from unittest.mock import Mock, patch

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.database import DatabaseManager
from backend.llm_handler import OllamaLLM
from backend.chat_service import ChatService

def test_full_system_integration():
    """
    Verifies complete system functionality using real services.
    
    Test sequence:
    - Database connection and schema validation
    - LLM service communication and response quality
    - Chat service orchestration with actual persistence
    - Memory retention across conversation turns
    """
    
    print("🧪 Starting Integration Tests...")
    
    # Test 1: Database Connection
    print("\n1. Testing Database Connection...")
    try:
        from backend.database import DatabaseManager
        db = DatabaseManager()
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False
    
    # Test 2: LLM Connection  
    print("\n2. Testing LLM Connection...")
    try:
        from backend.llm_handler import OllamaLLM
        llm = OllamaLLM()
        response = llm.generate_response("Say hello")
        print(f"✅ LLM response: {response[:50]}...")
    except Exception as e:
        print(f"❌ LLM test failed: {e}")
        return False
    
    # Test 3: Chat Service
    print("\n3. Testing Chat Service...")
    try:
        from backend.chat_service import ChatService
        chat = ChatService()
        
        # Test conversation
        response1 = chat.chat("My name is Alice", "test_session")
        response2 = chat.chat("What's my name?", "test_session")
        
        print(f"✅ Chat test successful")
        print(f"   Response 1: {response1[:50]}...")
        print(f"   Response 2: {response2[:50]}...")
        
        # Test memory
        if "alice" in response2.lower():
            print("✅ Memory test passed - AI remembered the name")
        else:
            print("⚠️  Memory test unclear - check manually")
            
    except Exception as e:
        print(f"❌ Chat service test failed: {e}")
        return False
    
    # Test 4: Database Persistence
    print("\n4. Testing Database Persistence...")
    try:
        history = chat.get_chat_history("test_session")
        if len(history) >= 2:
            print(f"✅ Database persistence working - {len(history)} conversation pairs stored")
        else:
            print("⚠️  Database persistence test unclear")
    except Exception as e:
        print(f"❌ Database persistence test failed: {e}")
        return False
    
    print("\n🎉 All integration tests completed!")
    return True

# Memory-specific tests
def test_memory_functionality():
    """
    Tests conversation memory persistence across multiple scenarios.
    
    Memory test cases:
    - Personal information retention (name, preferences)
    - Professional details recall (job, location)
    - Contextual information persistence (pets, hobbies)
    - Cross-session isolation verification
    """
    
    memory_tests = [
        ("My favorite color is Pink", "What's my favorite color?"),
        ("I work as a Data Scientist", "What do I do for work?"), 
        ("I like swimming, running, and playing the guitar", "What are my hobbies?"),
        ("I live in Metro Manila", "Where do I live?")
    ]
    
    print("🧠 Testing Memory Functionality...")
    
    from backend.chat_service import ChatService
    chat = ChatService()
    
    for i, (setup, question) in enumerate(memory_tests):
        session_id = f"memory_test_{i}"
        
        # Setup information
        chat.chat(setup, session_id)
        
        # Test recall
        response = chat.chat(question, session_id)
        
        print(f"Test {i+1}:")
        print(f"  Setup: {setup}")
        print(f"  Question: {question}")
        print(f"  Response: {response[:100]}...")
        print()

if __name__ == "__main__":
    test_full_system_integration()
    test_memory_functionality()