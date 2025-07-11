import speech_recognition as sr
import pyttsx3
import openai
import datetime
import webbrowser
import os

# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Set OpenAI API key (replace with your own)
openai.api_key = 'your-openai-api-key'

def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good Morning, Sir.")
    elif hour < 18:
        speak("Good Afternoon, Sir.")
    else:
        speak("Good Evening, Sir.")
    speak("I am JARVIS. How can I help you today?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"You said: {query}\n")
    except Exception:
        speak("Sorry, I did not catch that.")
        return "None"
    return query.lower()

def ask_openai(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if available
            messages=[{"role": "user", "content": question}]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return "I'm having trouble connecting to OpenAI."

def execute_task(query):
    if "open youtube" in query:
        speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")
    elif "open google" in query:
        speak("Opening Google.")
        webbrowser.open("https://google.com")
    elif "time" in query:
        time_str = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time_str}")
    elif "shutdown" in query or "exit" in query:
        speak("Shutting down. Goodbye.")
        exit()
    else:
        speak("Let me think...")
        answer = ask_openai(query)
        speak(answer)

if __name__ == "__main__":
    wish_me()
    while True:
        command = take_command()
        if command != "None":
            execute_task(command)
