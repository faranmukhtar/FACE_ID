Face ID — Biometric Access Control System

A Python desktop app that lets you register and log in using your face.
Run Gui.py to launch. Click Register New Face to add yourself — the camera will capture your face from three angles. Click Login with Face to authenticate — if your face is recognised, access is granted.


Setup

pip install -r requirements.txt

python Gui.py


Resetting Data

To wipe all registered faces and start fresh, delete Encodings.pkl, Names.pkl, and the SAVED_PEOPLE/ folder.
