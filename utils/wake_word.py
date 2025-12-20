import openwakeword
from openwakeword.model import Model
import sounddevice as sd
import numpy as np
import time

class WakeWordDetection:
    def __init__(self, model_names=["hey jarvis"]):
        """
        Initialize the WakeWordDetection model.
        Args:
            model_names (list): List of model names to load (e.g., ["hey jarvis", "alexa"]).
        """
        print(f"🔄 Loading Wake Word models: {model_names}...")
        # Automatically download models if missing
        openwakeword.utils.download_models()
        self.owwModel = Model(wakeword_models=model_names)
        print("✅ Wake Word models loaded!")
        
        self.SAMPLE_RATE = 16000
        self.CHUNK_SIZE = 1280 # 80ms chunks

    def listen(self):
        """
        Listens continuously until the wake word is detected.
        Returns:
            str: The detected wake word.
        """
        print("👂 Listening for wake word (Say 'Hey Jarvis')...")
        
        # Capture at 48000Hz (Native for many Pi USB mics)
        # We need chunks of 1280 samples at 16k => 80ms
        # At 48k, 80ms is 1280 * 3 = 3840 samples
        NATIVE_RATE = 48000
        CHUNK_16K = 1280
        CHUNK_48K = 3840 
        
        # Verify downsample factor is integer
        assert NATIVE_RATE / self.SAMPLE_RATE == 3.0
        
        with sd.InputStream(samplerate=NATIVE_RATE, channels=1, dtype='int16', blocksize=CHUNK_48K) as stream:
            while True:
                # Read audio chunk (3840 samples)
                data_48k, overflowed = stream.read(CHUNK_48K)
                
                # Downsample to 16k (Take every 3rd sample)
                # Simple decimation works reasonably well for speech if not too much HF noise
                data_16k = data_48k[::3]
                
                # Predict
                prediction = self.owwModel.predict(data_16k)
                
                # Check results
                for mdl in self.owwModel.prediction_buffer.keys():
                    score = prediction[mdl]
                    if score > 0.5:
                        print(f"⚡ Wake Word Detected: {mdl} (Score: {score:.2f})")
                        return mdl
