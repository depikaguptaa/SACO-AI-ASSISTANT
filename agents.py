from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import requests
import time
from dotenv import load_dotenv
import os
from cache_service import cache_service

load_dotenv()

class Coordinates(BaseModel):
    latitude: float
    longitude: float
    address: str

class Amenity(BaseModel):
    name: str
    amenity_type: str
    distance: Optional[float] = None
    coordinates: Optional[Dict[str, float]] = None

class GeocodingAgent:
    """Agent responsible for converting addresses to coordinates using Nominatim API"""
    
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.user_agent = os.getenv("USER_AGENT", "MultiAgent-AI-Assistant/1.0")
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})
    
    async def geocode_address(self, address: str) -> Optional[Coordinates]:
        """
        Convert a US address to latitude and longitude using Nominatim API with caching
        
        Args:
            address: The address string to geocode
            
        Returns:
            Coordinates object with lat/lng or None if not found
        """
        try:
            # Check cache first
            cached_result = await cache_service.get('geocoding', {'address': address})
            if cached_result:
                print(f"Using cached geocoding for: {address}")
                return Coordinates(**cached_result)
            
            print(f"Geocoding address: {address}")
            
            # Add US country code to improve accuracy
            params = {
                "q": address,
                "format": "json",
                "countrycodes": "us",
                "limit": 1
            }
            
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            
            # Rate limiting - Nominatim requires 1 request per second
            time.sleep(1)
            
            data = response.json()
            
            if data and len(data) > 0:
                result = data[0]
                coords = Coordinates(
                    latitude=float(result["lat"]),
                    longitude=float(result["lon"]),
                    address=result["display_name"]
                )
                
                # Cache the result
                await cache_service.set('geocoding', {'address': address}, coords.dict())
                
                print(f"Found coordinates: {coords.latitude}, {coords.longitude}")
                return coords
            else:
                print(f"No coordinates found for address: {address}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error geocoding address: {e}")
            return None
        except (KeyError, ValueError) as e:
            print(f"Error parsing geocoding response: {e}")
            return None

class AmenitiesAgent:
    """Agent responsible for finding nearby amenities using Overpass API"""
    
    def __init__(self):
        self.base_urls = [
            "https://overpass-api.de/api/interpreter",
            "https://lz4.overpass-api.de/api/interpreter",
            "https://z.overpass-api.de/api/interpreter"
        ]
        self.current_url_index = 0
        self.session = requests.Session()
        self.default_radius = 1000  # Default radius in meters
    
    async def find_nearby_amenities(self, coordinates: Coordinates, radius: Optional[int] = None) -> List[Amenity]:
        """
        Find nearby amenities using Overpass API with caching
        
        Args:
            coordinates: The coordinates to search around
            radius: Search radius in meters (uses default if not provided)
            
        Returns:
            List of nearby amenities
        """
        try:
            # Use provided radius or default
            search_radius = radius if radius is not None else self.default_radius
            lat, lon = coordinates.latitude, coordinates.longitude
            
            # Check cache first
            cache_key = {
                'lat': lat,
                'lon': lon,
                'radius': search_radius
            }
            cached_result = await cache_service.get('amenities', cache_key)
            if cached_result:
                print(f"Using cached amenities for: {lat}, {lon} (radius: {search_radius}m)")
                return [Amenity(**amenity) for amenity in cached_result]
            
            print(f"Searching for amenities within {search_radius}m of {lat}, {lon}")
            
            # Overpass QL query for various amenities with dynamic radius
            airport_radius = search_radius * 5  # Larger radius for airports
            highway_radius = search_radius * 2  # Larger radius for highways
            
            # Use simpler query for large radius to avoid timeouts
            if search_radius > 3000:
                query = f"""
                [out:json];
                (
                  node["amenity"~"^(school|hospital|restaurant|fuel|bank|pharmacy)$"](around:{search_radius},{lat},{lon});
                  node["leisure"="park"](around:{search_radius},{lat},{lon});
                  node["shop"~"^(supermarket|mall)$"](around:{search_radius},{lat},{lon});
                );
                out body;
                """
            else:
                query = f"""
                [out:json];
                (
                  node["amenity"="school"](around:{search_radius},{lat},{lon});
                  node["amenity"="hospital"](around:{search_radius},{lat},{lon});
                  node["amenity"="restaurant"](around:{search_radius},{lat},{lon});
                  node["amenity"="fuel"](around:{search_radius},{lat},{lon});
                  node["amenity"="bank"](around:{search_radius},{lat},{lon});
                  node["amenity"="pharmacy"](around:{search_radius},{lat},{lon});
                  node["leisure"="park"](around:{search_radius},{lat},{lon});
                  node["leisure"="pitch"]["sport"="basketball"](around:{search_radius},{lat},{lon});
                  node["leisure"="pitch"]["sport"="tennis"](around:{search_radius},{lat},{lon});
                  node["leisure"="pitch"]["sport"="soccer"](around:{search_radius},{lat},{lon});
                  node["aeroway"="aerodrome"](around:{airport_radius},{lat},{lon});
                  way["highway"="motorway"](around:{highway_radius},{lat},{lon});
                  way["highway"="primary"](around:{search_radius},{lat},{lon});
                  node["shop"="supermarket"](around:{search_radius},{lat},{lon});
                  node["shop"="mall"](around:{search_radius},{lat},{lon});
                );
                out body;
                """
            
            # Try different Overpass servers if one fails
            for attempt in range(len(self.base_urls)):
                try:
                    current_url = self.base_urls[self.current_url_index]
                    print(f"Trying Overpass server: {current_url}")
                    
                    response = self.session.post(
                        current_url,
                        data=query,
                        headers={"Content-Type": "text/plain"},
                        timeout=30
                    )
                    response.raise_for_status()
                    break  # Success, exit the retry loop
                    
                except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
                    print(f"Server {current_url} failed: {e}")
                    self.current_url_index = (self.current_url_index + 1) % len(self.base_urls)
                    if attempt == len(self.base_urls) - 1:  # Last attempt
                        raise e
            
            data = response.json()
            amenities = self._parse_amenities(data["elements"])
            
            # Cache the result
            await cache_service.set('amenities', cache_key, [amenity.dict() for amenity in amenities])
            
            print(f"Found {len(amenities)} amenities")
            return amenities
            
        except requests.exceptions.Timeout as e:
            print(f"Timeout error querying amenities: {e}")
            print("Retrying with smaller radius...")
            # Retry with smaller radius
            if search_radius > 1000:
                return await self.find_nearby_amenities(coordinates, 1000)
            return []
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 504:
                print(f"Overpass API timeout (504). Retrying with smaller radius...")
                if search_radius > 1000:
                    return await self.find_nearby_amenities(coordinates, 1000)
            print(f"HTTP error querying amenities: {e}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"Error querying amenities: {e}")
            return []
        except (KeyError, ValueError) as e:
            print(f"Error parsing amenities response: {e}")
            return []
    
    def _parse_amenities(self, elements: List[Dict]) -> List[Amenity]:
        """Parse Overpass API response into Amenity objects"""
        amenities = []
        seen_names = set()
        
        for element in elements:
            tags = element.get("tags", {})
            
            # Determine amenity type and name
            amenity_type = self._get_amenity_type(tags)
            name = self._get_amenity_name(tags, amenity_type)
            
            if name and amenity_type:
                # Normalize name for deduplication
                normalized_name = name.lower().strip()
                if normalized_name in seen_names:
                    continue  # Skip duplicates
                seen_names.add(normalized_name)
                
                amenity = Amenity(
                    name=name,
                    amenity_type=amenity_type,
                    coordinates={
                        "lat": element.get("lat"),
                        "lon": element.get("lon")
                    } if "lat" in element else None
                )
                amenities.append(amenity)
        
        return amenities
    
    def _get_amenity_type(self, tags: Dict[str, str]) -> str:
        """Extract amenity type from OSM tags"""
        if "amenity" in tags:
            return f"amenity:{tags['amenity']}"
        elif "leisure" in tags:
            if "sport" in tags:
                return f"leisure:{tags['leisure']}:{tags['sport']}"
            return f"leisure:{tags['leisure']}"
        elif "aeroway" in tags:
            return f"aeroway:{tags['aeroway']}"
        elif "highway" in tags:
            return f"highway:{tags['highway']}"
        elif "shop" in tags:
            return f"shop:{tags['shop']}"
        return "unknown"
    
    def _get_amenity_name(self, tags: Dict[str, str], amenity_type: str) -> str:
        """Extract amenity name from OSM tags"""
        # Try different name fields
        for name_field in ["name", "brand", "operator"]:
            if name_field in tags:
                return tags[name_field]
        
        # Fallback to amenity type
        return amenity_type.replace(":", " ").title()
