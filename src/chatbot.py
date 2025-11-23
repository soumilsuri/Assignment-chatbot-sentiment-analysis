"""
Chatbot module using Google Gemini API.
"""

import google.generativeai as genai
from typing import List, Dict, Optional
from src.utils import get_api_key


class Chatbot:
    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = get_api_key('GEMINI_API_KEY')
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.chat = None
    
    def start_conversation(self):
        self.chat = self.model.start_chat(history=[])
    
    def get_response(self, user_message: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        try:
            if conversation_history and len(conversation_history) > 1:
                history = []
                for msg in conversation_history[:-1]:
                    if msg['role'] == 'user':
                        history.append({'role': 'user', 'parts': [msg['content']]})
                    elif msg['role'] == 'assistant':
                        history.append({'role': 'model', 'parts': [msg['content']]})
                
                self.chat = self.model.start_chat(history=history)
            elif self.chat is None:
                self.start_conversation()
            
            response = self.chat.send_message(user_message)
            return response.text
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            return f"I apologize, but I encountered an error. {error_msg}. Please try again."
    
    def reset(self):
        self.chat = None

