import whisper

model = whisper.load_model("base")

audio = input(
    "Enter audio file path: "
)

result = model.transcribe(audio)

print("\nRecognized Speech:")
print(result["text"])