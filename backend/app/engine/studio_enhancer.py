import os
import torch
import numpy as np
import soundfile as sf
import librosa
from pathlib import Path
from app.utils.logger import get_logger
from app.config import settings

# Import Pedalboard
try:
    from pedalboard import Pedalboard, Compressor, Limiter, HighpassFilter, LowShelfFilter, HighShelfFilter, Gain
    from pedalboard.io import AudioFile
    HAS_PEDALBOARD = True
except ImportError:
    HAS_PEDALBOARD = False

# Import AudioSR
try:
    from audiosr import build_model, super_resolution
    HAS_AUDIOSR = True
except ImportError:
    HAS_AUDIOSR = False

log = get_logger("StudioEnhancer")

class StudioEnhancer:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # DirectML check for AudioSR (might need CPU if not supported)
        try:
            import torch_directml
            self.device = torch_directml.device()
            # AudioSR might not like DirectML, use CPU fallback if needed
        except ImportError:
            pass
            
        self.audiosr_model = None
        self.mastering_chain = None
        
    def _load_models(self):
        """Lazy load models only when needed."""
        if self.audiosr_model:
            return

        if HAS_AUDIOSR:
            log.info("Loading AudioSR model...")
            try:
                # AudioSR: 'basic' model is efficient and good quality
                self.audiosr_model = build_model(model_name="basic", device=self.device)
                log.info("AudioSR model loaded.")
            except Exception as e:
                log.error(f"Failed to load AudioSR: {e}")
                
        if HAS_PEDALBOARD and not self.mastering_chain:
            # Studio Grade Mastering Chain
            self.mastering_chain = Pedalboard([
                # 1. Clean up low end
                HighpassFilter(cutoff_frequency_hz=30),
                
                # 2. Gentle compression (Glue)
                Compressor(threshold_db=-12, ratio=2.5, attack_ms=30, release_ms=100),
                
                # 3. Tonal Balance (Smiley Curve - slight boost to lows and highs)
                LowShelfFilter(cutoff_frequency_hz=100, gain_db=2.0),
                HighShelfFilter(cutoff_frequency_hz=10000, gain_db=2.0),
                
                # 4. Limiting (Maximize Loudness without clipping)
                Limiter(threshold_db=-0.5, release_ms=60)
            ])

    def enhance(self, input_path: str, output_path: str, enable_upscale: bool = True):
        self._load_models()
        log.info(f"Starting studio enhancement for {input_path}...")
        
        # 1. AudioSR Upscaling (Bandwidth Extension)
        # Input: Path, Output: Helpers usually save to file, but we might want to pipe
        # AudioSR 'super_resolution' saves to file.
        
        temp_upscaled = input_path.replace(".wav", "_sr.wav")
        
        current_input = input_path
        
        if HAS_AUDIOSR and enable_upscale and self.audiosr_model:
            log.info("Running AudioSR Upscaling (High Quality)...")
            try:
                # AudioSR wrapper typically handles loading/saving
                # We can use the helper or manual inference
                super_resolution(
                    self.audiosr_model,
                    input_path,
                    save_path=output_path.replace(".wav", ""), # AudioSR appends suffix sometimes or we handle it
                    ddim_steps=200, # Increased from 100 (User request: "200 steps pls")
                    guidance_scale=3.5,
                    seed=42
                )
                
                # Check for output file
                # AudioSR file naming can be complex.
                # Strategy: Look for the newest file in the directory that is not the input or output path
                # and contains the basename of input.
                
                search_dir = os.path.dirname(output_path) or "."
                input_basename = os.path.basename(input_path).replace(".wav", "")
                
                candidates = []
                for fname in os.listdir(search_dir):
                    fpath = os.path.join(search_dir, fname)
                    if input_basename in fname and fpath != input_path and fpath != output_path:
                        # Check modification time (must be recent)
                        mtime = os.path.getmtime(fpath)
                        # Filter likely candidates
                        candidates.append((fpath, mtime))
                
                if candidates:
                    # Sort by time, newest first
                    candidates.sort(key=lambda x: x[1], reverse=True)
                    likely_sr = candidates[0][0]
                    log.info(f"Found likely AudioSR output: {likely_sr}")
                    current_input = likely_sr
                else:
                    log.warning("Could not locate AudioSR output file. Using original input.")
                
            except Exception as e:
                log.error(f"AudioSR failed: {e}. Skipping upscaling.")
        
        # 2. Pedalboard Mastering
        if HAS_PEDALBOARD and self.mastering_chain:
            log.info("Running Pedalboard Mastering Chain...")
            try:
                # Use current_input (which might be the upscaled one if found)
                # For robustness, check if upscaled exists
                input_to_master = current_input
                # If AudioSR succeeded, it created a new file. Let's try to find it.
                # Common AudioSR outputs: output_path + _out.wav
                # (Simple logic: if we find a new file that matches pattern, use it. Else use raw)
                
                with AudioFile(input_to_master) as f:
                    audio = f.read(f.frames)
                    samplerate = f.samplerate
                
                # Process
                effected = self.mastering_chain(audio, samplerate)
                
                # Save (High Quality Float32 to avoid size reduction)
                # Pedalboard defaults to 16-bit. We force 32-bit float.
                import soundfile as sf
                sf.write(output_path, effected.T if len(effected.shape)>1 else effected, samplerate, subtype='FLOAT')
                    
                log.info(f"Mastering complete. Saved to {output_path}")
                return output_path
            except Exception as e:
                log.error(f"Pedalboard failed: {e}")
                # Fallback to copy
                import shutil
                shutil.copy(current_input, output_path)
                return output_path
        else:
            log.warning("Pedalboard not found. Skipping mastering.")
            # Copy input to output
            import shutil
            shutil.copy(current_input, output_path)
            return output_path
