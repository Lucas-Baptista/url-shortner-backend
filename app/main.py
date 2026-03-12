from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.url.routes.url_routes import router as url_router

app = FastAPI()

app.include_router(url_router)