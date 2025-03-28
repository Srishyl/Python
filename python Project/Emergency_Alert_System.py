import sounddevice as sd
import numpy as np
import soundfile as sf
import speech_recognition as sr
import smtplib
from email.message import EmailMessage
import cv2
import geocoder
from twilio.rest import Client
import threading

# Twilio configuration
TWILIO_ACCOUNT_SID = "AC719b90af048a4b88ff19aeacdbff1904"
TWILIO_AUTH_TOKEN = "e14c39635d6591d05d3297b5266cb2d4"
TWILIO_PHONE_NUMBER = "+12188750812"  # Twilio phone number
CONTACT_PHONE_NUMBERS = ["+91 8660346308", "+91 7204037413"]  # Replace with recipient phone numbers

# Email configuration
EMAIL_ADDRESS = "srishylmayurisakshi@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "zkgr rjul hexd eotx"  # Generate an app password from Google settings

# Function to record audio
def record_audio(duration=10, sample_rate=44100):
    print("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    print("Recording complete!")
    return audio_data

# Function to extract screaming segments
def extract_screaming(audio_data, sample_rate, threshold=0.8):
    print("Analyzing audio for screaming...")
    screaming_indices = np.where(np.abs(audio_data) > threshold)[0]

    if len(screaming_indices) == 0:
        print("No screaming detected.")
        return None

    start_index = max(0, screaming_indices[0] - int(0.5 * sample_rate))
    end_index = min(len(audio_data), screaming_indices[-1] + int(0.5 * sample_rate))
    screaming_audio = audio_data[start_index:end_index]
    print(f"Screaming detected! Extracted {len(screaming_audio) / sample_rate:.2f} seconds of audio.")
    return screaming_audio

# Function to save audio
def save_audio(file_path, audio_data, sample_rate):
    sf.write(file_path, audio_data, sample_rate)
    print(f"Screaming audio saved to {file_path}")

# Function to capture video
def capture_video(duration, output_path):
    print("Capturing video...")
    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (640, 480))

    start_time = cv2.getTickCount()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        if (cv2.getTickCount() - start_time) / cv2.getTickFrequency() > duration:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Video saved to {output_path}")

# Function to get current location and generate a live location link
def get_location():
    print("Fetching current location...")
    try:
        g = geocoder.ip('me')
        if g.latlng:
            latitude, longitude = g.latlng
            google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
            return google_maps_link
        else:
            return "Location not available"
    except Exception as e:
        print(f"Error fetching location: {e}")
        return "Error fetching location"

# Function to send an alert email with live location link
def send_email_alert(keyword, location_link, video_path, contacts):
    print("Sending email alert...")
    subject = f"ALERT: {keyword.capitalize()} detected!"
    body = f"Risk detected! Check the victim's live location: {location_link}\nVideo of the victim is attached."

    msg = EmailMessage()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ", ".join(contacts)
    msg['Subject'] = subject
    msg.set_content(body)

    with open(video_path, "rb") as video_file:
        video_data = video_file.read()
        msg.add_attachment(video_data, maintype="video", subtype="mp4", filename="victim_video.mp4")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email alert sent!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to make calls using Twilio
def make_calls(keyword, location_link):
    print("Making emergency calls...")
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for contact in CONTACT_PHONE_NUMBERS:
        try:
            message = f"Emergency Alert: {keyword.capitalize()} detected! Check live location: {location_link}"
            call = client.calls.create(
                twiml=f'<Response><Say>{message}</Say></Response>',
                to=contact,
                from_=TWILIO_PHONE_NUMBER
            )
            print(f"Call initiated to {contact}.")
        except Exception as e:
            print(f"Error making call to {contact}: {e}")

# Function to analyze speech
def analyze_speech(file_path, contacts):
    print("Analyzing speech for keywords...")
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data).lower()
            print(f"Detected speech: {text}")

            keywords = ["risk", "risky", "high risk"]
            for keyword in keywords:
                if keyword in text:
                    print(f"Alert: Keyword '{keyword}' detected in the speech!")
                    location_link = get_location()
                    video_path = "victim_video.mp4"

                    # Start video capture in a separate thread
                    video_thread = threading.Thread(target=capture_video, args=(10, video_path))
                    video_thread.start()
                    video_thread.join()

                    send_email_alert(keyword, location_link, video_path, contacts)
                    make_calls(keyword, location_link)
                    return
            print("No keywords detected in the speech.")
    except Exception as e:
        print(f"Error during speech recognition: {e}")

# Main program
def main():
    contacts = ["srishylkumar29@gmail.com", "mayurishetty444@gmail.com"]
    sample_rate = 44100
    audio_data = record_audio(duration=10, sample_rate=sample_rate)
    screaming_audio = extract_screaming(audio_data, sample_rate, threshold=0.8)

    if screaming_audio is not None:
        file_path = "screaming_output.wav"
        save_audio(file_path, screaming_audio, sample_rate)
        analyze_speech(file_path, contacts)
    else:
        print("No screaming audio to save or analyze.")

if __name__ == "__main__":
    main()V
