
import time
import torch
import os
import sys

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.engine.heartmula import HeartMuLaService
from app.utils.logger import get_logger

# Setup logging
log = get_logger("Benchmark")

def benchmark():
    log.info("Starting HeartMuLa Benchmark...")
    
    service = HeartMuLaService()
    
    # Measure Load Time
    start_load = time.time()
    service.load_pipeline()
    end_load = time.time()
    log.info(f"Pipeline Loaded in {end_load - start_load:.2f} seconds.")
    
    # Prompt
    prompt = {
        "genre": "Pop",
        "title": "Benchmark Track",
        "duration_target": 10, # 10 seconds
        "structure": [
            {"type": "Verse", "text": "Testing performance now"}
        ]
    }
    
    output_path = os.path.join(os.getcwd(), "benchmark_output.wav")
    
    # Measure Generation Time
    log.info("Starting Generation...")
    start_gen = time.time()
    try:
        service.generate(prompt, output_path)
    except Exception as e:
        import traceback
        traceback.print_exc()
        log.error(f"Generation failed: {e}")
        return

    end_gen = time.time()
    duration = end_gen - start_gen
    
    log.info(f"Generation Complete in {duration:.2f} seconds.")
    log.info(f"Speed: {10 / duration:.2f} seconds of audio / second of compute (Approx)")

if __name__ == "__main__":
    benchmark()
