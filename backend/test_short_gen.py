import sys
import os
import asyncio
from pathlib import Path

# Fix path to allow importing app modules
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.engine.heartmula import HeartMuLaService
from app.utils.logger import get_logger

log = get_logger("TestShortGen")

def run_test():
    log.info("=== Starting Short Generation Test ===")
    
    # 3. Define Prompt (Very Short)
    prompt = {
        "title": "Short_Test",
        "genre": "Test",
        "bpm": 120,
        "duration_target": 5, # 5 seconds
        "structure": [
            {"type": "intro", "bars": 2, "text": "Test Start"}
        ]
    }
    
    output_dir = "test_outputs"
    os.makedirs(output_dir, exist_ok=True)
    raw_path = f"{output_dir}/short_test.wav"
    
    # 4. Generate
    log.info("Initializing HeartMuLa Service...")
    service = HeartMuLaService()
    
    log.info(f"Generating 5s track: {prompt}")
    print("DEBUG: Calling service.generate...", flush=True)
    try:
        service.generate(prompt, raw_path)
        print("DEBUG: Returned from service.generate", flush=True)
        log.info(f"Raw generation successful: {raw_path}")
    except Exception as e:
        print(f"DEBUG: Exception caught: {e}", flush=True)
        log.error(f"Generation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_test()
