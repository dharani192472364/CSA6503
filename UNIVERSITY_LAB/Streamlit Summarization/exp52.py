import streamlit as st
import ollama

st.set_page_config(
    page_title="Local AI Assistant"
)

st.title("🤖 Local Engineering AI")

prompt = st.text_area(
    "Enter your question or prompt"
)

if st.button("Generate Response"):

    if prompt.strip():

        result = ollama.generate(
            model="llama3.2",
            prompt=prompt
        )

        st.success(
            result["response"]
        )

    else:

        st.error(
            "Please enter a prompt."
        )