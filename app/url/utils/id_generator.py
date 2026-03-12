from app.database.redis import get_redis

COUNTER_KEY = "url:id"
INITIAL_VALUE = 15000000

def get_next_id() -> int:
    redis = get_redis()
    
    redis.setnx(COUNTER_KEY, INITIAL_VALUE)
    
    return redis.incr(COUNTER_KEY)