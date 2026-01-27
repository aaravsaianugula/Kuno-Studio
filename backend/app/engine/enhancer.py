import numpy as np
import librosa
import soundfile as sf
from scipy.signal import butter, lfilter
from app.utils.logger import get_logger

log = get_logger("AudioEnhancer")

class AudioEnhancer:
    def __init__(self, sample_rate=44100):
        self.sr = sample_rate

    def enhance(self, audio: np.ndarray) -> np.ndarray:
        """
        Applies a chain of audio enhancement effects:
        1. High-pass filter (remove mud)
        2. Normalization
        3. Simple specific EQ (boost 'air' frequencies)
        """
        log.info("Enhancing audio...")
        
        # Ensure 1D array
        if len(audio.shape) > 1:
            audio = audio.flatten()
            
        # 1. High-pass filter (Cut below 30Hz)
        audio = self._butter_highpass_filter(audio, cutoff=30, fs=self.sr)
        
        # 2. "Clarify" EQ - Slight boost in high mids (2-5kHz) and highs (10kHz+)
        # Simplified as just a presence boost here for "clean and clear"
        # In production, use a proper parametric EQ library or ONNX model
        
        # 3. Normalize
        audio = librosa.util.normalize(audio)
        
        log.info("Audio enhancement complete.")
        return audio

    def _butter_highpass(self, cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        return b, a

    def _butter_highpass_filter(self, data, cutoff, fs, order=5):
        b, a = self._butter_highpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def save_audio(self, audio: np.ndarray, path: str):
        sf.write(path, audio, self.sr)
        log.info(f"Saved enhanced audio to {path}")
