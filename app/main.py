from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "API rodando 🚀"}


@app.get("/users")
def get_users():
    return [
    {"id": 1, "name": "Lucas"},
    {"id": 2, "name": "Maria"}
    ]
