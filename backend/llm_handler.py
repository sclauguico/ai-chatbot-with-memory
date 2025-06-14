import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class OllamaLLM:
   """
   Handles communication with Ollama LLM API.
   
   Features:
   - Health checking and model verification
   - Prompt formatting and context management
   - Error handling and timeout management
   - Configurable model parameters
   """
   
   def __init__(self):
       self.base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
       self.model_name = os.getenv('MODEL_NAME', 'llama2:7b-chat')
       self._check_ollama_connection()
   
   def _check_ollama_connection(self):
       """Check if Ollama is running and model is available"""
       try:
           response = requests.get(f"{self.base_url}/api/tags")
           if response.status_code == 200:
               models = [model['name'] for model in response.json().get('models', [])]
               if self.model_name not in models:
                   print(f"Warning: Model {self.model_name} not found. Available models: {models}")
               else:
                   print(f"Ollama connected successfully. Using model: {self.model_name}")
           else:
               print("Warning: Could not connect to Ollama")
       except Exception as e:
           print(f"Warning: Ollama connection check failed: {e}")
   
   def _format_prompt(self, prompt: str, context: str) -> str:
       """Format prompt with conversation context"""
       if context and len(context.strip()) > 0:
           return f"""You are a helpful AI assistant. Here is our previous conversation:

            {context}

            Based on our conversation history above, please respond to: {prompt}

            Remember to use information from our previous conversation when relevant."""
       else:
           return f"You are a helpful AI assistant.\n\nHuman: {prompt}\n\nAssistant:"
   
   def generate_response(self, prompt: str, context: str = "") -> str:
       """
       Generate response using Ollama API.
       
       Args:
           prompt: User input message
           context: Previous conversation context
           
       Returns:
           Generated response string
       """
       full_prompt = self._format_prompt(prompt, context)
       
       payload = {
           "model": self.model_name,
           "prompt": full_prompt,
           "stream": False,
           "options": {
               "temperature": 0.7,
               "max_tokens": 500,
           }
       }
       
       try:
           response = requests.post(
               f"{self.base_url}/api/generate",
               json=payload,
               timeout=30
           )
           
           if response.status_code == 200:
               return response.json().get('response', 'Sorry, I could not generate a response.')
           else:
               return f"Error: Could not connect to LLM (Status: {response.status_code})"
               
       except requests.exceptions.RequestException as e:
           return f"Error: Connection to LLM failed - {str(e)}"