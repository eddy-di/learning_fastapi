from redis import Redis

from app.config import REDIS_HOST, REDIS_PORT


def create_redis():
    '''
    Connect to Redis database, using host and port variables from `.env`
    '''
    # return ConnectionPool.from_url(redis_url_connection)
    return Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)


# pool = create_redis()


# def get_redis() -> Redis:
    # '''
    # Get Redis using created connection from `create_redis` function\n
    # that utilizes url connection specified in `config.py`.
    # '''
    # return Redis(pool)
