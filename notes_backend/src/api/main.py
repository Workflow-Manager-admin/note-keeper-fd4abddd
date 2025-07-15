from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .routes_auth import router as auth_router
from .routes_notes import router as notes_router

app = FastAPI(
    title="Note Keeper API",
    description="API for user authentication and note CRUD.",
    version="1.0.0",
    openapi_tags=[
        {"name": "auth", "description": "Operations for user registration and login."},
        {"name": "notes", "description": "CRUD operations for user notes."},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/", tags=["utility"], summary="Health Check", description="Service status and healthcheck endpoint")
def health_check():
    return {"message": "Healthy"}

app.include_router(auth_router)
app.include_router(notes_router)
