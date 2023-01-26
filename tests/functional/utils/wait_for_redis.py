from functional.src.settings import settings

import time

from redis import Redis

if __name__ == '__main__':
    redis_client = Redis(
        host=settings.redis_host, port=settings.redis_port,
        decode_responses=True
    )

    while True:
        if redis_client.ping():
            break
        time.sleep(1)
