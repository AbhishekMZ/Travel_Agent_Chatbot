from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import dateparser
import spacy
from datetime import datetime
import os

app = Flask(__name__)

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Load travel intents
with open('travel_intents.json', 'r') as f:
    travel_intents = json.load(f)

# Load airports data
airports_df = pd.read_csv('airports.csv')

def process_message(user_message):
    doc = nlp(user_message.lower())
    
    # Basic intent matching
    for intent in travel_intents['intents']:
        for pattern in intent['patterns']:
            if pattern.lower() in user_message.lower():
                return random.choice(intent['responses'])
    
    # Default response
    return "I'm sorry, I didn't quite understand that. Could you please rephrase your question about travel?"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    response = process_message(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
