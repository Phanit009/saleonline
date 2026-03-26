from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from contextlib import asynccontextmanager

from .config import settings
from .utils.database import connect_to_mongo, close_mongo_connection
from .routes import auth, users, content, media, settings as settings_route, analytics

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(
    title="Ectomeres CMS API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.storage_type == "local" and os.path.exists(settings.storage_path):
    app.mount("/uploads", StaticFiles(directory=settings.storage_path), name="uploads")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(content.router)
app.include_router(media.router)
app.include_router(settings_route.router)
app.include_router(analytics.router)

@app.get("/")
async def root():
    return {"message": "Ectomeres CMS API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
