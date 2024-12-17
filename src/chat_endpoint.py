"""
Travel Chat Bot with Hotel Booking Suggestions
author: Enhanced version with hotel features
"""

import os
import json
import random 
import pandas as pd
import dateparser
import spacy
from datetime import datetime
import requests
from typing import Dict, List, Optional

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Load city and hotel data
with open('india_cities.json', 'r', encoding='utf-8') as f:
    CITIES_DATA = json.load(f)

with open('india_festivals.json', 'r', encoding='utf-8') as f:
    FESTIVALS_DATA = json.load(f)

class HotelRecommender:
    def __init__(self):
        with open('india_cities.json', 'r') as f:
            self.city_data = json.load(f)['cities']

    def get_hotels(self, city, budget='mid_range'):
        """Get hotel recommendations for a city based on budget category."""
        if city not in self.city_data:
            return None
        return self.city_data[city]['hotels'].get(budget, [])

    def get_nearby_attractions(self, city):
        """Get nearby attractions for a city."""
        if city not in self.city_data:
            return None
        return self.city_data[city]['attractions']

    def get_city_info(self, city):
        """Get comprehensive city information."""
        if city not in self.city_data:
            return None
        city_data = self.city_data[city]
        return {
            'best_time': city_data['best_time'],
            'weather': city_data['weather'],
            'transport': city_data['transport'],
            'local_food': city_data['local_food'],
            'specialties': city_data['specialties']
        }

class TravelChatbot:
    def __init__(self):
        self.hotel_recommender = HotelRecommender()
        self.context = {}
        
    def extract_travel_info(self, text: str) -> Dict:
        """Extract travel-related information from user input."""
        doc = nlp(text.lower())
        
        # Extract cities
        cities = []
        for city in self.hotel_recommender.city_data.keys():
            if city.lower() in text.lower():
                cities.append(city)
        
        # Extract budget preference
        budget_terms = {
            'luxury': ['luxury', 'five star', '5 star', 'premium'],
            'mid_range': ['mid range', 'moderate', 'three star', '3 star'],
            'budget': ['budget', 'cheap', 'affordable', 'hostel']
        }
        
        budget = 'mid_range'  # default
        for category, terms in budget_terms.items():
            if any(term in text.lower() for term in terms):
                budget = category
                break
        
        # Extract dates
        dates = []
        for ent in doc.ents:
            if ent.label_ == 'DATE':
                parsed_date = dateparser.parse(ent.text)
                if parsed_date:
                    dates.append(parsed_date)
        
        return {
            "cities": cities,
            "budget": budget,
            "dates": dates
        }
    
    def process_hotel_query(self, doc, hotel_recommender):
        """Process hotel-related queries."""
        ner_df = ner_doc(doc)
        cities = ner_df[ner_df['label'] == 'GPE']['text'].tolist()
        
        if not cities:
            return "Please specify a city for hotel recommendations."
        
        city = cities[0]
        budget = 'mid_range'  # default budget category
        
        # Check for budget preferences in the query
        text = doc.text.lower()
        if 'luxury' in text or '5 star' in text:
            budget = 'luxury'
        elif 'budget' in text or 'cheap' in text:
            budget = 'budget'
        
        hotels = hotel_recommender.get_hotels(city, budget)
        attractions = hotel_recommender.get_nearby_attractions(city)
        
        if not hotels:
            return f"Sorry, I couldn't find any {budget} hotels in {city}."
        
        response = f"Here are some {budget} hotels in {city}:\n"
        response += ", ".join(hotels[:5])  # Show top 5 hotels
        
        if attractions:
            response += f"\n\nNearby attractions: {', '.join(attractions[:3])}"
        
        return response

    def process_city_query(self, doc, hotel_recommender):
        """Process city information queries."""
        ner_df = ner_doc(doc)
        cities = ner_df[ner_df['label'] == 'GPE']['text'].tolist()
        
        if not cities:
            return "Please specify a city you'd like to know more about."
        
        city = cities[0]
        city_info = hotel_recommender.get_city_info(city)
        
        if not city_info:
            return f"Sorry, I don't have information about {city}."
        
        text = doc.text.lower()
        
        # Customize response based on query type
        if 'weather' in text or 'climate' in text:
            weather = city_info['weather']
            return f"Weather in {city}:\nSummer: {weather['summer']}\nMonsoon: {weather['monsoon']}\nWinter: {weather['winter']}\nBest time to visit: {city_info['best_time']}"
        elif 'food' in text or 'restaurant' in text:
            return f"Popular food spots in {city}: {', '.join(city_info['local_food'])}\nLocal specialties: {', '.join(city_info['specialties']['cuisine'])}"
        elif 'transport' in text or 'getting around' in text:
            return f"Transportation options in {city}: {', '.join(city_info['transport'])}"
        elif 'shopping' in text:
            return f"Popular shopping areas in {city}: {', '.join(city_info['specialties']['shopping'])}"
        else:
            # General city information
            return f"Welcome to {city}!\nBest time to visit: {city_info['best_time']}\nTop attractions: {', '.join(hotel_recommender.get_nearby_attractions(city)[:3])}\nLocal transport: {', '.join(city_info['transport'][:3])}\nDon't miss: {', '.join(city_info['specialties']['culture'][:2])}"

    def handle_message(self, text: str) -> str:
        """Main message handler."""
        doc = nlp(text.lower())
        
        if any(word in text.lower() for word in ['hotel', 'stay', 'room', 'accommodation']):
            return self.process_hotel_query(doc, self.hotel_recommender)
        elif any(word in text.lower() for word in ['city', 'information', 'info']):
            return self.process_city_query(doc, self.hotel_recommender)
        
        # Handle other types of queries (can be expanded)
        return "I can help you find hotels and accommodations. Please ask about hotels in any major Indian city!"

# Initialize the chatbot
chatbot = TravelChatbot()

def get_response(text: str) -> str:
    """Get response from chatbot."""
    return chatbot.handle_message(text)

if __name__ == "__main__":
    # Example usage
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            break
        response = get_response(user_input)
        print(f"Bot: {response}")