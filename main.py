# -------- main file to run Jarvis
import os
import subprocess
import eel
import pygame

# Carry all commands
from engine.command import *
# Contains all features of assistant
from engine.features import *
# Use for face authentication
from authenticate.recoganize import AuthenticateFace
# Default configuration file
from engine.config import *

# Initialize www directory for GUI
eel.init('www')


# ----------------- Sound Helper -----------------
def play_sound(file_path):
    """Play a sound using pygame (works reliably on Windows)."""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()  # plays asynchronously
    except Exception as e:
        print(f"Failed to play sound: {e}")


# ----------------- Main Start Function -----------------
def start():
    # Absolute path to start sound
    music_dir = os.path.join(os.getcwd(), "www", "assets", "audio", "start_sound.mp3")
    play_sound(music_dir)

    # Exposed function for GUI to play start sound again
    @eel.expose
    def StartSound():
        play_sound(music_dir)

    # Exposed function to start Jarvis via GUI
    @eel.expose
    def Start():
        subprocess.call([r'static\\device.bat'])
        eel.AssistantName(ASSISTANT_NAME)

        from engine.features import auth_protocol

        auth_protocol()
        flag = AuthenticateFace()
        # flag = 1  # uncomment to skip face authentication for testing
        print(flag)

        if flag == 1:
            eel.hideFaceAuth()
            speak("Face authentication successful")
            eel.hideFaceAuthSuccess()

            from engine.features import wish
            wish()
            eel.hideStart()
            eel.init()
        else:
            speak("Authentication failed")

    # Open GUI in MS Edge as app window
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    # Run Eel index file in browser
    eel.start("index.html", mode=None, host='localhost', block=True)
