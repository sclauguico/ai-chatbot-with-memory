import streamlit as st
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.chat_service import ChatService

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

def initialize_chat_service():
    """Initialize chat service with error handling"""
    try:
        return ChatService()
    except Exception as e:
        st.error(f"Failed to initialize chat service: {e}")
        st.stop()

def main():
    st.title("🤖 AI Chatbot with Memory")
    st.write("Chat with an AI assistant powered by local LLM and persistent memory")
    
    # Initialize chat service
    if 'chat_service' not in st.session_state:
        st.session_state.chat_service = initialize_chat_service()
    
    # Initialize session state for messages
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        # Load existing history
        try:
            history = st.session_state.chat_service.get_chat_history()
            for human_msg, ai_msg in history:
                st.session_state.messages.append({"role": "user", "content": human_msg})
                st.session_state.messages.append({"role": "assistant", "content": ai_msg})
        except Exception as e:
            st.warning(f"Could not load chat history: {e}")
    
    # Sidebar with controls
    with st.sidebar:
        st.header("Chat Controls")
        
        if st.button("Clear Chat History", type="secondary"):
            try:
                st.session_state.chat_service.clear_history()
                st.session_state.messages = []
                st.success("Chat history cleared!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to clear history: {e}")
        
        st.divider()
        st.subheader("System Status")
        
        # Check system status
        try:
            # Test database connection
            st.session_state.chat_service.db_manager.get_chat_history("test")
            st.success("✅ Database connected")
        except:
            st.error("❌ Database connection failed")
        
        st.info("💡 Ollama service required for AI responses")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.chat_service.chat(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()