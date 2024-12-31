import torch
import torchaudio
from scipy.io import wavfile
import sounddevice as sd
import numpy as np

# Load pre-trained model for sound classification
class ScreamDetector:
    def _init_(self, model_path):
        self.model = torch.load(model_path)
        self.model.eval()

    def process_audio(self, audio_data, sample_rate):
        # Convert audio data to tensor
        waveform = torch.tensor(audio_data).unsqueeze(0)
        transform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
        waveform = transform(waveform)
        return waveform

    def detect_scream(self, audio_data, sample_rate):
        waveform = self.process_audio(audio_data, sample_rate)
        with torch.no_grad():
            prediction = self.model(waveform)
        return prediction.argmax(dim=1).item()  # Return class index (e.g., 1 for scream)


# Real-time audio capture and scream detection
def audio_callback(indata, frames, time, status):
    detector = ScreamDetector(model_path='scream_model.pth')
    if status:
        print(status)
    audio_data = indata[:, 0]  # Use first channel of audio
    sample_rate = 44100
    scream_detected = detector.detect_scream(audio_data, sample_rate)
    if scream_detected:  # If scream detected, activate system
        print("Scream detected! Activating system...")
        activate_system()


def activate_system():
    # Implement logic for risk assessment and communication
    print("System activated. Assessing risk and communicating...")


# Start audio stream
stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=44100)
print("Listening for screams...")
with stream:
    sd.sleep(10000)  # Listen for 10 seconds (adjust as needed)