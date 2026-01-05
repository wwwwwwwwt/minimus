from functools import lru_cache
import logging
from redis.asyncio import Redis
from core.config import get_settings, Settings
from typing import Any, List, Dict

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self) -> None:
        self._client : Redis | None = None
        self._settings: Settings = get_settings()

    async def init(self) -> None:
        if self._client is not None:
            return
        
        try:
            self._client = Redis(host=self._settings.REDIS_HOST, port=self._settings.REDIS_PORT, db=self._settings.REDIS_DB
                ,decode_responses=True)
        except Exception as e:
            logger.error(f"Failed to initialize Redis client: {e}")
            raise e
        await self.is_alive()
        logger.info("Redis client initialized")

    async def is_alive(self) -> bool:
        return await self._client.ping()

    async def close(self) -> None:
        if self._client is None:
            return
        await self._client.close()
        self._client = None
        logger.info("Redis client closed")
        get_redis_client.cache_clear()


    @property
    def client(self) -> Redis | None:
        if self._client is None:
            logger.error("Redis client is not initialized")
            raise ValueError("Redis client is not initialized")
        return self._client


    async def setnxex(self, key: str, value: Any, seconds: int) -> bool:
        return await self._client.setnxex(key, value, seconds)
    
    async def setnxex(self, key: str, value: Any, seconds: int) -> bool:
        return await self._client.setnxex(key, value, seconds)
    
    async def delete(self, key: str) -> None:
        await self._client.delete(key)
    
    async def exists(self, key: str) -> bool:
        return await self._client.exists(key)
    
    async def incr(self, key: str) -> int:
        return await self._client.incr(key)
    
    async def decr(self, key: str) -> int:
        return await self._client.decr(key)
    
    async def incrby(self, key: str, amount: int) -> int:
        return await self._client.incrby(key, amount)
    
    async def decrby(self, key: str, amount: int) -> int:
        return await self._client.decrby(key, amount)
    
    async def hget(self, key: str, field: str) -> Any:
        return await self._client.hget(key, field)
    
    async def hset(self, key: str, field: str, value: Any) -> None:
        await self._client.hset(key, field, value)
    
    async def hgetall(self, key: str) -> Dict[str, Any]:
        return await self._client.hgetall(key)
    
    async def hdel(self, key: str, field: str) -> None:
        await self._client.hdel(key, field)
    
    async def hkeys(self, key: str) -> List[str]:
        return await self._client.hkeys(key)
    
    async def hvals(self, key: str) -> List[Any]:
        return await self._client.hvals(key)
    
    async def hlen(self, key: str) -> int:
        return await self._client.hlen(key)
    
    async def hsetnx(self, key: str, field: str, value: Any) -> bool:
        return await self._client.hsetnx(key, field, value)
    
    async def hmget(self, key: str, fields: List[str]) -> List[Any]:
        return await self._client.hmget(key, fields)
    
    async def hmset(self, key: str, mapping: Dict[str, Any]) -> None:
        await self._client.hmset(key, mapping)
    
    async def hmgetall(self, key: str) -> Dict[str, Any]:
        return await self._client.hmgetall(key)
    
    async def hmsetnx(self, key: str, mapping: Dict[str, Any]) -> bool:
        return await self._client.hmsetnx(key, mapping)
    
    async def hmgetall(self, key: str) -> Dict[str, Any]:
        return await self._client.hmgetall(key)
    
    async def keys(self, pattern: str) -> List[str]:
        return await self._client.keys(pattern)

    async def ttl(self, key: str) -> int:
        return await self._client.ttl(key)

    async def expire(self, key: str, seconds: int) -> bool:
        return await self._client.expire(key, seconds)


@lru_cache
def get_redis_client() -> RedisClient:
    return RedisClient()