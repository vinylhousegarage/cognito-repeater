from fastapi import FastAPI
from app.config import Config
from app.routers import auth, health

def create_app() -> FastAPI:
    app = FastAPI()

    config = Config()
    app.state.config = config

    app.include_router(auth.router)
    app.include_router(health.router)

    return app
