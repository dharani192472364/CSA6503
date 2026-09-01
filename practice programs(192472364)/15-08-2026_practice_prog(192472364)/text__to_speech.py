import speech_recognition as sr

recognizer = sr.Recognizer()

print("=" * 60)
print("SPEECH TO TEXT")
print("=" * 60)

with sr.Microphone() as source:
    print("Adjusting for background noise...")
    recognizer.adjust_for_ambient_noise(source, duration=1)

    print("Speak now...")
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)

    print("\nRecognized Text:")
    print(text)

except sr.UnknownValueError:
    print("Could not understand the speech.")

except sr.RequestError as e:
    print("Could not connect to speech recognition service:", e)