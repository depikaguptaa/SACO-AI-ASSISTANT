#!/usr/bin/env python3
"""
Keep-alive script for Render backend
Pings the backend every 10 minutes to prevent it from sleeping
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
            data = response.json()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Ping successful: {data.get('message', 'OK')}")
            return True
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Ping failed: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Ping failed: {e}")
        return False

def main():
    """Main keep-alive loop"""
    print(f"🚀 Starting keep-alive for {BACKEND_URL}")
    print("Press Ctrl+C to stop")
    
    ping_interval = 10 * 60  # 10 minutes in seconds
    
    try:
        while True:
            ping_backend()
            print(f"⏰ Next ping in {ping_interval // 60} minutes...")
            time.sleep(ping_interval)
    except KeyboardInterrupt:
        print("\n🛑 Keep-alive stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
