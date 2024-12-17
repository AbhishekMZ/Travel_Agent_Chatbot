class ChatUI {
    constructor() {
        this.chatContainer = document.getElementById('chatContainer');
        this.userInput = document.getElementById('userInput');
        this.sendButton = document.getElementById('sendButton');
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }

    addMessage(message, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.textContent = message;
        this.chatContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.id = 'typingIndicator';
        indicator.innerHTML = `
            <span></span>
            <span></span>
            <span></span>
        `;
        this.chatContainer.appendChild(indicator);
        this.scrollToBottom();
    }

    removeTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.remove();
        }
    }

    scrollToBottom() {
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }

    async sendMessage() {
        const message = this.userInput.value.trim();
        
        if (message) {
            // Clear input and add user message
            this.userInput.value = '';
            this.addMessage(message, true);
            
            // Show typing indicator
            this.showTypingIndicator();
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message }),
                });
                
                const data = await response.json();
                
                // Remove typing indicator and add bot response
                this.removeTypingIndicator();
                this.addMessage(data.response, false);
            } catch (error) {
                console.error('Error:', error);
                this.removeTypingIndicator();
                this.addMessage('Sorry, I encountered an error. Please try again.', false);
            }
        }
    }
}

// Initialize chat UI when document is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chatUI = new ChatUI();
});
