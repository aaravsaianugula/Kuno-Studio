from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
from app.engine.heartmula import HeartMuLaService
# from app.engine.heartcodec import HeartCodecService # Deprecated: Pipeline handles codec
# from app.engine.enhancer import AudioEnhancer # Deprecated
from app.engine.studio_enhancer import StudioEnhancer
from app.utils.logger import get_logger
import uuid
import os
import glob
import shutil
import json
import sys
import contextlib
import re
import time

router = APIRouter()
log = get_logger("GenerationRouter")

heartmula = HeartMuLaService()
enhancer = StudioEnhancer()

# Request Models (Same as before)
class SongStructureItem(BaseModel):
    type: str 
    bars: int
    text: Optional[str] = None
    description: Optional[str] = None
    singer_voice: Optional[str] = None
    dynamic: Optional[str] = "medium"

class MasteringConfig(BaseModel):
    cleanliness: str = "normal"
    clarity: str = "normal"
    bass_boost: bool = False

class GenerationRequest(BaseModel):
    title: str
    bpm: int
    genre: str
    duration_target: Optional[int] = 30
    structure: List[SongStructureItem]
    mastering: Optional[MasteringConfig] = None
    
    # Optional fields for richer prompts (prevent validation errors)
    inspiration: Optional[str] = None
    vocal_processing: Optional[str] = None
    generation_parameters: Optional[dict] = None

class GenerationResponse(BaseModel):
    task_id: str
    status: str
    message: str

# Global task store (InMemory but persistent)
TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump(TASKS, f)

TASKS = load_tasks() 

def update_task(task_id, data):
    if task_id not in TASKS:
        TASKS[task_id] = {}
    TASKS[task_id].update(data)
    save_tasks()

import sys
import contextlib
import re
import time

# ... existing code ...

class LogCapture:
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.last_save = 0
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        
    def write(self, text: str):
        # 1. Write to real console so we don't lose visibility
        sys.__stdout__.write(text)
        sys.__stdout__.flush()
        
        # 2. Process for UI
        if self.task_id not in TASKS: return
        
        # Clean ANSI codes for cleaner UI (optional)
        clean_text = self.ansi_escape.sub('', text)
        
        logs = TASKS[self.task_id].get("logs", [])
        if not logs: logs.append("")
        
        for char in clean_text:
            if char == '\r':
                # Carriage return: clear the current line (simulate overwriting)
                if logs: logs[-1] = ""
            elif char == '\n':
                # Newline: commit current line and start new
                logs.append("")
            else:
                # Regular char: append to last line
                if not logs: logs.append("")
                logs[-1] += char
                
        TASKS[self.task_id]["logs"] = logs
        
        # Throttle save to disk (once per second)
        now = time.time()
        if now - self.last_save > 1.0:
            save_tasks()
            self.last_save = now

    def flush(self):
        sys.__stdout__.flush()

def process_generation_task(task_id: str, request: GenerationRequest):
    capture = LogCapture(task_id)
    
    # helper for specific milestones (still useful for "message" field updates)
    def update_status(msg: str, progress: int = None):
         data = {"message": msg}
         if progress is not None:
             data["progress"] = progress
         update_task(task_id, data)
         # We do NOT append to logs here manually anymore, strictly use print()
         print(f"[{task_id}] {msg}")

    # Wrap execution in redirect
    with contextlib.redirect_stdout(capture), contextlib.redirect_stderr(capture):
        # Init
        update_task(task_id, {"status": "processing"})
        update_status("Initializing...", 5)
        print(f"Processing task for song: {request.title}")
        
        try:
            output_dir = "generated_songs"
            os.makedirs(output_dir, exist_ok=True)
            raw_path = f"{output_dir}/{task_id}_raw.wav"
            final_path = f"{output_dir}/{task_id}_{request.title.replace(' ', '_')}.wav"
            
            # 1. Generate
            print("Initializing HeartMuLa pipeline...")
            update_status("Initializing HeartMuLa pipeline...", 10)
            
            def progress_handler(current, total):
                pct = int((current / total) * 100)
                global_progress = 20 + int(pct * 0.5) 
                
                # Update status/progress only
                message = f"Generating audio tokens... {current}/{total} frames"
                update_task(task_id, {"status": "generating", "message": message, "progress": global_progress})
                # Note: We rely on tqdm printing to stdout for the granular logs!
                
            print("Starting generation sequence...")
            heartmula.generate(request.dict(), raw_path, video_callback=progress_handler)
            print("Generation sequence completed.")
            
            # 2. Enhance
            update_status("Enhancing audio (Studio Mode)...", 70)
            
            enhancer.enhance(raw_path, final_path)
            
            print(f"Task completed successfully. Final output: {final_path}")
            update_task(task_id, {"status": "completed", "message": "Ready to play.", "progress": 100})
            
        except Exception as e:
            print(f"Task {task_id} failed: {e}")
            import traceback
            traceback.print_exc() # This will be captured!
            update_task(task_id, {"status": "failed", "message": str(e), "progress": 0})
            update_task(task_id, {"status": "failed", "message": str(e), "progress": 0})
            save_tasks()
        finally:
            # Ensure VRAM is always cleaned up
            heartmula.reset()

@router.post("/generate", response_model=GenerationResponse)
async def generate_song(request: GenerationRequest, background_tasks: BackgroundTasks):

    from app.utils.project_state import save_project_state
    
    task_id = str(uuid.uuid4())
    log.info(f"Received generation request. ID: {task_id}")
    
    # Init Status with empty logs
    update_task(task_id, {"status": "queued", "message": "Waiting for worker...", "progress": 0, "logs": []})

    # Update Shared Project State IMMEDIATELY so UI reflects it
    new_state = {
        "title": request.title,
        "genre": request.genre,
        "bpm": request.bpm,
        "duration_target": request.duration_target,
        "structure": [item.dict() for item in request.structure]
    }
    save_project_state(new_state)
    
    background_tasks.add_task(process_generation_task, task_id, request)
    return GenerationResponse(task_id=task_id, status="queued", message="Started.")

@router.get("/project")
async def get_current_project():
    from app.utils.project_state import load_project_state
    state = load_project_state()
    if not state:
        return {"title": "New Project", "structure": []}
    return state
    
@router.get("/status/{task_id}")
async def get_status(task_id: str):
    return TASKS.get(task_id, {"status": "unknown", "message": "Task not found", "progress": 0, "logs": []})

@router.get("/library")
async def get_library():
    """List all generated songs."""
    output_dir = "generated_songs"
    if not os.path.exists(output_dir):
        return []
    
    files = glob.glob(f"{output_dir}/*.wav")
    # Filter out raw files if you want only finalized ones
    # files = [f for f in files if "_raw" not in f]
    
    songs = []
    for f in files:
        filename = os.path.basename(f)
        songs.append({
            "filename": filename,
            "path": f,
            "size": os.path.getsize(f)
        })
    return songs

@router.get("/audio/{filename}")
async def get_audio_file(filename: str):
    """Serve an audio file."""
    file_path = os.path.join("generated_songs", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="audio/wav")

@router.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    """Handle vocal input upload."""
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{uuid.uuid4()}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"filename": file.filename, "status": "uploaded", "path": file_path}
