"""
Conversation history management module.
Includes session management for saving/loading conversations.
"""

from typing import List, Dict, Tuple, Optional
import json
import os
from datetime import datetime


class ConversationManager:
    def __init__(self, session_id: Optional[str] = None):
        self.history: List[Dict[str, str]] = []
        self.session_id = session_id or self._generate_session_id()
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def add_message(self, role: str, content: str):
        if role not in ['user', 'assistant']:
            raise ValueError("Role must be 'user' or 'assistant'")
        
        self.history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        self.updated_at = datetime.now().isoformat()
    
    def get_history(self) -> List[Dict[str, str]]:
        return self.history.copy()
    
    def format_for_sentiment(self) -> str:
        if not self.history:
            return ""
        
        formatted_lines = []
        for msg in self.history:
            role_label = "User" if msg['role'] == 'user' else "Chatbot"
            formatted_lines.append(f"{role_label}: {msg['content']}")
        
        return "\n".join(formatted_lines)
    
    def get_conversation_text(self) -> str:
        user_messages = [msg['content'] for msg in self.history if msg['role'] == 'user']
        return " ".join(user_messages)
    
    def clear(self):
        self.history = []
    
    def get_message_count(self) -> int:
        return len(self.history)
    
    def get_user_message_count(self) -> int:
        return len([msg for msg in self.history if msg['role'] == 'user'])
    
    def get_user_messages(self) -> List[str]:
        return [msg['content'] for msg in self.history if msg['role'] == 'user']
    
    def is_empty(self) -> bool:
        return len(self.history) == 0
    
    def _generate_session_id(self) -> str:
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def save_to_file(self, filepath: Optional[str] = None) -> str:
        if filepath is None:
            os.makedirs('saved_conversations', exist_ok=True)
            filepath = f"saved_conversations/{self.session_id}.json"
        
        data = {
            'session_id': self.session_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'history': self.history
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'ConversationManager':
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        manager = cls(session_id=data.get('session_id'))
        manager.created_at = data.get('created_at', datetime.now().isoformat())
        manager.updated_at = data.get('updated_at', datetime.now().isoformat())
        manager.history = data.get('history', [])
        
        return manager
    
    @classmethod
    def list_saved_sessions(cls, directory: str = 'saved_conversations') -> List[Dict[str, str]]:
        if not os.path.exists(directory):
            return []
        
        sessions = []
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                filepath = os.path.join(directory, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    sessions.append({
                        'session_id': data.get('session_id', filename),
                        'filepath': filepath,
                        'created_at': data.get('created_at', 'Unknown'),
                        'updated_at': data.get('updated_at', 'Unknown'),
                        'message_count': len(data.get('history', []))
                    })
                except Exception:
                    continue
        
        return sorted(sessions, key=lambda x: x['updated_at'], reverse=True)
    
    def to_dict(self) -> Dict:
        return {
            'session_id': self.session_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'history': self.history
        }

