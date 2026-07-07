"""
Voice Assistant - Beginner Tier
--------------------------------
Features:
- Capture voice input via microphone (speech_recognition)
- Respond to "hello" with a greeting
- Tell current time and date
- Perform a web search on a spoken topic
- Graceful error handling (ask user to repeat if unclear)
- Text-to-speech feedback for every response (pyttsx3)

Install dependencies:
    pip install SpeechRecognition pyttsx3 pyaudio

Note: pyaudio can be tricky on Windows. If `pip install pyaudio` fails, use:
    pip install pipwin
    pipwin install pyaudio
"""

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser


class VoiceAssistant:

    
    def __init__(self):
        # Set up text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)   # speaking speed
        self.engine.setProperty("volume", 1.0)

        # Set up speech recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.8

        self.running = True

    # ---------- Core I/O ----------

    def speak(self, text: str):
        """Convert text to speech and print it for visibility."""
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self) -> str:
        """
        Capture audio from the microphone and convert it to text.
        Returns an empty string if speech was not understood.
        """
        with sr.Microphone() as source:
            print("\nListening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=8)
            except sr.WaitTimeoutError:
                self.speak("I didn't hear anything. Could you please repeat that?")
                return ""

        try:
            command = self.recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower().strip()
        except sr.UnknownValueError:
            # Speech was unintelligible
            self.speak("Sorry, I didn't catch that. Could you please repeat?")
            return ""
        except sr.RequestError:
            self.speak("I'm having trouble reaching the speech service right now.")
            return ""

    # ---------- Command handlers ----------

    def handle_greeting(self):
        self.speak("Hello! It's great to hear from you. How can I help you today?")

    def handle_time_date(self, command: str):
        now = datetime.datetime.now()
        if "date" in command and "time" not in command:
            response = f"Today's date is {now.strftime('%A, %B %d, %Y')}."
        elif "time" in command and "date" not in command:
            response = f"The current time is {now.strftime('%I:%M %p')}."
        else:
            response = (
                f"It's currently {now.strftime('%I:%M %p')} "
                f"on {now.strftime('%A, %B %d, %Y')}."
            )
        self.speak(response)

    def handle_web_search(self, command: str):
        # Strip trigger phrases to isolate the search topic
        trigger_phrases = ["search for", "search", "look up", "google"]
        topic = command
        for phrase in trigger_phrases:
            if phrase in topic:
                topic = topic.split(phrase, 1)[1].strip()
                break

        if not topic:
            self.speak("What would you like me to search for?")
            topic = self.listen()
            if not topic:
                return

        self.speak(f"Searching the web for {topic}.")
        url = f"https://www.google.com/search?q={topic.replace(' ', '+')}"
        webbrowser.open(url)

    def handle_exit(self):
        self.speak("Goodbye! Have a wonderful day.")
        self.running = False

    # ---------- Command router ----------

    def process_command(self, command: str):
        if not command:
            return  # already handled by listen()'s error messaging

        if "hello" in command or "hi assistant" in command:
            self.handle_greeting()

        elif "time" in command or "date" in command:
            self.handle_time_date(command)

        elif "search" in command or "look up" in command or "google" in command:
            self.handle_web_search(command)

        elif any(word in command for word in ["exit", "quit", "stop", "goodbye", "bye"]):
            self.handle_exit()

        else:
            self.speak(
                "I can greet you, tell the time or date, or search the web. "
                "Please try one of those commands."
            )

    # ---------- Main loop ----------

    def run(self):
        self.speak("Voice assistant is online. Say 'hello' to get started, or 'exit' to quit.")
        while self.running:
            command = self.listen()
            self.process_command(command)


if __name__ == "__main__":
    assistant = VoiceAssistant()
    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\nShutting down assistant.")