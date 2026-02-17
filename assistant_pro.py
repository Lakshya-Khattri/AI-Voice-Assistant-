
import threading
import speech_recognition as sr
import webbrowser
import datetime
import os
import pyttsx3
import psutil
import sounddevice as sd
import numpy as np
from dotenv import load_dotenv
from google import genai

# ---------- CONFIG ----------
WAKE_WORD = "nova"
GEMINI_MODEL = "gemini-2.5-flash"

# ---------- GEMINI ----------
load_dotenv()
API_KEY = os.getenv("AIzaSyBQ_sKeyb81h8ZPi7Or9godmbajTG9glwY")

gemini_client = None
if API_KEY:
    try:
        gemini_client = genai.Client(api_key=API_KEY)
    except Exception as e:
        print("Gemini error:", e)

# ---------- TTS ----------
engine = pyttsx3.init()
engine.setProperty("rate", 175)

def speak(text):
    engine.stop()
    engine.say(text)
    engine.runAndWait()

# ---------- AUDIO ----------
def record(duration=4, fs=16000):
    try:
        audio = sd.rec(int(duration*fs), samplerate=fs, channels=1, dtype="int16")
        sd.wait()
        return np.squeeze(audio)
    except:
        return None

def listen_once():
    r = sr.Recognizer()
    audio = record()
    if audio is None:
        return None
    data = sr.AudioData(audio.tobytes(),16000,2)
    try:
        return r.recognize_google(data,language="en-US")
    except:
        return None

# ---------- AI ----------
def ask_ai(q):
    if not gemini_client:
        return "AI not configured."
    try:
        res = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=q
        )
        return res.text if res and res.text else "No response."
    except Exception as e:
        return "AI error."

# ---------- COMMANDS ----------
def handle(cmd):
    cmd = cmd.lower()

    if "open google" in cmd:
        webbrowser.open("https://google.com")
        return "Opening Google"

    if "open youtube" in cmd:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"

    if "search for" in cmd:
        q = cmd.split("search for",1)[-1].strip()
        if q:
            webbrowser.open(f"https://google.com/search?q={q}")
            return f"Searching {q}"

    if "time" in cmd:
        return datetime.datetime.now().strftime("%I:%M %p")

    if "battery" in cmd:
        b = psutil.sensors_battery()
        return f"{b.percent}% battery" if b else "No battery data"

    return ask_ai(cmd)

# ---------- WAKE MODE ----------
def listen_for_wake(callback):
    while True:
        text = listen_once()
        if text and WAKE_WORD in text.lower():
            callback("Wake word detected")
            speak("Yes?")
            cmd = listen_once()
            if cmd:
                callback("You: "+cmd)
                res = handle(cmd)
                callback("Assistant: "+res)
                speak(res)
