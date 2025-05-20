import os
from blake3 import blake3

from redis.asyncio import Redis

class RedisClient:
    """
    Redis client for managing important data.
    """
    def __init__(self, redis_url: str = None):
        self.redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis = Redis.from_url(
            self.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )

    async def save_user_token(self, user_id: int, token: str, expire_seconds: int = 3600):
        await self.redis.set(f"user_token:{user_id}", token, ex=expire_seconds)

    async def get_user_token(self, user_id: int):
        return await self.redis.get(f"user_token:{user_id}")

    async def delete_user_token(self, user_id: int):
        await self.redis.delete(f"user_token:{user_id}")

    async def save_user_callback_data(self, user_id: int, callback_data: str, expire_seconds: int = 86400):
        cb_hash = str(blake3(callback_data.encode()).hexdigest(length=27))
        await self.redis.set(f"user_callback_data:{user_id}_{cb_hash}", callback_data, ex=expire_seconds)
        return cb_hash

    async def get_user_callback_data(self, user_id: int, cb_hash: str):
        return await self.redis.get(f"user_callback_data:{user_id}_{cb_hash}")

    async def close(self):
        await self.redis.close()
