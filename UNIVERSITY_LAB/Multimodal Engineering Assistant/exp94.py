import whisper
import ollama
import pyttsx3

# Speech to Text
print("Loading Whisper...")
speech_model = whisper.load_model("base")

audio = input(
    "Enter audio file path: "
)

result = speech_model.transcribe(audio)

question = result["text"]

print("\nRecognized Question:")
print(question)

# Text Generation
prompt = f"""
Answer this engineering question clearly:

{question}
"""

response = ollama.generate(
    model="llama3.2",
    prompt=prompt
)

answer = response["response"]

print("\nAI Explanation:")
print(answer)

# Text to Speech
engine = pyttsx3.init()

engine.save_to_file(
    answer,
    "engineering_explanation.wav"
)

engine.runAndWait()

print(
    "\nAudio explanation saved as "
    "engineering_explanation.wav"
)