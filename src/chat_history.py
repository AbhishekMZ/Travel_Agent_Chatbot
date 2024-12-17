from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class ChatMessage:
    message: str
    sender: str
    timestamp: datetime = datetime.now()

class ChatHistory:
    def __init__(self):
        self.messages: List[ChatMessage] = []
        self.current_context = {
            'destination': None,
            'date': None,
            'budget': None,
            'pending_info': None
        }

    def add_message(self, message: str, sender: str):
        """Add a message to the history"""
        self.messages.append(ChatMessage(message=message, sender=sender))

    def reset(self):
        """Reset the conversation context"""
        self.current_context = {
            'destination': None,
            'date': None,
            'budget': None,
            'pending_info': None
        }
        # Clear message history
        self.messages = []

    def start_over(self):
        """Start a new conversation by resetting context and history"""
        self.reset()
        # Set pending_info to destination to prompt for new destination
        self.current_context['pending_info'] = 'destination'
        return "Let's start a new search! Where would you like to travel?"

    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation"""
        if not self.current_context['destination']:
            return "No active search in progress."
        
        summary = f"Current search:\n- Destination: {self.current_context['destination']}"
        if self.current_context['date']:
            summary += f"\n- Date: {self.current_context['date']}"
        if self.current_context['budget']:
            summary += f"\n- Budget: Rs. {self.current_context['budget']}"
        return summary
