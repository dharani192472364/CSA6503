import streamlit as st
from transformers import pipeline

st.title("Engineering Support Chatbot")

@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-small")

model = load_model()

question = st.text_input("Enter a technical question:")

if st.button("Get Solution"):
    if question:
        prompt = "Provide a simple technical solution for: " + question
        answer = model(prompt, max_length=150)
        st.write("### Solution")
        st.write(answer[0]["generated_text"])