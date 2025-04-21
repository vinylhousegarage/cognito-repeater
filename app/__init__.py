from fastapi import FastAPI
from app.config import Config

def create_app() -> FastAPI:
    app = FastAPI()

    config = Config()
    app.state.config = config

    return app
