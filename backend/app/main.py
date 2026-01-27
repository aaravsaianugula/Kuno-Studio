from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.utils.logger import get_logger
from app.routers import generation, system
from app.engine.model_loader import ensure_models_available
import asyncio

# ... (omitted)

app = FastAPI(
    title="Kuno AI Engine",
    description="Backend for Kuno Music Production AI",
    version="0.1.0"
)

# CORS (Allow Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

log = get_logger("Main")

# Routers
app.include_router(generation.router, prefix="/api/v1", tags=["generation"])
app.include_router(system.router, prefix="/api/v1", tags=["system"])

@app.on_event("startup")
async def startup_event():
    log.info("Starting Kuno AI Engine...")
    
    # Initialize status
    app.state.status = "initializing"
    
    # Run model loading in background so API is responsive immediately
    asyncio.create_task(background_init())

async def background_init():
    try:
        log.info("Running background initialization...")
        # ensure_models_available might trigger downloads, which is slow
        # We run it here to not block the server startup
        # use run_in_executor to avoid blocking the event loop with synchronous code
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, ensure_models_available)
        
        app.state.status = "ready"
        log.info("Background initialization complete. System READY.")
    except Exception as e:
        log.error(f"Model initialization failed: {e}")
        app.state.status = "error"
    
    log.info("Startup complete. Ready to rock.")

@app.get("/")
def read_root():
    return {"message": "Welcome to Kuno AI API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, reload_excludes=["*.json"])
