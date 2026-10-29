import datetime              # Provides current date and time
import json                  # Parses JSON data returned from Wikipedia
import re                    # Cleans whole filler words using regex word boundaries
import urllib.error          # Handles network/HTTP exceptions
import urllib.parse          # Formats URLs safely for searches
import urllib.request        # Makes HTTP requests to Wikipedia API without extra installs
import numpy as np           # Handles raw audio byte arrays
import pyttsx3               # Text-to-speech library to make Python speak
import sounddevice as sd     # Captures audio from your microphone (bypasses PyAudio)
import speech_recognition as sr  # Converts recorded voice into text
import webbrowser
import os
import pywhatkit
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="models/gemini-3.8-flash",
    system_instruction="you are Badriprasad, a witty and efficient personal desktop assistant. Keep your  spoken responses short, precise (1-2 sentences max), natural, and direct.Avoid markdown asterisks, emojis, or bullet points. "
)
def ask_ai(prompt):
    try:
        response = model.generate_content(prompt)
        # Bold markers aur unnecessary symbols clean up karna
        clean_reply = response.text.replace("*", "").replace("#", "").strip()
        return clean_reply
    except Exception as e:
        print(f"AI Error: {e}")
        return "Sir, I had trouble connecting to my neural core."

def speak(audio):
    """
    Initializes a fresh SAPI5 COM instance per call to guar nm s/2wwwwwwww        antee audio plays
    without freezing or dropping out in continuous loops.
    """
    try:
        temp_engine = pyttsx3.init('sapi5')
        voices = temp_engine.getProperty('voices')
        temp_engine.setProperty('voice', voices[1].id)
        temp_engine.setProperty('rate', 175)

        temp_engine.say(audio)
        temp_engine.runAndWait()
        temp_engine.stop()
        del temp_engine
    except Exception as e:
        print(f"Text-to-speech error: {e}")


def wishMe():
    """
    Greets dynamically based on the system clock and introduces BadriPrasad.
    """
    hour = int(datetime.datetime.now().hour)

    if 0 <= hour < 12:
        greetings = "Good Morning sir."
    elif 12 <= hour < 18:
        greetings = "Good Afternoon sir."
    else:
        greetings = "Good evening sir."

    full_wish = f"{greetings} I am Badriprasad sir. Please tell me how may I help you"
    speak(full_wish)


def take_command(duration=5, samplerate=16000):
    """
    Records 5 seconds of audio using sounddevice and converts it to text via Google STT.
    """
    r = sr.Recognizer()
    print("Listening...")

    try:
        # Record mono 16-bit audio without requiring PyAudio
        audio_np = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype='int16'
        )
        sd.wait()  # Wait for recording to complete

        # Convert NumPy array into raw bytes that SpeechRecognition understands
        audio = sr.AudioData(audio_np.tobytes(), samplerate, 2)

        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        return query

    except Exception:
        print("Say that again please...")
        return "None"


def get_wikipedia_summary(search_topic):
    """
    Directly queries Wikipedia's REST API using standard urllib.
    Avoids deprecated or blocked external packages.
    """
    clean_title = urllib.parse.quote(search_topic.strip().replace(" ", "_"))
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{clean_title}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=6) as response:
            data = json.loads(response.read().decode("utf-8"))
            extract = data.get("extract", "")

            if extract:
                # Split paragraph into individual sentences and return the first two
                sentences = extract.split(". ")
                return ". ".join(sentences[:2]) + "."
            return "No summary found for this topic on Wikipedia."

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return f"Sorry sir, I could not find a Wikipedia page for '{search_topic}'."
        return "Wikipedia service is currently unreachable."
    except Exception as e:
        print(f"Wikipedia Fetch Error: {e}")
        return "An error occurred while connecting to Wikipedia."


# Execution entry point
if __name__ == "__main__":
    wishMe()

    while True:
        query = take_command().lower()

        # Skip loop if audio failed or returned nothing
        if query == "none" or not query.strip():
            continue

        # Voice command to safely exit
        if "exit" in query or "quit" in query or "bye" in query:
            speak("Goodbye sir, shutting down.")
            break

        # Task: Wikipedia Search
        if "wikipedia" in query:
            speak("Searching Wikipedia...")

            # Clean up trigger words and filler phrases safely using word boundaries (\b)
            search_query = query
            fillers = [
                r"\bwikipedia\b",
                r"\baccording to\b",
                r"\btell me about\b",
                r"\bwho is\b",
                r"\bwhat is\b",
                r"\bsearch for\b",
                r"\bsearch\b",
                r"\bon\b",
                r"\bfor\b",
            ]
            for pattern in fillers:
                search_query = re.sub(pattern, "", search_query, flags=re.IGNORECASE)

            # Clean up extra whitespace left behind
            search_query = " ".join(search_query.split()).strip()

            if not search_query:
                speak("What would you like me to look up on Wikipedia?")
                continue

            results = get_wikipedia_summary(search_query)
            print(results)

            # Clean citations and non-standard dashes that cause SAPI5 to choke
            clean_text = re.sub(r"\[.*?\]", "", results)
            clean_text = clean_text.replace("–", "-").replace("—", "-")

            speak(f"According to Wikipedia. {clean_text}")
            
            
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            
        elif 'open google' in query:
            webbrowser.open("google.com")
            
        elif 'open brave browser' in query:
            webbrowser.open("bravebrowser.com")
            
        elif 'open satckoverflow' in query:
            webbrowser.open("stackoverflow.com")
        # task: play songs on youtube
        elif 'play' in query:
            song = query.replace("play","").strip()
            if song:
                speak(f"Playing{song} on youtube")
                print(f"playing:{song}")
                pywhatkit.playonyt(song)
            else:
                speak("Which song would you like to play,sir?")
        
        elif 'the time inquery' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"sir the time is {strTime}")
        else:
            print("Thinking...")
            reply = ask_ai(query)
            print(f"Badriprasad: {reply}")
            speak(reply)
            
            