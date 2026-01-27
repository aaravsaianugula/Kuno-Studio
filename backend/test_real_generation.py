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

log = get_logger("TestRealGen")

def run_test():
    log.info("=== Starting Real Generation Test ===")
    
    # 1. Ensure Models are Present
    log.info("Checking model availability...")
    try:
        ensure_models_available()
    except Exception as e:
        log.error(f"Failed to download/verify models: {e}")
        return

    # 2. Initialize Service
    # 2. Initialize Service (Moved to Generate block to save VRAM)
    # log.info("Initializing HeartMuLa Service...")
    # service = HeartMuLaService()
    service = None
    
    # 3. Define Prompt (Full Production K-Rock, ~2:30)
    prompt = {
        "title": "K_Rock_Full_Production",
        "genre": "Energetic Rock",
        "bpm": 170, # Fast, driving
        "duration_target": 150, # 2 mins 30 sec
        "structure": [
            {"type": "intro", "bars": 8, "text": "심장이 타는 냄새가 나 (Instrumental Build-up)"},
            {"type": "verse", "bars": 16, "text": "차가운 레일 위를 긁어대는 소리\n마찰열이 내 혈관을 태우고 있어\n어두운 터널 따위 그냥 씹어삼켜\n뒤를 돌아보는 건 약해빠진 짓이야"},
            {"type": "pre_chorus", "bars": 8, "text": "속도계의 바늘은 이미 Red Zone\n경고음은 리듬이 돼 더 크게 울려\n준비는 끝났어 미친 듯이 밟아"},
            {"type": "chorus", "bars": 16, "text": "폭주하는 강철의 짐승처럼\n이 밤의 적막을 찢어버려\n중력을 거스른 이 궤도 위에서\n나는 오직 앞만 보고 달려가"},
            {"type": "verse", "bars": 16, "text": "차가운 레일 위를 긁어대는 소리 (Verse 2 Variation)\n마찰열이 내 혈관을 태우고 있어\n(Driving Bass Line)"},
            {"type": "chorus", "bars": 16, "text": "폭주하는 강철의 짐승처럼\n이 밤의 적막을 찢어버려\n중력을 거스른 이 궤도 위에서\n나는 멈추지 않는 폭풍이야"},
            {"type": "bridge", "bars": 8, "text": "브레이크는 처음부터 없었어\n충돌한다 해도 상관없어\n끝까지 가볼 거야 재가 될 때까지"},
            {"type": "solo", "bars": 16, "text": "(Electric Guitar Solo - Shredding)"},
            {"type": "chorus", "bars": 16, "text": "폭주하는 강철의 짐승처럼\n이 밤의 적막을 찢어버려\n중력을 거스른 이 궤도 위에서\n나는 오직 앞만 보고 달려가"},
            {"type": "outro", "bars": 8, "text": "나는 멈추지 않는 폭풍이야 (Heavy Ending)"}
        ]
    }
    
    output_dir = "test_outputs"
    os.makedirs(output_dir, exist_ok=True)
    raw_path = f"{output_dir}/k_rock_full_raw.wav"
    final_path = f"{output_dir}/k_rock_full_mastered.wav"
    
    # 4. Generate
    if os.path.exists(raw_path):
        log.info(f"Raw file exists at {raw_path}. Skipping generation.")
    else:
        # Initialize service ONLY if needed (saves VRAM for enhancer)
        log.info("Initializing HeartMuLa Service...")
        service = HeartMuLaService()
        
        log.info(f"Generating 10s K-Pop track: {prompt}")
        print("DEBUG: Calling service.generate...", flush=True)
        try:
            # This will load model -> move to GPU/DirectML -> Generate -> Decode on CPU
            service.generate(prompt, raw_path)
            print("DEBUG: Returned from service.generate", flush=True)
            log.info(f"Raw generation successful: {raw_path}")
        except Exception as e:
            print(f"DEBUG: Exception caught: {e}", flush=True)
            log.error(f"Generation failed: {e}")
            import traceback
            traceback.print_exc()
            return


    # 5. Enhance (Studio Grade)
    log.info("Running Studio Enhancer...")
    try:
        from app.engine.studio_enhancer import StudioEnhancer
        studio = StudioEnhancer()
        studio.enhance(raw_path, final_path)
        log.info(f"Studio Enhancement successful: {final_path}")
    except Exception as e:
        log.error(f"Enhancement failed: {e}")
        import traceback
        traceback.print_exc()
        
    log.info("=== Test Complete ===")

if __name__ == "__main__":
    run_test()
