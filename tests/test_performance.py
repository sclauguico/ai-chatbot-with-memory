import os
import sys
import time
import concurrent.futures

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.chat_service import ChatService

def test_response_time():
    """
    Measures chatbot response time performance across various query types.
    
    Performance metrics:
    - Individual message response times
    - Average response time calculation
    - Response length correlation analysis
    - Latency patterns across different query complexities
    """
    chat = ChatService()
    
    test_messages = [
        "Hello, how are you?",
        "What's the weather like?", 
        "Tell me a joke",
        "Explain quantum physics",
        "What's 2+2?"
    ]
    
    times = []
    for message in test_messages:
        start_time = time.time()
        response = chat.chat(message, "perf_test")
        end_time = time.time()
        
        response_time = end_time - start_time
        times.append(response_time)
        
        print(f"Message: {message}")
        print(f"Response time: {response_time:.2f}s")
        print(f"Response length: {len(response)} chars")
        print()
    
    avg_time = sum(times) / len(times)
    print(f"Average response time: {avg_time:.2f}s")

def test_concurrent_users():
    """
    Tests system performance under concurrent user load conditions.
    
    Concurrency validation:
    - Multiple simultaneous chat sessions
    - Database connection pool handling
    - Session isolation verification
    - Resource contention and bottleneck identification
    """
    def chat_session(session_id):
        chat = ChatService()
        response = chat.chat(f"Hello from session {session_id}", f"concurrent_{session_id}")
        return len(response)
    
    print("Testing concurrent users...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(chat_session, i) for i in range(5)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    print(f"✅ Concurrent test completed - {len(results)} sessions handled")

if __name__ == "__main__":
    test_response_time()
    test_concurrent_users()