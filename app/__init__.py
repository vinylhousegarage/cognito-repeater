from fastapi import FastAPI
from app.config import Config
from app.routers import api_docs, auth, errors, root

def create_app() -> FastAPI:
    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    config = Config()
    app.state.config = config

    app.include_router(api_docs.router)
    app.include_router(auth.router)
    app.include_router(errors.router)
    app.include_router(root.router)

    return app
