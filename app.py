import os
import sys
from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import dateparser
import spacy
from datetime import datetime
from src.chat_endpoint import TravelChatbot

# Initialize Flask app with static folder configuration
app = Flask(__name__, 
    static_url_path='/static',
    static_folder='static',
    template_folder='templates'
)

# Load data files
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def load_json_file(filename, default=None):
    try:
        with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {filename} not found in data directory")
        return default or {}

def load_csv_file(filename):
    try:
        return pd.read_csv(os.path.join(DATA_DIR, filename))
    except FileNotFoundError:
        print(f"Warning: {filename} not found in data directory")
        return pd.DataFrame()

# Load data files
travel_intents = load_json_file('india_travel_intents.json', {"intents": []})
airports_df = load_csv_file('airports.csv')

# Initialize the chatbot with data
chatbot = TravelChatbot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        response = chatbot.process_message(user_message)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return jsonify({'response': f"I apologize, but I encountered an error. Please try again or rephrase your question."})

if __name__ == '__main__':
    app.run(debug=True)
