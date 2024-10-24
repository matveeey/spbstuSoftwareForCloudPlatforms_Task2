from fastapi import FastAPI, HTTPException
from app.api.router import router
from app.api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/groups/openapi.json", docs_url="/api/v1/groups/docs")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(router, prefix='/api/v1/groups', tags=['groups'])