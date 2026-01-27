import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "backend", "heartlib", "src"))

from backend.app.config import settings
from backend.heartlib.src.heartlib.heartmula.modeling_heartmula import HeartMuLa, HeartMuLaConfig

def inspect():
    model_path = os.path.join(settings.MODELS_DIR, "HeartMuLa-oss-3B")
    print(f"Loading config from {model_path}")
    try:
        config = HeartMuLaConfig.from_pretrained(model_path)
        # Load meta model to save time/ram
        from accelerate import init_empty_weights
        with init_empty_weights():
             model = HeartMuLa(config)
        
        print("\n=== Module structure ===")
        for name, _ in model.named_modules():
             print(name)
             
        print("\n=== Parameter structure ===")
        for name, _ in model.named_parameters():
             print(name)
             
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect()
