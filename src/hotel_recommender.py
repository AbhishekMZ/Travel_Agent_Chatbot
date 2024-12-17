import spacy
import requests
from typing import Dict, List, Any
import os
import json

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

class Hotel:
    def __init__(self, name: str, rating: float, price: float, location: str, category: str):
        self.name = name
        self.rating = rating
        self.price = price
        self.location = location
        self.category = category

    def __str__(self):
        return f"{self.name} ({self.rating}★) - Rs.{self.price:.2f} per night"

class HotelRecommender:
    def __init__(self):
        """Initialize with mock hotel data"""
        self.mock_hotels = [
            {
                'name': 'Taj Palace',
                'location': 'mumbai',
                'rating': 4.8,
                'price': 15000,
                'amenities': ['Pool', 'Spa', 'Restaurant', 'Bar', 'Gym']
            },
            {
                'name': 'The Oberoi',
                'location': 'mumbai',
                'rating': 4.7,
                'price': 12000,
                'amenities': ['Pool', 'Restaurant', 'Bar', 'Gym']
            },
            {
                'name': 'Trident Nariman Point',
                'location': 'mumbai',
                'rating': 4.5,
                'price': 8000,
                'amenities': ['Pool', 'Restaurant', 'Bar']
            },
            {
                'name': 'ITC Grand Central',
                'location': 'mumbai',
                'rating': 4.3,
                'price': 6000,
                'amenities': ['Restaurant', 'Bar', 'Gym']
            },
            {
                'name': 'Taj Mahal Palace',
                'location': 'delhi',
                'rating': 4.9,
                'price': 20000,
                'amenities': ['Pool', 'Spa', 'Restaurant', 'Bar', 'Gym']
            },
            {
                'name': 'The Imperial',
                'location': 'delhi',
                'rating': 4.7,
                'price': 15000,
                'amenities': ['Pool', 'Restaurant', 'Bar', 'Gym']
            },
            {
                'name': 'The Leela Palace',
                'location': 'delhi',
                'rating': 4.6,
                'price': 12000,
                'amenities': ['Pool', 'Restaurant', 'Bar']
            },
            {
                'name': 'ITC Maurya',
                'location': 'delhi',
                'rating': 4.4,
                'price': 8000,
                'amenities': ['Restaurant', 'Bar', 'Gym']
            }
        ]

    def recommend_hotels(self, location: str, budget: float) -> str:
        """Get hotel recommendations based on location and budget"""
        try:
            # Validate inputs
            if not location or budget <= 0:
                return "Please provide a valid location and budget."
            
            # Filter hotels based on criteria
            matching_hotels = self._filter_hotels(location, budget)
            
            if not matching_hotels:
                min_price = min([h['price'] for h in self.mock_hotels if h['location'].lower() == location.lower()], default=0)
                if min_price > 0:
                    return f"Sorry, I couldn't find any hotels in {location} within your budget of Rs.{budget}. The minimum price for hotels in {location} starts from Rs.{min_price}."
                return f"Sorry, I couldn't find any hotels in {location}. Please try another city."
            
            # Format response
            response = f"Available hotels in {location} within your budget of Rs.{budget}:\n\n"
            
            for hotel in matching_hotels:
                response += f" {hotel['name']}\n"
                response += f"   Rating: {int(hotel['rating']) * '*'} ({hotel['rating']})\n"
                response += f"   Price: Rs.{hotel['price']} per night\n"
                response += f"   Amenities: {', '.join(hotel['amenities'])}\n\n"
            
            return response
            
        except Exception as e:
            print(f"Error in recommend_hotels: {str(e)}")
            return "Sorry, I encountered an error while searching for hotels. Please try again."

    def _filter_hotels(self, location: str, budget: float) -> List[Dict[str, Any]]:
        """Filter hotels based on criteria"""
        # In a real implementation, this would query a hotel database
        # For now, filter mock data by budget and location
        return [hotel for hotel in self.mock_hotels 
                if hotel['price'] <= budget and hotel['location'].lower() == location.lower()]

    def get_hotels_by_city_and_budget(self, city: str, budget: float) -> list:
        """Get hotels in a city within the specified budget"""
        city = city.lower()
        hotels = [hotel for hotel in self.mock_hotels 
                 if hotel['location'].lower() == city and hotel['price'] <= budget]
        
        if not hotels:
            min_price = float('inf')
            for hotel in self.mock_hotels:
                if hotel['location'].lower() == city and hotel['price'] < min_price:
                    min_price = hotel['price']
            
            if min_price == float('inf'):
                return []  # No hotels found in this city
            else:
                return [{'message': f'No hotels found within budget. Minimum price in {city} is Rs. {min_price}'}]
        
        return sorted(hotels, key=lambda x: x['price'])

class TravelChatbot:
    def __init__(self):
        self.hotel_recommender = HotelRecommender()
        self.context = {
            'current_city': None,
            'destination_city': None,
            'travel_date': None,
            'budget': None,
            'last_intent': None,
            'chat_history': [],
            'pending_question': None
        }