import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Please say something...")
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Sorry, I could not understand your speech.")
except sr.RequestError:
    print("Could not request results from Google Speech Recognition service.")
import pyttsx3

engine = pyttsx3.init()
engine.say("Hello! Your voice advisory system is ready.")
engine.runAndWait()
import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()
engine = pyttsx3.init()

with sr.Microphone() as source:
    engine.say("Hello! Ask me about weather or crops.")
    engine.runAndWait()

    print("Listening...")
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)
    print("You said:", text)

    # Simple logic to reply
    if "weather" in text.lower():
        reply = "The weather in Hyderabad is 30 degrees Celsius."
    elif "crop" in text.lower():
        reply = "The crop seems healthy. Keep regular irrigation."
    else:
        reply = "Sorry, I can only give weather or crop advice for now."

    engine.say(reply)
    engine.runAndWait()

except sr.UnknownValueError:
    engine.say("Sorry, I could not understand your speech.")
    engine.runAndWait()
except sr.RequestError:
    engine.say("Could not request results from Google Speech Recognition service.")
    engine.runAndWait()
