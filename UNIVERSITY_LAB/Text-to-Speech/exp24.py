import pyttsx3

engine = pyttsx3.init()

text = input(
    "Enter engineering text: "
)

engine.say(text)

engine.runAndWait()

print("\nSpeech generated successfully.")