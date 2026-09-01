import whisper

model = whisper.load_model("base")

print("Speech-to-Text Engineering Assistant")

audio_file = input(
    "\nEnter microphone/audio file path: "
)

result = model.transcribe(
    audio_file
)

print("\nWritten Query:")
print(result["text"])