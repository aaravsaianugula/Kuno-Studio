import os
from pathlib import Path
from huggingface_hub import snapshot_download
from app.utils.logger import get_logger
from app.config import settings
import shutil

log = get_logger("ModelLoader")

def download_repo(repo_id: str, local_dir: Path, allow_patterns=None):
    log.info(f"Checking {repo_id} in {local_dir}...")
    try:
        snapshot_download(
            repo_id=repo_id,
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            resume_download=True,
            allow_patterns=allow_patterns
        )
        log.info(f"Verified {repo_id}.")
    except Exception as e:
        log.error(f"Failed to download {repo_id}: {e}")
        raise e

def ensure_models_available():
    """
    Ensures the 'models' directory structure matches HeartLib requirements:
    ./models/
       ├── HeartCodec-oss/
       ├── HeartMuLa-oss-3B/
       ├── gen_config.json (from HeartMuLaGen)
       └── tokenizer.json  (from HeartMuLaGen)
    """
    base_dir = settings.MODELS_DIR # e.g., backend/models
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. HeartMuLaGen (Base configs like tokenizer.json, gen_config.json)
    # Download to root of models dir
    log.info("Downloading Base Configs (HeartMuLaGen)...")
    download_repo("HeartMuLa/HeartMuLaGen", base_dir, allow_patterns=["*.json", "*.model"])

    # 2. HeartMuLa-oss-3B (The Main Model)
    # Target: ./models/HeartMuLa-oss-3B
    hm_dir = base_dir / "HeartMuLa-oss-3B"
    log.info("Downloading HeartMuLa 3B...")
    download_repo("HeartMuLa/HeartMuLa-oss-3B", hm_dir)
    
    # 3. HeartCodec-oss (The Audio Codec)
    # Target: ./models/HeartCodec-oss
    hc_dir = base_dir / "HeartCodec-oss"
    log.info("Downloading HeartCodec...")
    download_repo("HeartMuLa/HeartCodec-oss", hc_dir)

    log.info("All models verified.")
