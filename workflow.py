from typing import Dict, Any, List, Optional, TypedDict
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from agents import GeocodingAgent, AmenitiesAgent, Coordinates, Amenity
from categorization_agent import CategorizationAgent
from cache_service import cache_service
import json
import asyncio

class AgentState(TypedDict):
    """State for the multi-agent workflow"""
    address: str
    radius: Optional[int]
    coordinates: Optional[Coordinates]
    amenities: List[Amenity]
    categorized_amenities: Optional[Dict[str, List[Dict[str, Any]]]]
    result: Optional[str]
    error: Optional[str]

class MultiAgentWorkflow:
    """LangGraph workflow coordinating geocoding and amenities agents"""
    
    def __init__(self):
        self.geocoding_agent = GeocodingAgent()
        self.amenities_agent = AmenitiesAgent()
        self.categorization_agent = CategorizationAgent()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self._get_api_key(),
            temperature=0.7
        )
        self.graph = self._build_graph()
        self._initialized = False
    
    async def initialize(self):
        """Initialize the workflow and cache service"""
        if not self._initialized:
            await cache_service.initialize()
            self._initialized = True
            print("Workflow initialized with caching")
    
    def _get_api_key(self) -> str:
        """Get Google API key from environment"""
        import os
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        return api_key
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("geocode", self._geocode_node)
        workflow.add_node("find_amenities_and_categorize", self._find_amenities_and_categorize_node)
        workflow.add_node("process_results", self._process_results_node)
        
        # Add edges
        workflow.set_entry_point("geocode")
        workflow.add_edge("geocode", "find_amenities_and_categorize")
        workflow.add_edge("find_amenities_and_categorize", "process_results")
        workflow.add_edge("process_results", END)
        
        return workflow.compile()
    
    async def _geocode_node(self, state: AgentState) -> AgentState:
        """Node for geocoding the address"""
        print(f"\nStep 1: Geocoding address...")
        
        try:
            coordinates = await self.geocoding_agent.geocode_address(state["address"])
            
            if coordinates:
                state["coordinates"] = coordinates
                state["error"] = None
            else:
                state["error"] = f"Could not find coordinates for address: {state['address']}"
                
        except Exception as e:
            state["error"] = f"Error during geocoding: {str(e)}"
        
        return state
    
    async def _find_amenities_and_categorize_node(self, state: AgentState) -> AgentState:
        """Node for finding amenities and categorizing them in parallel"""
        print(f"\nStep 2: Finding amenities and categorizing in parallel...")
        
        if state.get("error"):
            return state
        
        try:
            coordinates = state["coordinates"]
            radius = state.get("radius", None)
            
            # Run amenities and categorization in parallel
            amenities = await self.amenities_agent.find_nearby_amenities(coordinates, radius)
            
            if amenities:
                # Convert amenities to dict format for categorization
                amenities_data = []
                for amenity in amenities:
                    amenities_data.append({
                        "name": amenity.name,
                        "amenity_type": amenity.amenity_type
                    })
                
                # Run categorization
                categorized = await self.categorization_agent.categorize_amenities(amenities_data)
                
                state["amenities"] = amenities
                state["categorized_amenities"] = categorized
                print(f"Found {len(amenities)} amenities and categorized into {len(categorized)} categories")
            else:
                state["amenities"] = []
                state["categorized_amenities"] = {}
                
        except Exception as e:
            print(f"Error in parallel processing: {e}")
            state["error"] = f"Error finding amenities: {str(e)}"
        
        return state
    
    async def _process_results_node(self, state: AgentState) -> AgentState:
        """Node for processing results with Gemini LLM"""
        print(f"\nStep 3: Processing results with Gemini...")
        
        if state.get("error"):
            state["result"] = f"Error: {state['error']}"
            return state
        
        try:
            # Prepare data for LLM
            coordinates = state["coordinates"]
            categorized_amenities = state.get("categorized_amenities", {})
            
            # If we have categorized amenities, use them (much more efficient)
            if categorized_amenities:
                print(f"Using categorized data for analysis ({len(categorized_amenities)} categories)")
                prompt = self._create_prompt_from_categories(state["address"], coordinates, categorized_amenities)
            else:
                # Fallback to raw amenities (limit to avoid timeout)
                amenities = state["amenities"]
                print(f"Using raw amenities for analysis (limited to 100 items)")
                
                # Limit amenities to avoid timeout
                limited_amenities = amenities[:100] if len(amenities) > 100 else amenities
                
                # Group amenities by type
                amenities_by_type = {}
                for amenity in limited_amenities:
                    amenity_type = amenity.amenity_type.split(":")[0]  # Get main category
                    if amenity_type not in amenities_by_type:
                        amenities_by_type[amenity_type] = []
                    amenities_by_type[amenity_type].append(amenity.name)
                
                prompt = self._create_prompt(state["address"], coordinates, amenities_by_type)
            
            # Get response from Gemini with timeout handling
            try:
                messages = [
                    SystemMessage(content="You are a helpful assistant that provides detailed information about locations and their nearby amenities."),
                    HumanMessage(content=prompt)
                ]
                
                response = self.llm.invoke(messages)
                state["result"] = response.content
                state["error"] = None
                
            except Exception as e:
                print(f"Gemini API timeout/error: {e}")
                # Fallback to simple analysis
                state["result"] = self._create_fallback_analysis(state["address"], coordinates, categorized_amenities)
                state["error"] = None
            
        except Exception as e:
            state["error"] = f"Error processing results: {str(e)}"
            state["result"] = f"Error: {str(e)}"
        
        return state
    
    def _create_prompt_from_categories(self, address: str, coordinates: Coordinates, categorized_amenities: Dict[str, List[Dict]]) -> str:
        """Create a prompt using categorized amenities (much more efficient)"""
        
        # Count total amenities
        total_amenities = sum(len(items) for items in categorized_amenities.values())
        
        # Create summary of categories
        categories_summary = []
        for category, items in categorized_amenities.items():
            categories_summary.append(f"- **{category}**: {len(items)} locations")
        
        prompt = f"""
Please provide a comprehensive analysis of the location and its nearby amenities.

**Location Details:**
- Address: {address}
- Coordinates: {coordinates.latitude}, {coordinates.longitude}
- Full Address: {coordinates.address}

**Nearby Amenities Summary:**
Total amenities found: {total_amenities}

{chr(10).join(categories_summary)}

**Analysis Request:**
Please provide insights about:
1. **Location Quality**: What makes this area attractive for living/working?
2. **Amenity Density**: How well-served is this location with essential services?
3. **Lifestyle Factors**: What type of lifestyle does this area support?
4. **Notable Features**: Any standout amenities or unique characteristics?
5. **Recommendations**: Who would benefit most from living/working here?

Please provide a detailed, well-structured analysis that would be helpful for someone considering this location.
"""
        return prompt
    
    def _create_fallback_analysis(self, address: str, coordinates: Coordinates, categorized_amenities: Dict[str, List[Dict]]) -> str:
        """Create a fallback analysis when Gemini API fails"""
        
        if not categorized_amenities:
            return f"## Location Analysis\n\n**Address:** {address}\n**Coordinates:** {coordinates.latitude}, {coordinates.longitude}\n\n*Analysis unavailable due to API limitations.*"
        
        # Count amenities
        total_amenities = sum(len(items) for items in categorized_amenities.values())
        
        # Create basic analysis
        analysis = f"""## Location Analysis

**Address:** {address}
**Coordinates:** {coordinates.latitude}, {coordinates.longitude}
**Full Address:** {coordinates.address}

### Amenity Summary
Total amenities found: {total_amenities}

"""
        
        # Add category summaries
        for category, items in categorized_amenities.items():
            analysis += f"**{category}:** {len(items)} locations\n"
        
        analysis += f"""
### Key Insights
- This location has {total_amenities} nearby amenities across {len(categorized_amenities)} categories
- The area appears to be well-served with essential services
- Consider the proximity to your most important amenity types when evaluating this location

*Note: This is a basic analysis. For detailed insights, please try again later.*
"""
        
        return analysis
    
    def _create_prompt(self, address: str, coordinates: Coordinates, amenities_by_type: Dict[str, List[str]]) -> str:
        """Create a comprehensive prompt for Gemini"""
        
        prompt = f"""
        Please provide a comprehensive analysis of the location and its nearby amenities.

        **Location Details:**
        - Address: {address}
        - Coordinates: {coordinates.latitude}, {coordinates.longitude}
        - Full Address: {coordinates.address}

        **Nearby Amenities Found:**
        """
        
        for amenity_type, amenity_list in amenities_by_type.items():
            prompt += f"\n- {amenity_type.title()}: {', '.join(amenity_list)}"
        
        prompt += f"""

        **Please provide:**
        1. A brief description of the location
        2. Summary of available amenities by category
        3. Notable highlights (e.g., major attractions, transportation, services)
        4. Overall assessment of the area's convenience and livability
        5. Any recommendations or insights about the location

        Format your response in a clear, organized manner that would be helpful for someone considering this location.
        """
        
        return prompt
    
    async def process_address(self, address: str, radius: Optional[int] = None) -> Dict[str, Any]:
        """Process a US address through the complete workflow"""
        print(f"\nStarting multi-agent workflow for address: {address}")
        if radius:
            print(f"Using custom radius: {radius}m")
        
        # Initialize cache if not already done
        await self.initialize()
        
        initial_state = AgentState(
            address=address,
            radius=radius,
            coordinates=None,
            amenities=[],
            categorized_amenities=None,
            result=None,
            error=None
        )
        
        try:
            # Run the workflow steps sequentially with async operations
            state = initial_state.copy()
            
            # Step 1: Geocode
            state = await self._geocode_node(state)
            if state.get("error"):
                return {
                    "success": False,
                    "address": address,
                    "coordinates": None,
                    "amenities": [],
                    "categorized_amenities": None,
                    "result": None,
                    "error": state["error"]
                }
            
            # Step 2: Find amenities and categorize
            state = await self._find_amenities_and_categorize_node(state)
            if state.get("error"):
                return {
                    "success": False,
                    "address": address,
                    "coordinates": state.get("coordinates"),
                    "amenities": state.get("amenities", []),
                    "categorized_amenities": state.get("categorized_amenities"),
                    "result": None,
                    "error": state["error"]
                }
            
            # Step 3: Process results
            state = await self._process_results_node(state)
            
            return {
                "success": state.get("error") is None,
                "address": state["address"],
                "coordinates": state.get("coordinates"),
                "amenities": state.get("amenities", []),
                "categorized_amenities": state.get("categorized_amenities"),
                "result": state.get("result"),
                "error": state.get("error")
            }
            
        except Exception as e:
            return {
                "success": False,
                "address": address,
                "coordinates": None,
                "amenities": [],
                "categorized_amenities": None,
                "result": None,
                "error": f"Workflow error: {str(e)}"
            }
