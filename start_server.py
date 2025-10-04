#!/usr/bin/env python3
"""
Startup script for the Multi-Agent AI Assistant API
"""

import uvicorn
import os
from dotenv import load_dotenv

def main():
    """Start the FastAPI server"""
    load_dotenv()
    
    # Check if API key is configured
    if not os.getenv("GOOGLE_API_KEY"):
        print("Warning: GOOGLE_API_KEY not found in environment variables")
        print("Please set your Google API key in the .env file")
        print("You can get a free API key from: https://makersuite.google.com/app/apikey")
        print("\nContinuing without API key (some features may not work)...")
    
    print("Starting Multi-Agent AI Assistant API...")
    print("API will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    print("Health check at: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server")
    
    # Start the server
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )

if __name__ == "__main__":
    main()
