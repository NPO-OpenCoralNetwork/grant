import json
import redis
from typing import Optional, Any
from app.core.config import settings


class RedisCache:
    """Redis cache manager"""

    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None

    def connect(self):
        """Connect to Redis"""
        try:
            self.redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                decode_responses=True
            )
            self.redis_client.ping()
            print("✓ Redis connection established")
        except (redis.ConnectionError, redis.RedisError) as e:
            print(f"⚠ Redis connection failed: {e}")
            print("Cache will be disabled")
            self.redis_client = None

    def disconnect(self):
        """Disconnect from Redis"""
        if self.redis_client:
            self.redis_client.close()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.redis_client:
            return None

        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
        except (redis.RedisError, json.JSONDecodeError):
            pass
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache"""
        if not self.redis_client:
            return False

        try:
            serialized = json.dumps(value, ensure_ascii=False)
            if ttl is None:
                ttl = settings.REDIS_CACHE_TTL
            self.redis_client.setex(key, ttl, serialized)
            return True
        except (redis.RedisError, TypeError, ValueError):
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.redis_client:
            return False

        try:
            self.redis_client.delete(key)
            return True
        except redis.RedisError:
            return False

    def flush_all(self) -> bool:
        """Flush all cache"""
        if not self.redis_client:
            return False

        try:
            self.redis_client.flushdb()
            return True
        except redis.RedisError:
            return False


# Global cache instance
cache = RedisCache()
