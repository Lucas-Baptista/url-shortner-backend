import os

from app.database.redis import get_redis

counter_key = os.getenv("COUNTER_KEY")
initial_value = os.getenv("INITIAL_VALUE")

if not counter_key or not initial_value:
    raise ValueError("COUNTER_KEY or INITIAL_VALUE is not defined in environment variables")

def get_next_id() -> int:
    redis = get_redis()
    
    redis.setnx(counter_key, initial_value)
    
    return redis.incr(counter_key)