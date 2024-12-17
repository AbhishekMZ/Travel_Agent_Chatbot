"""Flight Service for Indian Travel Chatbot

This module handles flight-related queries and provides information about
Indian airports, airlines, and flight routes.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os

class FlightService:
    def __init__(self):
        self.flights_data = {
            'chennai': {
                'mumbai': [
                    {
                        'airline': 'Air India',
                        'origin': 'chennai',
                        'destination': 'mumbai',
                        'duration': '2h 15m',
                        'base_price': 4800
                    },
                    {
                        'airline': 'IndiGo',
                        'origin': 'chennai',
                        'destination': 'mumbai',
                        'duration': '2h 10m',
                        'base_price': 4500
                    }
                ],
                'delhi': [
                    {
                        'airline': 'IndiGo',
                        'origin': 'chennai',
                        'destination': 'delhi',
                        'duration': '2h 45m',
                        'base_price': 5200
                    },
                    {
                        'airline': 'Air India',
                        'origin': 'chennai',
                        'destination': 'delhi',
                        'duration': '2h 50m',
                        'base_price': 5500
                    }
                ],
                'bangalore': [
                    {
                        'airline': 'SpiceJet',
                        'origin': 'chennai',
                        'destination': 'bangalore',
                        'duration': '1h 05m',
                        'base_price': 3500
                    },
                    {
                        'airline': 'IndiGo',
                        'origin': 'chennai',
                        'destination': 'bangalore',
                        'duration': '1h 00m',
                        'base_price': 3200
                    }
                ]
            },
            'mumbai': {
                'delhi': [
                    {
                        'airline': 'Air India',
                        'origin': 'mumbai',
                        'destination': 'delhi',
                        'duration': '2h 10m',
                        'base_price': 5000
                    },
                    {
                        'airline': 'Vistara',
                        'origin': 'mumbai',
                        'destination': 'delhi',
                        'duration': '2h 05m',
                        'base_price': 5200
                    }
                ],
                'bangalore': [
                    {
                        'airline': 'IndiGo',
                        'origin': 'mumbai',
                        'destination': 'bangalore',
                        'duration': '1h 45m',
                        'base_price': 4500
                    }
                ],
                'chennai': [
                    {
                        'airline': 'Vistara',
                        'origin': 'mumbai',
                        'destination': 'chennai',
                        'duration': '2h 15m',
                        'base_price': 4800
                    }
                ]
            },
            'delhi': {
                'mumbai': [
                    {
                        'airline': 'SpiceJet',
                        'origin': 'delhi',
                        'destination': 'mumbai',
                        'duration': '2h 15m',
                        'base_price': 4800
                    }
                ],
                'bangalore': [
                    {
                        'airline': 'Vistara',
                        'origin': 'delhi',
                        'destination': 'bangalore',
                        'duration': '2h 30m',
                        'base_price': 5500
                    }
                ],
                'chennai': [
                    {
                        'airline': 'Air India',
                        'origin': 'delhi',
                        'destination': 'chennai',
                        'duration': '2h 45m',
                        'base_price': 5200
                    }
                ]
            },
            'bangalore': {
                'mumbai': [
                    {
                        'airline': 'IndiGo',
                        'origin': 'bangalore',
                        'destination': 'mumbai',
                        'duration': '1h 45m',
                        'base_price': 4500
                    }
                ],
                'delhi': [
                    {
                        'airline': 'Air India',
                        'origin': 'bangalore',
                        'destination': 'delhi',
                        'duration': '2h 30m',
                        'base_price': 5500
                    }
                ],
                'chennai': [
                    {
                        'airline': 'SpiceJet',
                        'origin': 'bangalore',
                        'destination': 'chennai',
                        'duration': '1h 05m',
                        'base_price': 3500
                    }
                ]
            }
        }

        # Add more cities with their connections
        additional_routes = {
            'hyderabad': {
                'mumbai': [{'airline': 'IndiGo', 'duration': '1h 35m', 'base_price': 4200}],
                'delhi': [{'airline': 'Air India', 'duration': '2h 15m', 'base_price': 5100}],
                'bangalore': [{'airline': 'SpiceJet', 'duration': '1h 15m', 'base_price': 3800}]
            },
            'kolkata': {
                'delhi': [{'airline': 'Vistara', 'duration': '2h 30m', 'base_price': 5300}],
                'mumbai': [{'airline': 'IndiGo', 'duration': '2h 45m', 'base_price': 5500}],
                'bangalore': [{'airline': 'Air India', 'duration': '2h 40m', 'base_price': 5400}]
            },
            'jaipur': {
                'delhi': [{'airline': 'SpiceJet', 'duration': '1h 00m', 'base_price': 3800}],
                'mumbai': [{'airline': 'Air India', 'duration': '2h 00m', 'base_price': 4900}]
            },
            'agra': {
                'delhi': [{'airline': 'IndiGo', 'duration': '0h 45m', 'base_price': 3500}]
            },
            'varanasi': {
                'delhi': [{'airline': 'Air India', 'duration': '1h 30m', 'base_price': 4200}],
                'mumbai': [{'airline': 'IndiGo', 'duration': '2h 15m', 'base_price': 5100}]
            }
        }

        # Add the additional routes with complete information
        for origin, destinations in additional_routes.items():
            if origin not in self.flights_data:
                self.flights_data[origin] = {}
            
            for dest, flights in destinations.items():
                self.flights_data[origin][dest] = []
                for flight in flights:
                    complete_flight = {
                        'airline': flight['airline'],
                        'origin': origin,
                        'destination': dest,
                        'duration': flight['duration'],
                        'base_price': flight['base_price']
                    }
                    self.flights_data[origin][dest].append(complete_flight)

                    # Add return flight if it doesn't exist
                    if dest not in self.flights_data:
                        self.flights_data[dest] = {}
                    if origin not in self.flights_data[dest]:
                        self.flights_data[dest][origin] = []
                    
                    return_flight = {
                        'airline': flight['airline'],
                        'origin': dest,
                        'destination': origin,
                        'duration': flight['duration'],
                        'base_price': int(flight['base_price'] * 1.1)  # Slightly higher price for return
                    }
                    self.flights_data[dest][origin].append(return_flight)

    def get_flights(self, origin: str, destination: str, date: str) -> list:
        """Get flights from origin to destination on given date"""
        origin = origin.lower()
        destination = destination.lower()
        
        if origin not in self.flights_data or destination not in self.flights_data[origin]:
            return []
        
        # Get base flights for the route
        flights = self.flights_data[origin][destination]
        result_flights = []
        
        for flight in flights:
            # Create a copy of the flight to modify
            modified_flight = flight.copy()
            base_price = flight['base_price']
            
            # Apply price modifiers based on date
            if any(peak_time in date.lower() for peak_time in ['weekend', 'friday', 'sunday', 'january', 'december']):
                modified_flight['price'] = int(base_price * 1.2)  # 20% more expensive during peak times
            elif 'next month' in date.lower():
                modified_flight['price'] = int(base_price * 0.9)  # 10% cheaper for advance booking
            else:
                modified_flight['price'] = base_price
            
            # Add distance-based pricing
            if flight['duration'] > '2h 30m':
                modified_flight['price'] = int(modified_flight['price'] * 1.15)  # 15% more for long flights
            
            result_flights.append(modified_flight)
        
        return sorted(result_flights, key=lambda x: x['price'])

    def _filter_flights(self, origin: str, destination: str, date: str) -> List[Dict[str, Any]]:
        """Filter flights based on criteria"""
        return self.get_flights(origin, destination, date)
