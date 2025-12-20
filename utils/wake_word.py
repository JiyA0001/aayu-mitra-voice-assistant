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
        
        # We need a streaming callback or a blocking loop
        # A simple blocking loop with sd.InputStream is easiest for a linear flow
        
        with sd.InputStream(samplerate=self.SAMPLE_RATE, channels=1, dtype='int16', blocksize=self.CHUNK_SIZE) as stream:
            while True:
                # Read audio chunk
                data, overflowed = stream.read(self.CHUNK_SIZE)
                
                # Convert to numpy array if needed (sounddevice returns numpy by default)
                # openwakeword expects 16-bit PCM (int16) as numpy array or pre-converted float
                # It handles int16 numpy arrays directly now in many examples, but let's confirm format.
                # The model.predict receives input audio.
                
                # Predict
                prediction = self.owwModel.predict(data)
                
                # Check results
                for mdl in self.owwModel.prediction_buffer.keys():
                    # buffer contains history, but we can just check the latest score
                    # prediction is a dict: {'hey jarvis': 0.002, ...}
                    score = prediction[mdl]
                    if score > 0.5:
                        print(f"⚡ Wake Word Detected: {mdl} (Score: {score:.2f})")
                        return mdl
                
                # small sleep to prevent CPU hogging not needed because stream.read blocks
