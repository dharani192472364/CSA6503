import streamlit as st
import ollama

st.title("Engineering Text Generator")

prompt = st.text_area(
    "Enter your prompt:"
)

if st.button("Generate"):

    if prompt:

        response = ollama.generate(
            model="llama3.2",
            prompt=prompt
        )

        st.subheader("Generated Text")

        st.write(
            response["response"]
        )

    else:
        st.warning("Please enter a prompt.")