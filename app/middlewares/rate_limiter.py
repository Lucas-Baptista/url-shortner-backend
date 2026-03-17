from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from app.database.redis import get_redis


class RateLimiterMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, limit: int = 10, window: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window = window

    async def dispatch(self, request: Request, call_next):

        redis = get_redis()

        ip = request.client.host

        key = f"rate_limit:{ip}"

        current = redis.incr(key)

        if current == 1:
            redis.expire(key, self.window)

        if current > self.limit:
            raise HTTPException(
                status_code=429,
                detail="Too many requests"
            )

        response = await call_next(request)
        return response