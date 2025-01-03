import sounddevice as sd
import numpy as np
import soundfile as sf


def record_audio(duration=10, sample_rate=44100):
    """
    Records audio for the given duration and returns the audio data.
    """
    print("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    print("Recording complete!")
    return audio_data


def extract_screaming(audio_data, sample_rate, threshold=0.8):
    """
    Extracts screaming segments based on amplitude threshold.
    """
    print("Analyzing audio for screaming...")
    screaming_indices = np.where(np.abs(audio_data) > threshold)[0]
    
    if len(screaming_indices) == 0:
        print("No screaming detected.")
        return None

    start_index = max(0, screaming_indices[0] - int(0.5 * sample_rate))  # Add padding before screaming
    end_index = min(len(audio_data), screaming_indices[-1] + int(0.5 * sample_rate))  # Add padding after screaming
    screaming_audio = audio_data[start_index:end_index]
    print(f"Screaming detected! Extracted {len(screaming_audio) / sample_rate:.2f} seconds of audio.")
    return screaming_audio


def save_audio(file_path, audio_data, sample_rate):
    """
    Saves the audio data to a file.
    """
    sf.write(file_path, audio_data, sample_rate)
    print(f"Screaming audio saved to {file_path}")


# Main program
sample_rate = 44100
audio_data = record_audio(duration=10, sample_rate=sample_rate)  # Record for 10 seconds
screaming_audio = extract_screaming(audio_data, sample_rate, threshold=0.8)

if screaming_audio is not None:
    save_audio("screaming_output.wav", screaming_audio, sample_rate)
else:
    print("No screaming audio to save.")
