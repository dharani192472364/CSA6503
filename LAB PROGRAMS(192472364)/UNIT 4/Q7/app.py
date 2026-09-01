
import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Engineering Document Summarizer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Engineering Document Summarizer")

st.write(
    "Upload a lengthy engineering document and generate "
    "a short and meaningful summary using a pre-trained "
    "Generative AI model."
)

# =========================================================
# LOAD API KEY
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found in .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

# =========================================================
# FILE UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "Upload an engineering document",
    type=["pdf", "txt"]
)

# =========================================================
# EXTRACT TEXT
# =========================================================

def extract_text(file):

    if file.type == "application/pdf":

        reader = PdfReader(file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    else:

        return file.read().decode(
            "utf-8",
            errors="ignore"
        )

# =========================================================
# SUMMARIZATION
# =========================================================

if uploaded_file is not None:

    st.success(
        f"File uploaded: {uploaded_file.name}"
    )

    if st.button("📝 Generate Summary"):

        with st.spinner("Reading engineering document..."):

            document_text = extract_text(uploaded_file)

        if not document_text.strip():

            st.error(
                "No readable text was found in the document."
            )

            st.stop()

        st.info(
            f"Extracted approximately "
            f"{len(document_text):,} characters."
        )

        # -------------------------------------------------
        # LIMIT TEXT TO A SAFE SIZE
        # -------------------------------------------------

        max_chars = 30000

        if len(document_text) > max_chars:

            document_text = document_text[:max_chars]

            st.warning(
                "The document is very large, so the first "
                "30,000 characters were summarized."
            )

        # -------------------------------------------------
        # PROMPT
        # -------------------------------------------------

        prompt = f"""
You are an engineering document summarization assistant.

Read the engineering document below and create a concise,
meaningful summary.

Include:

1. Main topic
2. Important concepts
3. Key technical points
4. Important results or findings
5. Conclusion

Use simple technical language suitable for an engineering
student.

Do not invent information that is not present in the document.

ENGINEERING DOCUMENT:

{document_text}
"""

        # -------------------------------------------------
        # GEMINI
        # -------------------------------------------------

        with st.spinner("Generating AI summary..."):

            try:

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                summary = response.text

            except Exception as e:

                st.error(
                    f"Error generating summary: {e}"
                )

                st.stop()

        # -------------------------------------------------
        # DISPLAY SUMMARY
        # -------------------------------------------------

        st.subheader("📌 Generated Summary")

        st.markdown(summary)

        # -------------------------------------------------
        # DOWNLOAD SUMMARY
        # -------------------------------------------------

        st.download_button(
            label="⬇️ Download Summary",
            data=summary,
            file_name="engineering_summary.txt",
            mime="text/plain"
        )

# =========================================================
# INFORMATION
# =========================================================

st.markdown("---")

st.subheader("📚 Example Documents")

st.write("• Machine Learning Research Paper")
st.write("• Structural Engineering Report")
st.write("• Electrical Engineering Notes")
st.write("• Robotics Technical Document")
st.write("• Civil Engineering Project Report")

st.markdown("---")

st.caption(
    "Powered by Google Gemini and Streamlit"
)
