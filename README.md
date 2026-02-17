Nova AI Voice Assistant : 
An AI-powered desktop voice assistant built in Python using Google Gemini.

Designed to demonstrate production-level skills in:

AI integration
Secure key management
Multithreading
Audio processing
GUI development

Features :

Voice input + TTS responses
Gemini-powered intelligence
System commands (time, browser, battery)
CustomTkinter UI
Secure environment-variable API handling

Architecture :

Modular design separating:
AI logic
Audio handling
UI layer
Configuration management
Follows clean-code and separation-of-concerns principles.

Security:

API keys managed via environment variables.
No secrets stored in source code.
Industry-standard .env + .gitignore approach.

Installation:
pip install customtkinter speechrecognition pyttsx3 psutil sounddevice numpy python-dotenv google-genai


Create .env:
GEMINI_API_KEY=your_key


Run:
python ui_pro.py
