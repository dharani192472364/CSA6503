import pyttsx3

engine = pyttsx3.init()

text = input("Enter text: ")

engine.save_to_file(text, "output.wav")
engine.runAndWait()

print("Text converted to speech successfully.")
print("Audio saved as output.wav")