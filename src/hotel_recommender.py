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
        """Initialize with comprehensive hotel data"""
        self.hotels_data = {
            'mumbai': [
                {
                    'name': 'Taj Palace',
                    'rating': 4.8,
                    'price': 15000,
                    'amenities': ['Pool', 'Spa', 'Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'The Oberoi',
                    'rating': 4.7,
                    'price': 12000,
                    'amenities': ['Pool', 'Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'Trident Nariman Point',
                    'rating': 4.5,
                    'price': 8000,
                    'amenities': ['Pool', 'Restaurant', 'Bar']
                },
                {
                    'name': 'ITC Grand Central',
                    'rating': 4.3,
                    'price': 6000,
                    'amenities': ['Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'Residency Hotel',
                    'rating': 3.8,
                    'price': 3500,
                    'amenities': ['Restaurant', 'WiFi']
                }
            ],
            'delhi': [
                {
                    'name': 'The Imperial',
                    'rating': 4.9,
                    'price': 20000,
                    'amenities': ['Pool', 'Spa', 'Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'The Leela Palace',
                    'rating': 4.8,
                    'price': 18000,
                    'amenities': ['Pool', 'Spa', 'Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'Taj Mahal Hotel',
                    'rating': 4.7,
                    'price': 15000,
                    'amenities': ['Pool', 'Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'The Metropolitan',
                    'rating': 4.2,
                    'price': 7000,
                    'amenities': ['Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'Hotel Palace Heights',
                    'rating': 3.9,
                    'price': 4000,
                    'amenities': ['Restaurant', 'WiFi']
                }
            ],
            'bangalore': [
                {
                    'name': 'The Ritz-Carlton',
                    'rating': 4.8,
                    'price': 18000,
                    'amenities': ['Pool', 'Spa', 'Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'ITC Gardenia',
                    'rating': 4.7,
                    'price': 15000,
                    'amenities': ['Pool', 'Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'Taj West End',
                    'rating': 4.6,
                    'price': 12000,
                    'amenities': ['Pool', 'Restaurant', 'Bar']
                },
                {
                    'name': 'Novotel',
                    'rating': 4.2,
                    'price': 7000,
                    'amenities': ['Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'Ginger Hotel',
                    'rating': 3.8,
                    'price': 3000,
                    'amenities': ['Restaurant', 'WiFi']
                }
            ],
            'chennai': [
                {
                    'name': 'ITC Grand Chola',
                    'rating': 4.8,
                    'price': 16000,
                    'amenities': ['Pool', 'Spa', 'Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'The Leela Palace',
                    'rating': 4.7,
                    'price': 14000,
                    'amenities': ['Pool', 'Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'Taj Coromandel',
                    'rating': 4.6,
                    'price': 12000,
                    'amenities': ['Pool', 'Restaurant', 'Bar']
                },
                {
                    'name': 'The Residency',
                    'rating': 4.1,
                    'price': 6000,
                    'amenities': ['Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'FabHotel Rr Inn',
                    'rating': 3.7,
                    'price': 2500,
                    'amenities': ['Restaurant', 'WiFi']
                }
            ],
            'hyderabad': [
                {
                    'name': 'Taj Falaknuma Palace',
                    'rating': 4.9,
                    'price': 25000,
                    'amenities': ['Pool', 'Spa', 'Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'ITC Kohenur',
                    'rating': 4.7,
                    'price': 15000,
                    'amenities': ['Pool', 'Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'Novotel HICC',
                    'rating': 4.4,
                    'price': 8000,
                    'amenities': ['Pool', 'Restaurant', 'Bar']
                },
                {
                    'name': 'Lemon Tree Premier',
                    'rating': 4.0,
                    'price': 5000,
                    'amenities': ['Restaurant', 'Bar', 'Gym']
                }
            ],
            'kolkata': [
                {
                    'name': 'ITC Royal Bengal',
                    'rating': 4.8,
                    'price': 15000,
                    'amenities': ['Pool', 'Spa', 'Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'The Oberoi Grand',
                    'rating': 4.7,
                    'price': 13000,
                    'amenities': ['Pool', 'Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'Taj Bengal',
                    'rating': 4.5,
                    'price': 10000,
                    'amenities': ['Pool', 'Restaurant', 'Bar']
                },
                {
                    'name': 'Novotel Kolkata',
                    'rating': 4.2,
                    'price': 6000,
                    'amenities': ['Restaurant', 'Bar', 'Gym']
                }
            ],
            'jaipur': [
                {
                    'name': 'Rambagh Palace',
                    'rating': 4.9,
                    'price': 30000,
                    'amenities': ['Pool', 'Spa', 'Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'ITC Rajputana',
                    'rating': 4.6,
                    'price': 12000,
                    'amenities': ['Pool', 'Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'Holiday Inn',
                    'rating': 4.2,
                    'price': 6000,
                    'amenities': ['Pool', 'Restaurant', 'Bar']
                },
                {
                    'name': 'Hotel Pearl Palace',
                    'rating': 4.0,
                    'price': 3000,
                    'amenities': ['Restaurant', 'WiFi']
                }
            ],
            'agra': [
                {
                    'name': 'The Oberoi Amarvilas',
                    'rating': 4.9,
                    'price': 35000,
                    'amenities': ['Pool', 'Spa', 'Restaurant', 'Bar', 'Gym', 'Taj View']
                },
                {
                    'name': 'ITC Mughal',
                    'rating': 4.6,
                    'price': 12000,
                    'amenities': ['Pool', 'Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'Crystal Sarovar',
                    'rating': 4.2,
                    'price': 6000,
                    'amenities': ['Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'Hotel Sidhartha',
                    'rating': 3.8,
                    'price': 2500,
                    'amenities': ['Restaurant', 'WiFi']
                }
            ],
            'varanasi': [
                {
                    'name': 'Taj Ganges',
                    'rating': 4.7,
                    'price': 12000,
                    'amenities': ['Pool', 'Spa', 'Restaurant', 'Bar', 'Gym']
                },
                {
                    'name': 'BrijRama Palace',
                    'rating': 4.6,
                    'price': 15000,
                    'amenities': ['Restaurant', 'Bar', 'Gym', 'River View']
                },
                {
                    'name': 'Ramada Plaza',
                    'rating': 4.2,
                    'price': 7000,
                    'amenities': ['Pool', 'Restaurant', 'Bar']
                },
                {
                    'name': 'Hotel Meraden Grand',
                    'rating': 4.0,
                    'price': 4000,
                    'amenities': ['Restaurant', 'WiFi']
                }
            ]
        }

    def get_hotels_by_city_and_budget(self, city: str, budget: float) -> list:
        """Get hotels in a city within the specified budget"""
        city = city.lower()
        if city not in self.hotels_data:
            return []

        hotels = [hotel for hotel in self.hotels_data[city] 
                 if hotel['price'] <= budget]
        
        if not hotels:
            min_price = min([h['price'] for h in self.hotels_data[city]])
            return [{'message': f'No hotels found within budget. Minimum price in {city.title()} is Rs. {min_price}'}]
        
        return sorted(hotels, key=lambda x: (-x['rating'], x['price']))

    def recommend_hotels(self, location: str, budget: float) -> str:
        """Get hotel recommendations based on location and budget"""
        try:
            # Validate inputs
            if not location or budget <= 0:
                return "Please provide a valid location and budget."
            
            # Get matching hotels
            hotels = self.get_hotels_by_city_and_budget(location, budget)
            
            if not hotels:
                return f"Sorry, I couldn't find any hotels in {location}. Please try another city."
            elif 'message' in hotels[0]:
                return hotels[0]['message']
            
            # Format response
            response = f"Available hotels in {location.title()} within your budget of Rs.{budget}:\n\n"
            
            for hotel in hotels:
                response += f"{hotel['name']}\n"
                response += f"Rating: {hotel['rating']}★\n"
                response += f"Price: Rs.{hotel['price']} per night\n"
                response += f"Amenities: {', '.join(hotel['amenities'])}\n\n"
            
            return response
            
        except Exception as e:
            print(f"Error in recommend_hotels: {str(e)}")
            return "Sorry, I encountered an error while searching for hotels. Please try again."

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