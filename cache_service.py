import json
import hashlib
import os
import asyncio
from typing import Optional, Any, Dict
import redis.asyncio as redis
from datetime import datetime, timedelta

class CacheService:
    """Redis-based caching service with fallback to in-memory cache"""
    
    def __init__(self):
        self.redis_client = None
        self.memory_cache = {}
        self.cache_ttl = {
            'geocoding': 24 * 60 * 60,  # 24 hours
            'amenities': 6 * 60 * 60,    # 6 hours
            'categorization': 12 * 60 * 60,  # 12 hours
            'analysis': 12 * 60 * 60     # 12 hours
        }
    
    async def initialize(self):
        """Initialize Redis connection with fallback to memory cache"""
        try:
            self.redis_client = redis.from_url(
                "redis://localhost:6379", 
                encoding="utf-8", 
                decode_responses=True
            )
            # Test connection
            await self.redis_client.ping()
            print("Redis cache connected")
        except Exception as e:
            print(f"Redis not available, using memory cache: {e}")
            self.redis_client = None
    
    def _generate_key(self, cache_type: str, data: Any) -> str:
        """Generate cache key from data"""
        data_str = json.dumps(data, sort_keys=True)
        hash_key = hashlib.md5(data_str.encode()).hexdigest()
        return f"saco:{cache_type}:{hash_key}"
    
    async def get(self, cache_type: str, data: Any) -> Optional[Any]:
        """Get cached data"""
        key = self._generate_key(cache_type, data)
        
        try:
            if self.redis_client:
                cached = await self.redis_client.get(key)
                if cached:
                    return json.loads(cached)
            else:
                # Fallback to memory cache
                if key in self.memory_cache:
                    cached_data, timestamp = self.memory_cache[key]
                    if datetime.now() - timestamp < timedelta(seconds=self.cache_ttl.get(cache_type, 3600)):
                        return cached_data
                    else:
                        del self.memory_cache[key]
        except Exception as e:
            print(f"Cache get error: {e}")
        
        return None
    
    async def set(self, cache_type: str, data: Any, result: Any):
        """Set cached data"""
        key = self._generate_key(cache_type, data)
        
        try:
            if self.redis_client:
                ttl = self.cache_ttl.get(cache_type, 3600)
                await self.redis_client.setex(key, ttl, json.dumps(result))
            else:
                # Fallback to memory cache
                self.memory_cache[key] = (result, datetime.now())
                # Clean old entries periodically
                if len(self.memory_cache) > 1000:
                    self._cleanup_memory_cache()
        except Exception as e:
            print(f"Cache set error: {e}")
    
    def _cleanup_memory_cache(self):
        """Clean up old memory cache entries"""
        now = datetime.now()
        keys_to_remove = []
        
        for key, (_, timestamp) in self.memory_cache.items():
            if now - timestamp > timedelta(hours=1):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.memory_cache[key]
    
    async def close(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()

# Global cache instance
cache_service = CacheService()
