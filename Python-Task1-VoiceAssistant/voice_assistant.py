import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

class VoiceAssistant: 
    def __init__(self):
      
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175) 
        self.engine.setProperty("volume", 1.0)
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.8

        self.running = True

    def speak(self, text: str):
     
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self) -> str:
        
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

  

    def process_command(self, command: str):
        if not command:
            return 

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
