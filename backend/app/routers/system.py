from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
import psutil
import torch
from pathlib import Path
from app.utils.logger import get_logger
from app.engine.heartmula import HeartMuLaService
import os
import asyncio
import time

router = APIRouter()
log = get_logger("SystemRouter")

@router.get("/stats")
async def get_system_stats(request: Request):
    """
    Returns system utilization stats for the frontend monitor.
    """
    try:
        cpu_usage = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory()
        ram_usage = memory.percent
        
        # GPU Stats (Estimates for DirectML/AMD)
        gpu_usage = 0 
        vram_usage = 0
        
        # Get status from app state if available, else default to ready
        status = getattr(request.app.state, "status", "ready")
        
        return {
            "cpu": cpu_usage,
            "ram": ram_usage,
            "gpu": gpu_usage, 
            "vram": vram_usage,
            "gpu_name": "AMD Radeon RX 6600 XT",
            "status": status
        }
    except Exception as e:
        log.error(f"Error getting stats: {e}")
        return {"error": str(e), "status": "error"}

from app.config import settings
from pydantic import BaseModel
from typing import Optional


@router.get("/config")
async def get_config():
    """Get current system configuration."""
    return {
        "device": settings.DEVICE_BACKEND,
        "use_gpu": settings.USE_GPU_GENERATION,
        "use_cpu_decoding": settings.USE_CPU_DECODING,
        "model_id": settings.HEARTMULA_MODEL_ID,
        "vram_target": settings.VRAM_TARGET_USAGE
    }

class ConfigUpdate(BaseModel):
    use_gpu: Optional[bool] = None
    use_cpu_decoding: Optional[bool] = None
    vram_target: Optional[float] = None

@router.post("/config")
async def update_config(config: ConfigUpdate):
    """Update system configuration."""
    if config.use_gpu is not None:
        settings.USE_GPU_GENERATION = config.use_gpu
    if config.use_cpu_decoding is not None:
        settings.USE_CPU_DECODING = config.use_cpu_decoding
    if config.vram_target is not None:
        settings.VRAM_TARGET_USAGE = config.vram_target
    
    return {"status": "updated", "config": await get_config()}



def kill_process():
    """Wait briefly then force kill the process."""
    time.sleep(1)
    log.warning("Forcing process exit to ensure clean restart...")
    os._exit(0)

@router.post("/reset")
async def reset_system(background_tasks: BackgroundTasks):
    """
    Emergency Reset: Clears VRAM and triggers a backend reload.
    Forces the process to exit to ensure a clean slate.
    """
    try:
        service = HeartMuLaService()
        service.reset()
        
        # Trigger Uvicorn Reload by touching main.py (Standard method)
        current_file = Path(__file__).resolve()
        main_py = current_file.parent.parent / "main.py"
        
        if main_py.exists():
            log.warning(f"Touching {main_py} to trigger reload...")
            os.utime(main_py, None)
            
            # Use BackgroundTask to kill process AFTER response is sent
            background_tasks.add_task(kill_process)
            
            return {"status": "ok", "message": "System resetting... Backend will reload."}
        else:
             return {"status": "error", "message": "Could not find main.py to trigger reload."}

    except Exception as e:
        log.error(f"Reset failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/prompt")
async def get_claude_prompt():
    """Get the current Claude prompt instructions."""
    try:
        # Resolve path relative to this file: .../backend/app/routers/system.py
        # We need to go up to .../Kuno/CLAUDE_PROMPT.md
        # system.py -> routers -> app -> backend -> Kuno
        prompt_path = Path(__file__).resolve().parent.parent.parent.parent / "CLAUDE_PROMPT.md"
        
        if not prompt_path.exists():
            # Fallback to current working directory
            prompt_path = Path.cwd() / "CLAUDE_PROMPT.md"
            
        if not prompt_path.exists():
             raise FileNotFoundError(f"CLAUDE_PROMPT.md not found at {prompt_path}")

        content = prompt_path.read_text(encoding="utf-8")
        return {"content": content}
    except Exception as e:
        log.error(f"Error reading prompt file: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to read prompt file: {str(e)}")
