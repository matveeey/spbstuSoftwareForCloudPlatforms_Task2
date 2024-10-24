from fastapi import FastAPI
from app.api.router import router

app = FastAPI(openapi_url="/api/v1/openapi.json", docs_url="/api/v1/docs")

app.include_router(router, prefix='/api/v1', tags=['university'])