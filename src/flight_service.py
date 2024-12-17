"""Flight Service for Indian Travel Chatbot

This module handles flight-related queries and provides information about
Indian airports, airlines, and flight routes.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

class FlightService:
    def __init__(self):
        self.mock_flights = [
            {
                'airline': 'Air India',
                'flight_no': 'AI-101',
                'departure': '09:00',
                'arrival': '11:00',
                'price': 5000.0,
                'duration': '2h 00m'
            },
            {
                'airline': 'IndiGo',
                'flight_no': '6E-345',
                'departure': '11:30',
                'arrival': '13:30',
                'price': 4500.0,
                'duration': '2h 00m'
            },
            {
                'airline': 'SpiceJet',
                'flight_no': 'SG-123',
                'departure': '14:00',
                'arrival': '16:00',
                'price': 4000.0,
                'duration': '2h 00m'
            }
        ]

    def get_flights(self, origin: str, date: str) -> list:
        """Get flights from origin to any destination on given date"""
        flights = [
            {
                'airline': 'Air India',
                'origin': 'mumbai',
                'destination': 'delhi',
                'duration': '2h 10m',
                'price': 5000
            },
            {
                'airline': 'IndiGo',
                'origin': 'mumbai',
                'destination': 'bangalore',
                'duration': '1h 45m',
                'price': 4500
            },
            {
                'airline': 'SpiceJet',
                'origin': 'delhi',
                'destination': 'mumbai',
                'duration': '2h 15m',
                'price': 4800
            },
            {
                'airline': 'Vistara',
                'origin': 'delhi',
                'destination': 'bangalore',
                'duration': '2h 30m',
                'price': 5500
            }
        ]
        
        return [flight for flight in flights 
                if flight['origin'].lower() == origin.lower()]

    def _filter_flights(self, origin: str, destination: str, date: str) -> List[Dict[str, Any]]:
        """Filter flights based on criteria"""
        # In a real implementation, this would query a flight database
        # For now, return mock data
        return self.mock_flights
