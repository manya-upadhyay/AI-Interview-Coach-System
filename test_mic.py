import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Say something...")
    r.energy_threshold = 100
    r.pause_threshold = 0.8

    audio = r.listen(source)

print("Processing...")

try:
    print(r.recognize_google(audio, language="en-IN"))
except Exception as e:
    print(e)