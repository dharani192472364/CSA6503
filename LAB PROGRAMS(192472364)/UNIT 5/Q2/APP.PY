import streamlit as st
import requests

st.set_page_config(
    page_title="Local LLM Text Summarizer",
    page_icon="📝"
)

st.title("📝 Local LLM Text Summarizer")

st.write(
    "Summarize text using a locally running Large Language Model through Ollama."
)

text = st.text_area(
    "Enter the text to summarize:",
    height=250,
    placeholder="Paste a paragraph or article here..."
)

if st.button("Summarize"):

    if text.strip() == "":
        st.warning("Please enter some text.")

    else:
        prompt = f"""
Summarize the following text clearly and concisely.
Include only the important points.

Text:
{text}
"""

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

                st.subheader("Summary")
                st.write(result["response"])

            else:
                st.error(
                    f"Ollama error: {response.status_code}"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to Ollama. Make sure Ollama is running."
            )