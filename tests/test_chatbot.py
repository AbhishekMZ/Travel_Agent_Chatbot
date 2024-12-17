import sys
import os
import unittest
from datetime import datetime

# Add the src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chat_endpoint import TravelChatbot
from src.hotel_recommender import HotelRecommender
from src.flight_service import FlightService

class TestTravelChatbot(unittest.TestCase):
    def setUp(self):
        self.chatbot = TravelChatbot()
        self.expected_responses = {
            'greeting': [
                "Hello!", "travel"
            ],
            'greeting_variations': {
                'hi': ["Hello!", "travel"],
                'hello': ["Hello!", "travel"],
                'hey': ["Hello!", "travel"],
                'good morning': ["Hello!", "travel"],
                'namaste': ["Hello!", "travel"],
                'invalid_greeting': ["I'm not sure", "start over"]
            },
            'destination': {
                'valid_cities': {
                    'mumbai': ["Great!", "When would you like to travel"],
                    'delhi': ["Great!", "When would you like to travel"],
                    'bangalore': ["Great!", "When would you like to travel"]
                },
                'invalid_cities': ["I'm not sure", "start over"]
            },
            'date': {
                'valid_dates': {
                    'next week': ["What would you like to know about", "1. Flights", "2. Hotels"],
                    'tomorrow': ["What would you like to know about", "1. Flights", "2. Hotels"],
                    '25th December': ["What would you like to know about", "1. Flights", "2. Hotels"]
                },
                'invalid_dates': ["I'm not sure", "start over"]
            },
            'menu': {
                'flights': {
                    'valid': ["Available flights", "Duration", "Price"],
                    'invalid': ["Please choose either 1 for Flights or 2 for Hotels"]
                },
                'hotels': {
                    'prompt': ["budget", "Rs."],
                    'valid_budget': ["Available hotels", "Rating", "Price"],
                    'invalid_budget': ["valid budget amount"]
                }
            }
        }

    def test_greetings(self):
        """Test all greeting variations"""
        print("\nTesting greetings...")
        for greeting, expected in self.expected_responses['greeting_variations'].items():
            with self.subTest(greeting=greeting):
                self.chatbot = TravelChatbot()  # Reset chatbot for each test
                response = self.chatbot.process_message(greeting)
                self.verify_response(response, expected, 'greeting')
                self.assertEqual(self.chatbot.history.current_context['pending_info'], 'destination')

    def test_destinations(self):
        """Test destination handling"""
        print("\nTesting destinations...")
        # Test valid cities
        for city, expected in self.expected_responses['destination']['valid_cities'].items():
            with self.subTest(city=city):
                self.chatbot.process_message("hi")  # Reset context
                response = self.chatbot.process_message(city)
                self.verify_response(response, expected, 'destination')
                self.assertEqual(self.chatbot.history.current_context['destination'], city)
        
        # Test invalid city
        self.chatbot.process_message("hi")  # Reset context
        response = self.chatbot.process_message("InvalidCity")
        self.verify_response(response, self.expected_responses['destination']['invalid_cities'], 'destination')

    def test_dates(self):
        """Test date handling"""
        print("\nTesting dates...")
        # Test valid dates
        for date, expected in self.expected_responses['date']['valid_dates'].items():
            with self.subTest(date=date):
                self.chatbot.process_message("hi")
                self.chatbot.process_message("mumbai")
                response = self.chatbot.process_message(date)
                self.verify_response(response, expected, 'date')
                self.assertEqual(self.chatbot.history.current_context['date'].lower(), date.lower())
        
        # Test invalid date
        self.chatbot.process_message("hi")
        self.chatbot.process_message("mumbai")
        response = self.chatbot.process_message("invalid_date")
        self.verify_response(response, self.expected_responses['date']['invalid_dates'], 'date')

    def test_menu_selection(self):
        """Test menu selection handling"""
        print("\nTesting menu selection...")
        # Setup context
        self.chatbot.process_message("hi")
        self.chatbot.process_message("mumbai")
        self.chatbot.process_message("next week")
        
        # Test flights
        response = self.chatbot.process_message("flights")
        self.verify_response(response, self.expected_responses['menu']['flights']['valid'], 'flight')
        
        # Test hotels
        self.chatbot.process_message("hi")  # Reset
        self.chatbot.process_message("mumbai")
        self.chatbot.process_message("next week")
        response = self.chatbot.process_message("hotels")
        self.verify_response(response, self.expected_responses['menu']['hotels']['prompt'], 'hotel')
        
        # Test invalid selection
        self.chatbot.process_message("hi")
        self.chatbot.process_message("mumbai")
        self.chatbot.process_message("next week")
        response = self.chatbot.process_message("invalid")
        self.verify_response(response, self.expected_responses['menu']['flights']['invalid'], 'menu')

    def test_hotel_budget(self):
        """Test hotel budget handling"""
        print("\nTesting hotel budget...")
        # Setup context
        self.chatbot.process_message("hi")
        self.chatbot.process_message("mumbai")
        self.chatbot.process_message("next week")
        self.chatbot.process_message("hotels")
        
        # Test valid budget (use a higher budget that will find hotels)
        response = self.chatbot.process_message("15000")
        self.verify_response(response, self.expected_responses['menu']['hotels']['valid_budget'], 'hotel')
        
        # Test invalid budget
        self.chatbot.process_message("hi")
        self.chatbot.process_message("mumbai")
        self.chatbot.process_message("next week")
        self.chatbot.process_message("hotels")
        response = self.chatbot.process_message("not a number")
        self.verify_response(response, self.expected_responses['menu']['hotels']['invalid_budget'], 'hotel')

    def test_conversation_flow(self):
        """Test complete conversation flows"""
        print("\nTesting complete conversation flows...")
        # Test flight booking flow
        responses = [
            self.chatbot.process_message("hi"),
            self.chatbot.process_message("mumbai"),
            self.chatbot.process_message("next week"),
            self.chatbot.process_message("1")  # Select flights
        ]
        self.verify_response(responses[-1], self.expected_responses['menu']['flights']['valid'], 'flight')
        
        # Test hotel booking flow
        self.chatbot = TravelChatbot()  # Reset chatbot
        responses = [
            self.chatbot.process_message("hi"),
            self.chatbot.process_message("mumbai"),
            self.chatbot.process_message("next week"),
            self.chatbot.process_message("2"),  # Select hotels
            self.chatbot.process_message("15000")  # Budget
        ]
        self.verify_response(responses[-1], self.expected_responses['menu']['hotels']['valid_budget'], 'hotel')

    def test_complete_conversation_flow(self):
        """Test a complete conversation flow with both flights and hotels"""
        print("\nTesting complete conversation flow...")
        
        # Test greeting
        response = self.chatbot.process_message("hi")
        self._verify_response(response, ["Hello!", "Where would you like to travel"])
        self.assertEqual(self.chatbot.history.current_context['pending_info'], 'destination')
        
        # Test destination
        response = self.chatbot.process_message("mumbai")
        self._verify_response(response, ["Great!", "When would you like to travel"])
        self.assertEqual(self.chatbot.history.current_context['destination'], 'mumbai')
        self.assertEqual(self.chatbot.history.current_context['pending_info'], 'date')
        
        # Test date
        response = self.chatbot.process_message("tomorrow")
        self._verify_response(response, ["What would you like to know about", "1. Flights", "2. Hotels"])
        self.assertEqual(self.chatbot.history.current_context['date'], 'tomorrow')
        self.assertEqual(self.chatbot.history.current_context['pending_info'], 'menu')
        
        # Test flights
        response = self.chatbot.process_message("1")  # Select flights
        self._verify_response(response, ["Available flights", "Duration", "Price", "Would you also like to check hotels"])
        self.assertEqual(self.chatbot.history.current_context['pending_info'], 'budget')
        
        # Test hotels
        response = self.chatbot.process_message("15000")  # High budget to ensure hotels are found
        self._verify_response(response, ["Available hotels", "Rating", "Price", "I've shown you the available options", "travel desk", "anything else", "hi to start"])
        self.assertIsNone(self.chatbot.history.current_context.get('pending_info'))  # Context should be reset
        
        # Test starting a new conversation
        response = self.chatbot.process_message("hi")
        self._verify_response(response, ["Hello!", "Where would you like to travel"])
        self.assertEqual(self.chatbot.history.current_context['pending_info'], 'destination')

    def test_error_handling(self):
        """Test error handling in the conversation flow"""
        print("\nTesting error handling...")
        
        # Test invalid greeting
        response = self.chatbot.process_message("invalid")
        self.assertIn("I'm not sure", response.lower())
        
        # Test invalid destination
        self.chatbot = TravelChatbot()
        self.chatbot.process_message("hi")
        response = self.chatbot.process_message("invalid_city")
        self.assertIn("I'm not sure", response.lower())
        
        # Test invalid date
        self.chatbot = TravelChatbot()
        self.chatbot.process_message("hi")
        self.chatbot.process_message("mumbai")
        response = self.chatbot.process_message("invalid_date")
        self.assertIn("I'm not sure", response.lower())
        
        # Test invalid menu selection
        self.chatbot = TravelChatbot()
        self.chatbot.process_message("hi")
        self.chatbot.process_message("mumbai")
        self.chatbot.process_message("tomorrow")
        response = self.chatbot.process_message("invalid_choice")
        self.assertIn("choose either 1", response.lower())
        
        # Test invalid budget
        self.chatbot = TravelChatbot()
        self.chatbot.process_message("hi")
        self.chatbot.process_message("mumbai")
        self.chatbot.process_message("tomorrow")
        self.chatbot.process_message("2")  # Select hotels
        response = self.chatbot.process_message("invalid_budget")
        self.assertIn("valid budget", response.lower())

    def verify_response(self, response: str, expected_phrases: list, context: str = None) -> None:
        """Verify response contains expected phrases"""
        for phrase in expected_phrases:
            self.assertIn(phrase.lower(), response.lower(), 
                         f"Response '{response}' missing phrase '{phrase}' in context '{context}'")

    def _verify_response(self, response: str, expected_phrases: list):
        """Helper method to verify response contains expected phrases"""
        for phrase in expected_phrases:
            self.assertIn(phrase.lower(), response.lower(),
                         f"Response missing expected phrase: {phrase}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
