# SACO AI Assistant

A multi-agent AI system that takes any US address and finds nearby amenities. Built with FastAPI backend and NextJS frontend, it uses free APIs and Google's Gemini for intelligent analysis.

## What it does

You give it an address like "123 Main St, New York, NY" and it:
1. Finds the exact coordinates
2. Searches for nearby amenities (schools, restaurants, parks, etc.)
3. Groups them intelligently using AI
4. Gives you insights about the location

## Project Structure

```
SACO Assignment/
├── Backend (Python/FastAPI)
│   ├── agents.py              # Handles geocoding and finding amenities
│   ├── categorization_agent.py # Uses AI to group amenities
│   ├── cache_service.py       # Redis caching (falls back to memory)
│   ├── workflow.py            # Orchestrates the whole process
│   ├── api.py                 # REST API endpoints
│   ├── config.py              # Settings
│   ├── start_server.py        # Starts the server
│   └── requirements.txt       # Python packages
│
├── Frontend (NextJS)
│   └── saco-frontend/         # The web interface
│       ├── src/app/           # Pages
│       ├── src/components/ui/ # UI components
│       ├── src/hooks/         # React hooks
│       ├── src/lib/           # API calls and utilities
│       └── public/            # Images and static files
│
└── README.md
```

## Getting Started

### What you need
- Python 3.8+ 
- Node.js 18+
- Google API key (free from Google AI Studio)
- Redis (optional - it'll use memory cache if Redis isn't available)

### Backend Setup
1. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file:
   ```bash
   echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env
   echo "USER_AGENT=SACO-AI-Assistant/1.0" >> .env
   ```

3. Start Redis (if you have it):
   ```bash
   # Windows
   redis-server
   
   # Linux/Mac
   sudo systemctl start redis
   ```

4. Start the API:
   ```bash
   python start_server.py
   ```

### Frontend Setup
1. Go to the frontend folder:
   ```bash
   cd saco-frontend
   ```

2. Install packages:
   ```bash
   npm install
   ```

3. Start the dev server:
   ```bash
   npm run dev
   ```

## How it works

### The Process
1. **Geocoding**: Converts your address to lat/lng using Nominatim
2. **Amenity Search**: Uses Overpass API to find nearby places
3. **AI Categorization**: Gemini groups amenities intelligently
4. **Analysis**: Gemini provides insights about the location

### Performance Features
- **Caching**: Results are cached so repeated searches are instant
- **Parallel Processing**: Searches and categorization happen simultaneously
- **Progressive Loading**: Frontend shows real-time progress
- **Retry Logic**: If an API fails, it tries again or uses fallbacks

### UI Features
- **Modern Design**: Clean interface with glass effects and animations
- **Real-time Updates**: See progress as it processes your request
- **Interactive Controls**: Adjust search radius with a slider
- **Organized Results**: Amenities grouped by category with pagination

## API Endpoints

- `POST /process-address` - Main endpoint to process an address
- `GET /amenity-types` - Get list of supported amenity types
- `GET /health` - Check if everything is working

## Access Points

- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Redis**: Caching (with memory fallback)
- **Nominatim**: Free geocoding
- **Overpass**: Free OpenStreetMap data
- **Google Gemini**: AI for analysis and categorization
- **Pydantic**: Data validation

### Frontend
- **NextJS 15**: React framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Aceternity UI**: Premium components
- **Framer Motion**: Animations
- **ReactMarkdown**: Renders AI analysis

## What amenities it finds

The system looks for:
- **Education**: Schools, universities, colleges
- **Healthcare**: Hospitals, clinics, pharmacies
- **Dining**: Restaurants, cafes, fast food
- **Banking**: Banks, ATMs
- **Shopping**: Supermarkets, malls, stores
- **Recreation**: Parks, sports facilities
- **Transportation**: Gas stations, airports, highways
- **Other**: Everything else

## Environment Variables

Create a `.env` file:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
USER_AGENT=SACO-AI-Assistant/1.0
```

## Error Handling

The system handles failures gracefully:
- **Nominatim**: Rate limited to 1 request/second
- **Overpass**: Multiple servers with retry logic
- **Gemini**: Timeouts with fallback analysis
- **Redis**: Falls back to memory cache if unavailable

## Production Deployment

### Backend
```bash
pip install -r requirements.txt
export GOOGLE_API_KEY=your_key_here
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd saco-frontend
npm install
npm run build
npm start
```


That's it! Give it an address and see what's nearby.