from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.middlewares.rate_limiter import RateLimiterMiddleware
from app.url.routes.url_routes import router as url_router

app = FastAPI()

# middleware
app.add_middleware(
    RateLimiterMiddleware,
    limit=20,
    window=60
)

# rotas
app.include_router(url_router)