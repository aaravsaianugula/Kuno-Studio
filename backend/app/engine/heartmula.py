import torch
import torch.nn as nn
try:
    import torch_directml
    has_directml = True
except ImportError:
    has_directml = False

from heartlib import HeartMuLaGenPipeline
from app.config import settings
from app.utils.logger import get_logger
import os

import gc

log = get_logger("HeartMuLaService")

class HeartMuLaService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HeartMuLaService, cls).__new__(cls)
            cls._instance.pipeline = None
            # HeartLib expects the path to the folder containing gen_config.json etc.
            # which is now settings.MODELS_DIR itself.
            cls._instance.model_path = str(settings.MODELS_DIR)
        return cls._instance

    def __init__(self):
        # Init logic is now in __new__ to prevent re-initialization
        pass
        
    def reset(self):
        """Force cleanup of VRAM/RAM resources."""
        log.info("Resetting HeartMuLa Service...")
        if self.pipeline:
            # Manually unload internal components if possible
            if hasattr(self.pipeline, "_unload"):
                self.pipeline.lazy_load = True # Force lazy load to enable unload
                self.pipeline._unload()
            
            del self.pipeline
            self.pipeline = None
            
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        elif has_directml:
             # DirectML cleanup if applicable
             pass
             
        log.info("System Reset Complete. Resources freed.")
        
    def _get_devices(self):
        """
        Returns device configuration:
        - mula: DirectML (if available) or CUDA/CPU
        - codec: CPU (Strictly requested by user)
        """
        devices = {}
        
        # Mula Device
        if has_directml:
            log.info("DirectML detected. Using DirectML for HeartMuLa.")
            devices["mula"] = torch_directml.device()
        elif torch.cuda.is_available():
             log.info("CUDA detected. Using CUDA for HeartMuLa.")
             devices["mula"] = torch.device("cuda")
        else:
             log.warning("No GPU acceleration found. Mula defaulting to CPU.")
             devices["mula"] = torch.device("cpu")
             
        # Codec Device - Explicitly CPU
        log.info("Codec set to CPU.")
        devices["codec"] = torch.device("cpu")
        
        return devices

    def load_pipeline(self):
        if self.pipeline:
            return
            
        log.info(f"Loading HeartMuLa Pipeline from {self.model_path}...")
        devices = self._get_devices()
        
        try:
            # Determine dtype based on device
            # DirectML/AMD 6600XT (8GB) -> float16 is REQUIRED for memory
            # Full model (3B) exceeds 8GB VRAM, so we use LAYER STREAMING:
            # - Load to CPU
            # - Stream layers to GPU during forward pass
            
            mula_dtype = torch.float32
            mula_device = torch.device("cpu")  # Layer streaming - load to CPU first
            use_dml_streaming = False
            
            if has_directml:
                mula_dtype = torch.float16
                use_dml_streaming = True  # Will stream layers to DirectML
                log.info("DirectML detected. Using layer streaming for GPU acceleration (float16).")
            elif torch.cuda.is_available():
                mula_dtype = torch.float16
                log.info("CUDA detected. Using layer streaming for GPU acceleration (float16).")
            else:
                log.warning("No GPU found. Using CPU (float32).")
                
            codec_dtype = torch.float32 # Codec stays on CPU
            
            # Load everything to CPU, streaming happens in modeling code
            load_devices = {
                "mula": mula_device,
                "codec": torch.device("cpu")
            }
            
            log.info(f"Initializing pipeline with mula_dtype={mula_dtype} (layer streaming enabled)...")

            self.pipeline = HeartMuLaGenPipeline.from_pretrained(
                self.model_path,
                device=load_devices, 
                dtype={
                    "mula": mula_dtype, 
                    "codec": codec_dtype  
                },
                version="3B",
                lazy_load=False,
            )
            
            # Post-loading setup 
            if has_directml:
                log.info("Pipeline loaded. DirectML acceleration active.")
            else:
                log.info("Pipeline loaded.")
            
        except Exception as e:
            log.error(f"Failed to load pipeline: {e}")
            raise e

    def generate(self, prompt_dict: dict, output_path: str, video_callback=None):
        """
        Generates music and saves to output_path.
        Returns the path on success.
        video_callback: Optional function(current_step, total_steps)
        """
        if not self.pipeline:
            self.load_pipeline()
            
        # Parse prompt dict to args for pipeline
        # Assuming prompt_dict keys align roughly or we parse them
        
        # Default behavior: construct "lyrics" or description based on structure
        # For Kuno's JSON structure, we might flatten it to a description string or use lyrics if provided.
        
        # Simplification: Use the 'description' of the first intro/verse as general vibe
        # or concatenate them.
        
        description = prompt_dict.get("genre", "Pop") + " " + \
                      prompt_dict.get("title", "")
                      
        # Collect lyrics if any
        lyrics = ""
        for part in prompt_dict.get("structure", []):
            if part.get("text"):
                lyrics += f"[{part['type']}] {part['text']}\n"
                
        # If no lyrics, use description as tags/prompt
        # ensure lyrics is never None (fix for pipelines/music_generation.py crash)
        inputs = {
            "lyrics": lyrics if lyrics else "", 
            "tags": description
        }
        
        log.info(f"Generating for inputs: {inputs}")
        
        try:
            with torch.no_grad():
                 self.pipeline(
                    inputs,
                    max_audio_length_ms=int(prompt_dict.get("duration_target", 30)) * 1000, 
                    save_path=output_path,
                    topk=50,
                    temperature=1.0,
                    cfg_scale=1.5,
                    progress_callback=video_callback
                )
            log.info(f"Generation saved to {output_path}")
            return output_path
            
        except Exception as e:
            log.error(f"Generation failed: {e}")
            raise e
