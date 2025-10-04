from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import requests
import time
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
import json
from cache_service import cache_service

load_dotenv()

class CategorizationAgent:
    """AI Agent responsible for intelligently categorizing amenities using Gemini LLM"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self._get_api_key(),
            temperature=0.3  # Lower temperature for more consistent categorization
        )
    
    def _get_api_key(self) -> str:
        """Get Google API key from environment"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        return api_key
    
    async def categorize_amenities(self, amenities: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Use AI to intelligently categorize amenities based on their names and types with caching
        
        Args:
            amenities: List of amenity dictionaries with name and amenity_type
            
        Returns:
            Dictionary with categories as keys and lists of amenities as values
        """
        try:
            # Check cache first
            cached_result = await cache_service.get('categorization', {'amenities': amenities})
            if cached_result:
                print(f"Using cached categorization for {len(amenities)} amenities")
                return cached_result
            
            # If too many amenities, use batch processing
            if len(amenities) > 1000:
                print(f"Large dataset ({len(amenities)} amenities), using batch processing...")
                return await self._categorize_in_batches(amenities)
            
            # Prepare the amenities data for the LLM
            amenities_text = self._format_amenities_for_llm(amenities)
            
            # Create the prompt for categorization
            prompt = f"""
You are an expert at categorizing business amenities and services. Your task is to categorize the following amenities into logical, user-friendly categories.

Rules:
1. Group similar amenities together (e.g., all restaurants, cafes, fast food under "Dining")
2. Use clear, intuitive category names that users would understand
3. Aim for 6-8 main categories maximum
4. Consider both the amenity type and the business name when categorizing
5. Return ONLY a JSON object with categories as keys and lists of amenity names as values

Amenities to categorize:
{amenities_text}

Return format:
{{
  "Dining": ["Restaurant Name 1", "Restaurant Name 2"],
  "Healthcare": ["Hospital Name", "Pharmacy Name"],
  "Education": ["School Name"],
  "Banking": ["Bank Name"],
  "Shopping": ["Store Name"],
  "Recreation": ["Park Name"],
  "Transportation": ["Highway Name"],
  "Other": ["Any other amenities"]
}}

Important: Return ONLY the JSON object, no additional text or explanation.
"""
            
            print(f"AI Categorizing {len(amenities)} amenities...")
            
            # Get AI categorization with timeout handling
            try:
                response = self.llm.invoke(prompt)
                categorization_text = response.content.strip()
            except Exception as e:
                print(f"Gemini API error: {e}")
                print("Falling back to batch processing...")
                return await self._categorize_in_batches(amenities)
            
            # Parse the JSON response
            try:
                # Clean the response to extract just the JSON
                if categorization_text.startswith("```json"):
                    categorization_text = categorization_text.replace("```json", "").replace("```", "").strip()
                elif categorization_text.startswith("```"):
                    categorization_text = categorization_text.replace("```", "").strip()
                
                categorization = json.loads(categorization_text)
                
                # Convert back to amenity objects
                categorized_amenities = {}
                for category, amenity_names in categorization.items():
                    categorized_amenities[category] = []
                    for name in amenity_names:
                        # Find the original amenity object
                        for amenity in amenities:
                            if amenity.get('name') == name:
                                categorized_amenities[category].append(amenity)
                                break
                
                # Cache the result
                await cache_service.set('categorization', {'amenities': amenities}, categorized_amenities)
                
                print(f"AI categorized amenities into {len(categorized_amenities)} categories")
                return categorized_amenities
                
            except json.JSONDecodeError as e:
                print(f"Error parsing AI response as JSON: {e}")
                print(f"Raw response: {categorization_text}")
                # Fallback to hard-coded categorization
                return self._fallback_categorization(amenities)
                
        except Exception as e:
            print(f"Error in AI categorization: {e}")
            # Fallback to hard-coded categorization
            return self._fallback_categorization(amenities)
    
    def _format_amenities_for_llm(self, amenities: List[Dict[str, Any]]) -> str:
        """Format amenities data for LLM processing"""
        formatted = []
        for amenity in amenities:
            name = amenity.get('name', 'Unknown')
            amenity_type = amenity.get('amenity_type', 'Unknown')
            formatted.append(f"- {name} (Type: {amenity_type})")
        return "\n".join(formatted)
    
    def _fallback_categorization(self, amenities: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Fallback categorization using hard-coded rules"""
        categories = {}
        
        for amenity in amenities:
            amenity_type = amenity.get('amenity_type', '').split(':')[1] if ':' in amenity.get('amenity_type', '') else amenity.get('amenity_type', '')
            name = amenity.get('name', '').lower()
            
            # Determine category based on type and name
            if any(keyword in amenity_type.lower() for keyword in ['restaurant', 'cafe', 'fast_food', 'food_court']) or \
               any(keyword in name for keyword in ['restaurant', 'cafe', 'pizza', 'burger', 'sushi', 'thai', 'chinese', 'mexican', 'italian']):
                category = 'Dining'
            elif any(keyword in amenity_type.lower() for keyword in ['school', 'university', 'college']) or \
                 any(keyword in name for keyword in ['school', 'university', 'college', 'academy']):
                category = 'Education'
            elif any(keyword in amenity_type.lower() for keyword in ['hospital', 'pharmacy', 'clinic', 'dentist']) or \
                 any(keyword in name for keyword in ['hospital', 'pharmacy', 'clinic', 'medical', 'health']):
                category = 'Healthcare'
            elif any(keyword in amenity_type.lower() for keyword in ['bank', 'atm', 'bureau_de_change']) or \
                 any(keyword in name for keyword in ['bank', 'credit union', 'atm']):
                category = 'Banking'
            elif any(keyword in amenity_type.lower() for keyword in ['supermarket', 'convenience', 'mall', 'shop']) or \
                 any(keyword in name for keyword in ['market', 'store', 'shop', 'mall', 'grocery']):
                category = 'Shopping'
            elif any(keyword in amenity_type.lower() for keyword in ['fuel', 'car_wash', 'garage']) or \
                 any(keyword in name for keyword in ['gas', 'fuel', 'shell', 'chevron', 'arco']):
                category = 'Automotive'
            elif any(keyword in amenity_type.lower() for keyword in ['park', 'playground', 'sports_centre', 'pitch']) or \
                 any(keyword in name for keyword in ['park', 'playground', 'sports', 'recreation']):
                category = 'Recreation'
            elif any(keyword in amenity_type.lower() for keyword in ['highway', 'motorway', 'primary']):
                category = 'Transportation'
            else:
                category = 'Other'
            
            if category not in categories:
                categories[category] = []
            categories[category].append(amenity)
        
        return categories
    
    async def _categorize_in_batches(self, amenities: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize amenities in smaller batches to avoid API timeouts"""
        batch_size = 500  # Process 500 amenities at a time
        all_categorized = {}
        
        print(f"Processing {len(amenities)} amenities in batches of {batch_size}")
        
        for i in range(0, len(amenities), batch_size):
            batch = amenities[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(amenities) + batch_size - 1) // batch_size
            
            print(f"Processing batch {batch_num}/{total_batches} ({len(batch)} amenities)")
            
            try:
                # Use hard-coded categorization for large batches to avoid API timeouts
                batch_categorized = self._fallback_categorization(batch)
                
                # Merge results
                for category, items in batch_categorized.items():
                    if category not in all_categorized:
                        all_categorized[category] = []
                    all_categorized[category].extend(items)
                    
            except Exception as e:
                print(f"Error processing batch {batch_num}: {e}")
                # Continue with next batch
                continue
        
        print(f"Batch processing complete. Categorized into {len(all_categorized)} categories")
        return all_categorized
