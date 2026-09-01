import pyttsx3

engine = pyttsx3.init()

text = input(
    "Enter engineering study material: "
)

engine.save_to_file(
    text,
    "engineering_audio.wav"
)

engine.runAndWait()

print("\nAudio saved as engineering_audio.wav")