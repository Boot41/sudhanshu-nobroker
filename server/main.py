from fastapi import FastAPI
from auth_routes import auth_router
from database import create_tables, test_connection
from config import app_config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=app_config.APP_NAME, 
    description=app_config.APP_DESCRIPTION, 
    version=app_config.APP_VERSION
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

@app.get("/")
def read_root():
    return {"message": f"Welcome to {app_config.APP_NAME}", "version": app_config.APP_VERSION}
