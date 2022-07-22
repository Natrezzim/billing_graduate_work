
import os

import redis

redis_conn = redis.from_url(f'redis://{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}',
                            encoding="utf-8", decode_responses=True, db=0)
