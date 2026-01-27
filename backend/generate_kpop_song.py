import sys
import os
import asyncio
from pathlib import Path

# Fix path to allow importing app modules
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.engine.heartmula import HeartMuLaService
from app.engine.enhancer import AudioEnhancer
from app.engine.model_loader import ensure_models_available
from app.utils.logger import get_logger

log = get_logger("GenKPop")

def run_generation():
    log.info("=== Starting K-Pop Generation ===")
    
    # 1. Ensure Models are Present
    log.info("Checking model availability...")
    try:
        ensure_models_available()
    except Exception as e:
        log.error(f"Failed to download/verify models: {e}")
        return

    # 2. Define Prompt
    # Style: pH-1 (Melodic Rap, Groovy, Chill) + Kochi no Kento (Upbeat Melancholy)
    # Voice: Male, Soothing
    # ... (imports)
    from app.utils.project_state import save_project_state

    # ...

    prompt = {
        "title": "Neon_Nights",
        "genre": "K-Pop, City Pop, Melodic Rap, R&B, Groovy, Upbeat Melancholy",
        "bpm": 110,
        "duration_target": 60, # 1 minute
        "structure": [
            {"type": "intro", "bars": 4, "text": "(Groovy Bass & Synth Intro) Yeah, let's go.", "color": "bg-indigo-400"},
            {"type": "verse", "bars": 8, "text": "Walking down the street light's low\nNobody knows where we gonna go\nFeeling the vibe, feeling the flow\nJust you and me, taking it slow", "color": "bg-violet-400"},
            {"type": "pre_chorus", "bars": 4, "text": "Heartbeat racing, can't deny\nLighting up the midnight sky", "color": "bg-fuchsia-400"},
            {"type": "chorus", "bars": 8, "text": "Party people in the place to be\nDance with me, set your spirit free\n5, 4, 3, 2, 1, let's fly\nHai yorokonde, touch the sky", "color": "bg-pink-500"},
            {"type": "verse", "bars": 8, "text": "Smooth like butter, cool like ice\nEvery moment feels so nice\nNo worries now, just roll the dice\nLiving our best life, that's the price", "color": "bg-violet-400"},
            {"type": "outro", "bars": 4, "text": "Yeah, fade away...\n(Soothing hums)\nGoodnight.", "color": "bg-indigo-300"}
        ]
    }

    # Save state for Frontend
    log.info("Saving project state for frontend...")
    save_project_state(prompt)

    
    output_dir = "backend/test_outputs"
    os.makedirs(output_dir, exist_ok=True)
    raw_path = f"{output_dir}/kpop_custom_raw.wav"
    final_path = f"{output_dir}/kpop_custom_mastered.wav"
    
    # 3. Generate
    if os.path.exists(raw_path):
        log.info(f"Raw file exists at {raw_path}. Skipping generation to save time/resources. Delete file to regenerate.")
    else:
        log.info("Initializing HeartMuLa Service...")
        service = HeartMuLaService()
        
        log.info(f"Generating 60s K-Pop track: {prompt['title']}")
        try:
            service.generate(prompt, raw_path)
            log.info(f"Raw generation successful: {raw_path}")
        except Exception as e:
            log.error(f"Generation failed: {e}")
            import traceback
            traceback.print_exc()
            return

    # 4. Enhance
    log.info("Running Studio Enhancer...")
    try:
        # Re-import to ensure clean state if possible, though not strictly necessary
        from app.engine.studio_enhancer import StudioEnhancer
        studio = StudioEnhancer()
        studio.enhance(raw_path, final_path)
        log.info(f"Studio Enhancement successful: {final_path}")
    except Exception as e:
        log.error(f"Enhancement failed: {e}")
        import traceback
        traceback.print_exc()
        
    log.info("=== Generation Complete ===")

if __name__ == "__main__":
    run_generation()
