# Configuration for Multi-Agent AI Assistant

# API Configuration
NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_BASE_URL = "https://overpass-api.de/api/interpreter"

# Rate Limiting (Nominatim requires 1 request per second)
NOMINATIM_RATE_LIMIT = 1.0  # seconds between requests

# Search Configuration
DEFAULT_SEARCH_RADIUS = 1000  # meters
AIRPORT_SEARCH_RADIUS = 5000  # meters (larger radius for airports)
HIGHWAY_SEARCH_RADIUS = 2000  # meters (larger radius for highways)

# Amenity Types to Search For
AMENITY_TYPES = {
    "education": ["school", "university", "college"],
    "healthcare": ["hospital", "clinic", "pharmacy"],
    "food": ["restaurant", "cafe", "fast_food"],
    "shopping": ["supermarket", "mall", "shop"],
    "recreation": ["park", "pitch", "sports_centre"],
    "transportation": ["fuel", "aerodrome", "motorway"],
    "services": ["bank", "atm", "post_office"]
}

# Gemini Model Configuration
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_TEMPERATURE = 0.7
GEMINI_MAX_TOKENS = 2048
