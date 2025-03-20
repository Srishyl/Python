**Emergency Alert System**

Overview:

This project is an Emergency Alert System that detects distress situations by analyzing screaming sounds and keywords in speech. Upon detection, it triggers multiple emergency responses:

1.Records and analyzes audio for screaming or distress keywords.

2.Captures a short video.

3.Fetches the user's live location.

4.Sends an alert email with location and video.

5.Initiates emergency calls to predefined contacts.

Features:

- Audio Recording: Captures real-time audio for analysis.

- Screaming Detection: Identifies screaming based on amplitude threshold.

- Speech Recognition: Detects distress keywords like risk, risky, high risk.

- Video Recording: Captures a short video when an emergency is detected.

- Live Location Sharing: Retrieves the user's current location and generates a Google Maps link.

- Email Alerts: Sends an alert email with the captured video and location details.

- Emergency Calls: Uses Twilio to make automated calls with an emergency message.

Prerequisites

Ensure you have the following dependencies installed:

Configuration

Twilio Setup

- Create an account on Twilio.

- Get your Account SID, Auth Token, and Twilio Phone Number.

- Replace the placeholders in the script:

Email Setup

- Use a Gmail account and enable App Passwords.

- Replace the email credentials in the script:

Contact List

- Modify the list of email recipients:

Usage

Run the main script:

How It Works

1.Records 10 seconds of audio.

2.Analyzes the audio for screaming and distress keywords.

3.If detected:

  Captures a 10-second video.

  Fetches live location.

  Sends an alert email with video and location link.

  Initiates emergency calls to predefined contacts.

4.If no distress is detected, the script terminates.

Notes

- Ensure your microphone and camera permissions are enabled.

- Adjust the screaming detection threshold if necessary.

- The project relies on Google's Speech Recognition API, which requires an internet connection.

Author

Developed by Srishyla Kumar TP

