import streamlit as st
import requests

st.set_page_config(
    page_title="Local LLM Text Generator",
    page_icon="🤖"
)

st.title("🤖 Local LLM Text Generator")

st.write(
    "Generate text using a locally running Large Language Model with Ollama."
)

prompt = st.text_area(
    "Enter your prompt:",
    placeholder="Write a short paragraph about Artificial Intelligence."
)

if st.button("Generate Text"):

    if prompt.strip() == "":
        st.warning("Please enter a prompt.")

    else:
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.2:latest",
                    "prompt": prompt,
                    "stream": False
                }
            )

            if response.status_code == 200:
                result = response.json()

                st.subheader("Generated Text")
                st.write(result["response"])

            else:
                st.error(
                    f"Ollama error: {response.status_code}"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to Ollama. Make sure Ollama is running."
            )