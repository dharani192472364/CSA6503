
import streamlit as st
st.write("PDF SUMMARIZER APP IS RUNNING")
from pdf_summarizer import extract_text_from_pdf
from ollama import chat


st.set_page_config(
    page_title="PDF Document Summarizer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 PDF Document Summarizer")

st.write(
    "Upload a PDF document and generate a concise "
    "AI-powered summary."
)

uploaded_file = st.file_uploader(
    "Upload your PDF document",
    type=["pdf"]
)

summary_length = st.selectbox(
    "Select summary length",
    ["Short", "Medium", "Detailed"]
)


if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("✨ Generate Summary"):

        with st.spinner("Extracting text from PDF..."):

            text, error = extract_text_from_pdf(
                uploaded_file
            )

        if error:

            st.error(error)

        else:

            st.info(
                f"Extracted approximately "
                f"{len(text.split())} words."
            )

            # Limit very large documents
            max_words = 6000
            text_for_summary = " ".join(
                text.split()[:max_words]
            )

            if summary_length == "Short":
                instruction = (
                    "Summarize the document in about "
                    "5 concise sentences."
                )

            elif summary_length == "Medium":
                instruction = (
                    "Summarize the document in about "
                    "10 concise sentences and include "
                    "the major points."
                )

            else:
                instruction = (
                    "Provide a detailed summary covering "
                    "the main concepts, important findings, "
                    "key points, and conclusion."
                )

            prompt = f"""
You are an intelligent document summarization assistant.

Summarize the following PDF content.

{instruction}

Preserve important facts, technical terms,
and important concepts.

Do not invent information that is not present
in the document.

DOCUMENT CONTENT:
{text_for_summary}
"""

            with st.spinner("Generating AI summary..."):

                try:

                    response = chat(
                        model="llama3.2",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                    summary = response[
                        "message"
                    ]["content"]

                    st.subheader("📝 Summary")

                    st.write(summary)

                except Exception as e:

                    st.error(
                        "Unable to generate the summary. "
                        "Make sure Ollama is running and "
                        "the llama3.2 model is available."
                    )

                    st.caption(str(e))

else:

    st.info(
        "Please upload a PDF file to begin."
    )