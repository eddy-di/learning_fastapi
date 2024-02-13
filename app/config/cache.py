import redis.asyncio as redis

from app.config.base import REDIS_HOST, REDIS_PORT


async def create_redis():
    '''Connect to async Redis database, using host and port variables from `.env`'''

    async with redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0) as session:
        yield session
