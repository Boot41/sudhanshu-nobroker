import path_setup
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.api.auth_routes import auth_router
from server.api.property_routes import property_router, application_router
from server.api.registereduser_routes import router as registereduser_router
from server.api.tenant_routes import router as tenant_router
from server.db.database import create_tables, test_connection
from server.core.config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME, 
    description=settings.APP_DESCRIPTION, 
    version=settings.APP_VERSION
)

# CORS for local development (Vite dev server)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    logger.info("Starting up application...")
    if test_connection():
        create_tables()
    else:
        logger.error("Database connection failed. Aborting startup.")
        # In a real application, you might want to exit or prevent the app from starting
        # For now, we'll just log the error.

# Include routers
app.include_router(auth_router)
app.include_router(property_router)
app.include_router(application_router)
app.include_router(registereduser_router)
app.include_router(tenant_router)

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.APP_NAME}", "version": settings.APP_VERSION}
