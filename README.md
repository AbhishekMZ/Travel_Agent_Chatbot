# India Travel Chatbot

An intelligent chatbot specialized in Indian travel assistance, providing hotel recommendations, cultural insights, and travel planning help.

## Features

### Hotel Recommendations
- Personalized hotel suggestions based on:
  - City preferences
  - Budget categories (luxury, mid-range, budget)
  - Peak season awareness
  - Nearby attractions
  - Festival considerations

### Travel Information
- Comprehensive city guides
- Festival and event information
- Weather-aware recommendations
- Local attraction details
- Cultural insights

### Smart Context Handling
- Budget-aware suggestions
- Seasonal considerations
- Festival period adjustments
- Location-specific tips

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

3. Ensure all data files are present:
- india_cities.json
- india_festivals.json
- india_travel_data.csv
- india_travel_intents.json

## Usage

Run the chatbot:
```bash
python src/chat_endpoint.py
```

### Example Queries

1. Hotel Search:
   - "Show me luxury hotels in Mumbai"
   - "Find budget hotels in Delhi near Red Fort"
   - "Hotels in Jaipur during Diwali"

2. Travel Information:
   - "What's the best time to visit Kerala?"
   - "Tell me about festivals in Rajasthan"
   - "Popular attractions in Agra"

## Data Structure

The chatbot uses several JSON files for structured data:

1. `india_cities.json`: City-specific information including:
   - Hotels by category
   - Local attractions
   - Transportation options
   - Weather patterns

2. `india_festivals.json`: Festival and seasonal information:
   - Major festivals
   - Peak seasons
   - Travel tips
   - Cultural events

3. `india_travel_intents.json`: Conversation patterns:
   - User intents
   - Response templates
   - Query patterns

## Customization

You can extend the chatbot's knowledge by:
1. Adding new cities to `india_cities.json`
2. Including more festivals in `india_festivals.json`
3. Expanding travel patterns in `india_travel_intents.json`

## Dependencies

- Python 3.8+
- spaCy
- pandas
- dateparser
- requests

## Contributing

Feel free to contribute by:
1. Adding more cities and hotels
2. Improving response patterns
3. Adding new features
4. Enhancing cultural context

## License

MIT License
