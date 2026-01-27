from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "Kuno AI Music Engine"
    VERSION: str = "0.1.0"
    
    # Hardware Config
    DEVICE_BACKEND: str = "privateuseone" # DirectML often uses this or 'cpu' mapped. For torch-directml specifically it's often DML. 
    # NOTE: torch-directml uses torch.device("privateuseone:0") usually mapped to DML.
    # We will detect this in logic.
    
    USE_GPU_GENERATION: bool = True
    USE_CPU_DECODING: bool = True
    
    # Model Paths - Defaulting to local cache or relative paths
    MODELS_DIR: Path = Path("./models")
    HEARTMULA_MODEL_ID: str = "HeartMuLa/HeartMuLa-RL-oss-3B"
    HEARTCODEC_MODEL_PATH: str = "./models/heartcodec"
    
    # Streaming Config
    MAX_GPU_LAYERS: int = 10 # Reduced for 50% compute (~half layers active)
    VRAM_TARGET_USAGE: float = 0.50 # ~4GB target, stays under 6GB on 8GB Card
    
    class Config:
        env_file = ".env"

settings = Settings()
