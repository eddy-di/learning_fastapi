from redis import Redis

from app.config.base import REDIS_HOST, REDIS_PORT


def create_redis():
    '''
    Connect to Redis database, using host and port variables from `.env`
    '''
    return Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
