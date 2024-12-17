"""Chat endpoint for the Travel Chatbot"""
import spacy
from typing import Dict, Any, List
from .flight_service import FlightService
from .hotel_recommender import HotelRecommender
from .chat_history import ChatHistory

class TravelChatbot:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.flight_service = FlightService()
        self.hotel_recommender = HotelRecommender()
        self.history = ChatHistory()
        self.greetings = {
            'hi', 'hello', 'hey', 'good morning', 'good afternoon', 
            'good evening', 'namaste', 'hola', 'greetings', 'howdy',
            'hi there', 'hello there', 'start', 'begin'
        }
        self.valid_cities = {'mumbai', 'delhi', 'bangalore', 'hyderabad', 'chennai', 'kolkata', 'jaipur', 'agra', 'varanasi'}

    def process_message(self, message: str) -> str:
        """Process user message and return appropriate response"""
        # Handle start over command
        if message.lower() in ['start over', 'restart', 'new search']:
            return self.history.start_over()

        # Handle greetings
        if self.history.current_context.get('pending_info') is None:
            self.history.reset()
            self.history.current_context['pending_info'] = 'origin'
            
            message_lower = message.lower().strip()
            if any(greeting in message_lower for greeting in self.greetings):
                return "Hello! I'm your travel assistant. I can help you book flights and find hotels. Which city are you traveling from?"
            return "Hi! To get started with planning your trip, please let me know which city you're traveling from."
        
        # Handle origin city
        if self.history.current_context.get('pending_info') == 'origin':
            if message.lower() in self.valid_cities:
                self.history.current_context['origin'] = message.lower()
                self.history.current_context['pending_info'] = 'destination'
                return "Great! And which city would you like to travel to?"
            return f"I'm not sure what you mean. Please enter a valid city ({', '.join(sorted(self.valid_cities))})."
        
        # Handle destination city
        if self.history.current_context.get('pending_info') == 'destination':
            if message.lower() in self.valid_cities:
                if message.lower() == self.history.current_context.get('origin'):
                    return "The destination city cannot be the same as your origin city. Please choose a different city."
                self.history.current_context['destination'] = message.lower()
                self.history.current_context['pending_info'] = 'date'
                return "Perfect! When would you like to travel?"
            return f"I'm not sure what you mean. Please enter a valid city ({', '.join(sorted(self.valid_cities))})."
        
        # Handle date
        if self.history.current_context.get('pending_info') == 'date':
            if any(date in message.lower() for date in ['next week',  'tomorrow',  '25th december',  'day after tomorrow',  'next monday',  'this friday',  'this weekend',  '1st january',  '15th august',  'in two days',  'in three weeks',  
                    'after 5 days',  'next month',  'next fortnight',  'this saturday',  'this sunday',  'coming friday',  'end of this week',  'early january',  'late february',  '4th july',  '31st march',  '14/02/2024',  '03/03/2024',  '2024-04-10',  '30-12-2024',  '2024/07/25']):
                self.history.current_context['date'] = message
                self.history.current_context['pending_info'] = 'menu'
                return "What would you like to know about?\n1. Flights\n2. Hotels"
            return "I'm not sure what you mean. Please enter a valid date."
        
        # Handle menu selection
        if self.history.current_context.get('pending_info') == 'menu':
            if message.lower() in ['2', 'hotels', 'hotel']:
                self.history.current_context['pending_info'] = 'budget'
                return "What's your budget per night for the hotel? (in Rs.)"
            elif message.lower() in ['1', 'flights', 'flight']:
                flights = self.flight_service.get_flights(
                    self.history.current_context['origin'],
                    self.history.current_context['destination'],
                    self.history.current_context['date']
                )
                if not flights:
                    return f"Sorry, no flights found from {self.history.current_context['origin'].title()} to {self.history.current_context['destination'].title()}. Please try different cities."
                
                flight_response = f"Available flights from {self.history.current_context['origin'].title()} to {self.history.current_context['destination'].title()}:\n" + "\n".join(
                    f"- {flight['airline']}: Duration {flight['duration']}, Price Rs. {flight['price']}"
                    for flight in flights
                )
                
                # Set context to budget to prompt for hotel recommendations
                self.history.current_context['pending_info'] = 'budget'
                return flight_response + "\n\nWould you also like to check hotels at your destination? What's your budget per night? (in Rs.)"
            return "Please choose either 1 for Flights or 2 for Hotels."
        
        # Handle hotel budget
        if self.history.current_context.get('pending_info') == 'budget':
            try:
                budget = float(message)
                self.history.current_context['budget'] = budget
                hotels = self.hotel_recommender.get_hotels_by_city_and_budget(
                    self.history.current_context['destination'], 
                    budget
                )
                
                # Store current context before resetting
                origin = self.history.current_context.get('origin', '')
                destination = self.history.current_context.get('destination', '')
                date = self.history.current_context.get('date', '')
                
                if not hotels:
                    # Don't reset context here to allow budget adjustment
                    return (
                        f"Sorry, I couldn't find any hotels in {destination} within your budget. "
                        "Please try a different budget or type 'start over' to begin a new search."
                    )
                elif 'message' in hotels[0]:
                    return hotels[0]['message'] + "\nType 'start over' to begin a new search."
                
                hotel_response = "Available hotels:\n" + "\n".join(
                    f"- {hotel['name']}: Rating {hotel['rating']}, Price Rs. {hotel['price']}"
                    for hotel in hotels
                )
                
                # Get conversation summary before resetting
                summary = self.history.get_conversation_summary()
                
                # Reset context after providing complete information
                self.history.reset()
                
                return (
                    f"{hotel_response}\n\n"
                    f"Based on {summary}\n\n"
                    f"You can book these options by contacting our travel desk at booking@travelagency.com.\n"
                    "Type 'start over' to begin a new search!"
                )
            except ValueError:
                return "Please enter a valid budget amount in Rs. (e.g., 5000) or type 'start over' to begin a new search."
        
        # Default response for unexpected messages
        return "I'm not sure what you mean. Type 'start over' to begin a new search."

    def _handle_conclusion(self, origin: str, destination: str, date: str) -> str:
        """Generate a conclusion message for the conversation"""
        return (
            f"Thank you for using our travel chatbot! Here's a summary of your search:\n"
            f"- Origin: {origin.capitalize()}\n"
            f"- Destination: {destination.capitalize()}\n"
            f"- Travel Date: {date}\n\n"
            "You can book any of the shown options by contacting our travel desk at booking@travelagency.com.\n"
            "Type 'start over' to begin a new search!"
        )

    def _is_greeting(self, message: str) -> bool:
        """Check if message is a greeting"""
        return message.lower() in self.greetings

    def _is_valid_city(self, city: str) -> bool:
        """Check if city is valid"""
        return city.lower() in self.valid_cities

    def _is_valid_date(self, date: str) -> bool:
        """Check if date is valid"""
        valid_date_terms = {'tomorrow', 'next week', 'next month', 'today'}
        date = date.lower()
        if date in valid_date_terms:
            return True
        # Add more date validation logic here if needed
        return True  # For now accept any date format

    def _get_menu_options(self) -> str:
        """Return menu options"""
        return """What would you like to know about? Choose an option:
1. Flights
2. Hotels"""

    def _handle_menu_selection(self, message: str) -> str:
        """Handle menu selection"""
        message = message.lower()
        
        # Handle flights
        if message in {'1', 'flights', 'flight'}:
            flights = self.flight_service.get_flights(
                self.history.current_context['origin'],
                self.history.current_context['destination'],
                self.history.current_context['date']
            )
            if not flights:
                return f"Sorry, no flights found from {self.history.current_context['origin'].title()} to {self.history.current_context['destination'].title()}. Please try different cities."
            return f"Available flights from {self.history.current_context['origin'].title()} to {self.history.current_context['destination'].title()}:\n" + "\n".join(
                f"- {flight['airline']}: Duration {flight['duration']}, Price Rs. {flight['price']}"
                for flight in flights
            )
            
        # Handle hotels
        if message in {'2', 'hotels', 'hotel'}:
            self.history.current_context['pending_info'] = 'budget'
            return "What's your budget per night for the hotel? (in Rs.)"
            
        # Handle invalid selection
        return "Please choose either 1 for Flights or 2 for Hotels"

    def _handle_hotel_budget(self, message: str) -> str:
        """Handle hotel budget"""
        try:
            budget = float(message)
            hotels = self.hotel_recommender.get_hotels_by_city_and_budget(
                self.history.current_context['destination'], 
                budget
            )
            if not hotels:
                return f"Sorry, I couldn't find any hotels in {self.history.current_context['destination']}. Please try another city."
            elif 'message' in hotels[0]:
                return hotels[0]['message']
            
            return "Available hotels:\n" + "\n".join(
                f"- {hotel['name']}: Rating {hotel['rating']}, Price Rs. {hotel['price']}"
                for hotel in hotels
            )
        except ValueError:
            return "Please enter a valid budget amount in numbers (e.g., 5000)"

def get_response(text: str) -> str:
    """Get response from chatbot."""
    return chatbot.process_message(text)

if __name__ == "__main__":
    chatbot = TravelChatbot()
    print("Bot: Hello! I'm your travel assistant. Which city are you traveling from?")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Bot: Thank you for chatting! Have a great trip!")
            break
        response = get_response(user_input)
        print(f"Bot: {response}")