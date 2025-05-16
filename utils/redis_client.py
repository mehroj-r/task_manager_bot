import os
from redis.asyncio import Redis

class RedisClient:
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

    async def close(self):
        await self.redis.close()
