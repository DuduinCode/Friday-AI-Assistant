import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os
import google.generativeai as genai

# Initialize speech recognizer, text-to-speech engine, and Pygame
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Configure the Google Gemini API
genai.configure(api_key="YOUR_GEMINI_API_KEY")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Function to use Google Gemini API for processing commands
def aiProcess(command):
    chat_session = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    ).start_chat(history=[])
    
    response = chat_session.send_message(command)
    return response.text

# Text-to-speech function using Google Text-to-Speech
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

# Command processing function
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open cloud" in c.lower():
        webbrowser.open("https://aws.amazon.com/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey=YOUR_NEWSAPI_KEY")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])
    else:
        output = aiProcess(c)
        speak(output)

# Main function to listen for commands and activate the assistant
if __name__ == "__main__":
    speak("I am listening, sir...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)
                word = recognizer.recognize_google(audio)
                if word.lower() == "friday":
                    speak("Yes sir")
                    with sr.Microphone() as source:
                        print("Friday Active...")
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
                        processCommand(command)
        except Exception as e:
            print(f"Error: {e}")
