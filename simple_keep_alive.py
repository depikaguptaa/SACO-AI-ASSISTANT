#!/usr/bin/env python3
"""
Simple keep-alive script for Render backend
Run this script to keep your backend alive
"""

import requests
import time
import sys
from datetime import datetime

# Your Render backend URL
BACKEND_URL = "https://saco-ai-assistant.onrender.com"

def ping_backend():
    """Ping the backend to keep it alive"""
    try:
        response = requests.get(f"{BACKEND_URL}/ping", timeout=10)
        if response.status_code == 200:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Ping OK")
            return True
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Ping failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Ping failed: {e}")
        return False

if __name__ == "__main__":
    print(f"🚀 Keeping {BACKEND_URL} alive...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            ping_backend()
            time.sleep(600)  # Wait 10 minutes
    except KeyboardInterrupt:
        print("\n🛑 Stopped")
        sys.exit(0)
