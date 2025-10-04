from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv
from workflow import MultiAgentWorkflow
from agents import Coordinates, Amenity

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Agent AI Assistant API",
    description="API for processing US addresses and finding nearby amenities",
    version="1.0.0"
)

# Add CORS middleware for NextJS frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # NextJS default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the workflow
workflow = MultiAgentWorkflow()

# Request/Response Models
class AddressRequest(BaseModel):
    address: str = Field(..., description="US address to process")
    radius: int = Field(default=1000, ge=100, le=10000, description="Search radius in meters (100-10000)")

class CoordinatesResponse(BaseModel):
    latitude: float
    longitude: float
    address: str

class AmenityResponse(BaseModel):
    name: str
    amenity_type: str
    distance: Optional[float] = None
    coordinates: Optional[Dict[str, float]] = None

class AddressResponse(BaseModel):
    success: bool
    address: str
    coordinates: Optional[CoordinatesResponse] = None
    amenities: List[AmenityResponse] = []
    categorized_amenities: Optional[Dict[str, List[Dict[str, Any]]]] = None
    result: Optional[str] = None
    error: Optional[str] = None
    radius_used: int

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Multi-Agent AI Assistant API is running!", "status": "healthy"}

@app.post("/process-address", response_model=AddressResponse)
async def process_address(request: AddressRequest):
    """
    Process a US address and find nearby amenities
    
    Args:
        request: AddressRequest containing address and optional radius
        
    Returns:
        AddressResponse with coordinates, amenities, and AI analysis
    """
    try:
        # Validate API key
        if not os.getenv("GOOGLE_API_KEY"):
            raise HTTPException(
                status_code=500, 
                detail="Google API key not configured"
            )
        
        # Process the address with custom radius
        # Process the address through the workflow
        result = await workflow.process_address(request.address, request.radius)
        
        # Convert coordinates to response model
        coordinates_response = None
        if result["coordinates"]:
            coords = result["coordinates"]
            coordinates_response = CoordinatesResponse(
                latitude=coords.latitude,
                longitude=coords.longitude,
                address=coords.address
            )
        
        # Convert amenities to response model
        amenities_response = []
        for amenity in result["amenities"]:
            amenity_response = AmenityResponse(
                name=amenity.name,
                amenity_type=amenity.amenity_type,
                distance=amenity.distance,
                coordinates=amenity.coordinates
            )
            amenities_response.append(amenity_response)
        
        return AddressResponse(
            success=result["success"],
            address=result["address"],
            coordinates=coordinates_response,
            amenities=amenities_response,
            categorized_amenities=result.get("categorized_amenities"),
            result=result["result"],
            error=result["error"],
            radius_used=request.radius
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing address: {str(e)}"
        )

@app.get("/amenity-types")
async def get_amenity_types():
    """
    Get list of supported amenity types
    
    Returns:
        Dictionary of amenity categories and their types
    """
    return {
        "amenity_types": {
            "education": ["school", "university", "college"],
            "healthcare": ["hospital", "clinic", "pharmacy"],
            "food": ["restaurant", "cafe", "fast_food"],
            "shopping": ["supermarket", "mall", "shop"],
            "recreation": ["park", "pitch", "sports_centre"],
            "transportation": ["fuel", "aerodrome", "motorway"],
            "services": ["bank", "atm", "post_office"]
        },
        "default_radius": 1000,
        "min_radius": 100,
        "max_radius": 10000
    }

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    try:
        # Check if API key is configured
        api_key_configured = bool(os.getenv("GOOGLE_API_KEY"))
        
        return {
            "status": "healthy",
            "api_key_configured": api_key_configured,
            "services": {
                "nominatim": "available",
                "overpass": "available",
                "gemini": "configured" if api_key_configured else "not_configured"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
