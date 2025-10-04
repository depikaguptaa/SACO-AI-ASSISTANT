# Multi-Agent AI Assistant - Backend API

A FastAPI backend that provides REST endpoints for the Multi-Agent AI Assistant system.

## 🚀 Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Google API key
   ```

3. **Start the API server**:
   ```bash
   python start_server.py
   # OR
   uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API**:
   - API Base URL: `http://localhost:8000`
   - Interactive Docs: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

## 📡 API Endpoints

### POST `/process-address`
Process a US address and find nearby amenities.

**Request Body**:
```json
{
  "address": "1600 Pennsylvania Avenue NW, Washington, DC",
  "radius": 1000
}
```

**Response**:
```json
{
  "success": true,
  "address": "1600 Pennsylvania Avenue NW, Washington, DC",
  "coordinates": {
    "latitude": 38.8977,
    "longitude": -77.0365,
    "address": "1600 Pennsylvania Avenue NW, Washington, DC 20500, USA"
  },
  "amenities": [
    {
      "name": "White House",
      "amenity_type": "amenity:government",
      "coordinates": {"lat": 38.8977, "lon": -77.0365}
    }
  ],
  "result": "AI analysis of the location...",
  "radius_used": 1000
}
```

### GET `/amenity-types`
Get supported amenity types and configuration.

### GET `/health`
Detailed health check of all services.

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google Gemini API key (required)
- `USER_AGENT`: Custom user agent for Nominatim API (optional)

### Radius Settings
- **Default**: 1000m (1km)
- **Minimum**: 100m
- **Maximum**: 10000m (10km)
- **Airports**: Automatically uses 5x radius
- **Highways**: Automatically uses 2x radius

## 🌐 Frontend Integration

The API is designed to work seamlessly with NextJS frontends. See `frontend-integration.js` for complete integration examples.

### CORS Configuration
The API includes CORS middleware configured for:
- `http://localhost:3000` (NextJS default)
- `http://127.0.0.1:3000`

### Example Frontend Usage
```javascript
// Process an address
const response = await fetch('http://localhost:8000/process-address', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    address: 'Times Square, New York, NY',
    radius: 2000
  })
});

const result = await response.json();
```

## 🛠️ Development

### Running in Development Mode
```bash
python start_server.py
```
This enables auto-reload and detailed logging.

### Testing the API
```bash
# Test with curl
curl -X POST "http://localhost:8000/process-address" \
  -H "Content-Type: application/json" \
  -d '{"address": "Times Square, New York, NY", "radius": 1000}'

# Check health
curl http://localhost:8000/health
```

## 📊 Rate Limits & Best Practices

- **Nominatim**: 1 request/second (automatically handled)
- **Overpass**: Reasonable usage policy
- **Gemini**: Follow Google's API limits
- **CORS**: Configured for localhost development

## 🐛 Troubleshooting

### Common Issues

1. **"Google API key not configured"**
   - Ensure `GOOGLE_API_KEY` is set in `.env`
   - Verify the key is valid and active

2. **CORS errors in frontend**
   - Check that frontend URL is in CORS allowlist
   - Ensure API is running on correct port

3. **"No amenities found"**
   - Try increasing the radius
   - Check if address is valid and in the US

4. **API not responding**
   - Check if port 8000 is available
   - Verify all dependencies are installed

## 🔄 Deployment

### Production Deployment
```bash
# Install production dependencies
pip install -r requirements.txt

# Set production environment variables
export GOOGLE_API_KEY=your_production_key

# Run with production settings
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

**Ready to integrate with your NextJS frontend! 🎉**
