import streamlit as st
import ollama

st.title("📄 Engineering Document Summarizer")

text = st.text_area(
    "Enter lengthy text:"
)

if st.button("Summarize"):

    if text.strip():

        prompt = f"""
Summarize the following engineering text
in a concise and meaningful way.

Text:
{text}

Summary:
"""

        response = ollama.generate(
            model="llama3.2",
            prompt=prompt
        )

        st.subheader("Summary")

        st.write(
            response["response"]
        )

    else:

        st.warning(
            "Please enter some text."
        )