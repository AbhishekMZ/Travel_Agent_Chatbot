# Travel Agency Chatbot

A conversational AI chatbot that helps users find and book flights and hotels for their travel plans.

## Features

- Natural language conversation for travel planning
- Flight search and recommendations
- Hotel recommendations based on budget
- Multi-step conversation flow with context management
- Error handling and graceful fallbacks
- Seamless integration between flight and hotel bookings
- Detailed summaries of travel options

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/TravelAgencyChatBot.git
cd TravelAgencyChatBot
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install spaCy English language model:
```bash
python -m spacy download en_core_web_sm
```

### Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage Guide

The chatbot follows a structured conversation flow:

1. **Greeting**: Start with a simple greeting (hi, hello, hey, etc.)
2. **Destination**: Enter your desired city (supports the following cities):
   - Delhi (DEL) - Indira Gandhi International Airport
   - Mumbai (BOM) - Chhatrapati Shivaji Maharaj International Airport
   - Bangalore (BLR) - Kempegowda International Airport
   - Hyderabad (HYD) - Rajiv Gandhi International Airport
   - Chennai (MAA) - Chennai International Airport
   - Kolkata (CCU) - Netaji Subhas Chandra Bose International Airport
   - Jaipur (JAI) - Jaipur International Airport
   - Agra (AGR) - Agra Airport
   - Varanasi (VNS) - Lal Bahadur Shastri International Airport
3. **Travel Date**: Specify when you want to travel
4. **Service Selection**: Choose between flights (1) or hotels (2)
5. **Budget**: For hotels, specify your per-night budget in Rs.
6. **Results**: View available options with prices and details
7. **Booking**: Contact the travel desk using the provided email for bookings

### Example Conversation

```
User: Hi
Bot: Hello! Where would you like to travel?

User: Mumbai
Bot: Great! When would you like to travel?

User: next week
Bot: What would you like to know about?
1. Flights
2. Hotels

User: 1
Bot: [Shows available flights]
Would you also like to check hotels? What's your budget per night? (in Rs.)
```

## Project Structure

```
TravelAgencyChatBot/
├── app.py                 # Flask application entry point
├── requirements.txt       # Python dependencies
├── src/
│   ├── chat_endpoint.py   # Main chatbot logic
│   ├── chat_history.py    # Conversation context management
│   ├── flight_service.py  # Flight search functionality
│   └── hotel_recommender.py # Hotel recommendation system
├── data/                  # Sample data for flights and hotels
├── static/               # Static assets (CSS, JS)
├── templates/            # HTML templates
└── tests/                # Unit tests
```

## Testing

Run the test suite to verify functionality:

```bash
python -m unittest tests/test_chatbot.py -v
```

## Error Handling

The chatbot includes robust error handling for:
- Invalid cities
- Invalid dates
- Incorrect menu selections
- Invalid budget inputs
- Missing or incomplete information

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For support or queries, contact: support@travelagency.com

## Acknowledgments

- Built with Flask and spaCy
- Uses modern conversational UI principles
- Implements best practices for chatbot development
