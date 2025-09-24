import os
import time
import pywhatkit
import eel
import pyttsx3
import speech_recognition as sr
import pygame

from engine.config import *

# ------------------- Text-to-Speech Setup -------------------
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 174)
print(voices[0].id)
print(voices)


def speak(audio):
    """Speak the audio and update the GUI via Eel."""
    engine.say(audio)
    eel.SpeakMessage(audio)
    eel.receiverText(audio)
    engine.runAndWait()


# ------------------- Speech Recognition -------------------
def takecommand():
    """Listen from microphone and return recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.SpeakMessage("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=10, phrase_time_limit=6)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said: {query}")
        eel.SpeakMessage(query)
        time.sleep(2)
    except Exception:
        return "none"
    return query.lower()


# ------------------- Sound Helper -------------------
def play_sound(file_path):
    """Play a sound using pygame (works reliably on Windows)."""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()  # plays asynchronously
    except Exception as e:
        print(f"Failed to play sound: {e}")


# ------------------- Main Command Handler -------------------
@eel.expose
def allCommands(typequery=1):
    """Handle all voice or chat commands."""
    music_dir = os.path.join(os.getcwd(), "www", "assets", "audio", "start_sound.mp3")
    play_sound(music_dir)

    # Input from chatbox or voice
    if typequery == 1:
        query = takecommand()
        eel.senderText(query)
    else:
        eel.SpeakMessage(typequery)
        time.sleep(2)
        query = typequery
        eel.senderText(query)

    # ------------------- Command Routing -------------------
    if "open" in query:
        from engine.features import openCommand
        openCommand(query)
    elif "close" in query:
        from engine.features import close
        close(query)
    elif "on youtube" in query:
        from engine.features import PlayYoutube
        PlayYoutube(query)
    elif "weather" in query:
        from engine.features import weather
        weather(query)
    elif "call disconnect" in query or "disconnect call" in query or "stop call" in query:
        from engine.features import DisconnectCall
        DisconnectCall()
    elif query == "call":
        speak("Who do you want to call?")
        query = takecommand()
        from engine.features import MakeCall
        MakeCall(query)
    elif "call" in query or "phone" in query:
        from engine.features import MakeCall
        MakeCall(query)
    elif "happy" in query:
        speak("Thank You Sir")
    elif "battery status" in query or "power status" in query:
        from engine.features import battery
        battery()
    elif "shutdown" in query or "power off" in query:
        speak("Shutdown process started")
        speak("Have a good day " + OWNER_NAME)
        os.system('shutdown -s')
    elif "send message" in query:
        from engine.features import sendMessage, whatsAppSend
        contact_no = sendMessage(query)
        if contact_no != 0:
            speak("What message to send?")
            query = takecommand()
            whatsAppSend("+91" + contact_no, query)
    elif "play song" in query or "play music" in query or "play" in query:
        from engine.features import spotifyPlayer
        spotifyPlayer(query)
    else:
        if query != "none":
            from engine.bot import bot
            returnString = bot(query)
            if returnString != 0:
                speak(returnString)
            else:
                from engine.features import chatGPT
                print("chatGPT run")
                chatGPT(query)

    eel.hideSpectrum()
