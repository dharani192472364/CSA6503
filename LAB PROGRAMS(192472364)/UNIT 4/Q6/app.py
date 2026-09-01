import streamlit as st
from gtts import gTTS

st.title("Engineering Text-to-Speech")

text = st.text_area(
    "Enter engineering text:",
    "Artificial intelligence is widely used in modern engineering applications."
)

if st.button("Convert to Speech"):

    if text:
        tts = gTTS(text=text, lang="en")
        tts.save("engineering_speech.mp3")

        st.audio(
            "engineering_speech.mp3",
            format="audio/mp3"
        )

        st.success("Speech generated successfully!")