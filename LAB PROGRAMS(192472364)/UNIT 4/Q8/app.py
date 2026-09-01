
import streamlit as st
from transformers import pipeline

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Engineering Document Translator",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Engineering Document Translator")

st.write(
    "Translate an engineering document from English "
    "into an Indian language using a pre-trained "
    "multilingual translation model."
)

# =========================================================
# LANGUAGE SELECTION
# =========================================================

languages = {
    "Hindi": "hin_Deva",
    "Tamil": "tam_Taml",
    "Telugu": "tel_Telu",
    "Kannada": "kan_Knda",
    "Malayalam": "mal_Mlym"
}

target_language = st.selectbox(
    "Select target Indian language",
    list(languages.keys())
)

# =========================================================
# LOAD MULTILINGUAL MODEL
# =========================================================

@st.cache_resource
def load_model():

    return pipeline(
        "translation",
        model="facebook/nllb-200-distilled-600M"
    )

# =========================================================
# DOCUMENT INPUT
# =========================================================

uploaded_file = st.file_uploader(
    "Upload an English engineering document",
    type=["txt"]
)

text_input = st.text_area(
    "Or enter engineering text manually",
    height=200,
    placeholder="Enter engineering text here..."
)

# =========================================================
# TRANSLATE
# =========================================================

if st.button("🌐 Translate"):

    # -----------------------------------------------------
    # GET INPUT TEXT
    # -----------------------------------------------------

    if uploaded_file is not None:

        english_text = uploaded_file.read().decode(
            "utf-8",
            errors="ignore"
        )

    elif text_input.strip():

        english_text = text_input

    else:

        st.warning(
            "Please upload a document or enter text."
        )

        st.stop()

    # -----------------------------------------------------
    # LOAD MODEL
    # -----------------------------------------------------

    with st.spinner(
        "Loading multilingual translation model..."
    ):

        try:

            translator = load_model()

        except Exception as e:

            st.error(
                f"Could not load translation model: {e}"
            )

            st.stop()

    # -----------------------------------------------------
    # SPLIT DOCUMENT INTO SENTENCES
    # -----------------------------------------------------

    sentences = []

    for line in english_text.splitlines():

        line = line.strip()

        if line:
            sentences.append(line)

    if not sentences:

        st.error("No readable text found.")

        st.stop()

    # -----------------------------------------------------
    # TRANSLATION
    # -----------------------------------------------------

    translated_parts = []

    target_code = languages[target_language]

    with st.spinner(
        f"Translating English → {target_language}..."
    ):

        try:

            for sentence in sentences:

                result = translator(
                    sentence,
                    src_lang="eng_Latn",
                    tgt_lang=target_code,
                    max_length=512
                )

                translated_parts.append(
                    result[0]["translation_text"]
                )

        except Exception as e:

            st.error(
                f"Translation error: {e}"
            )

            st.stop()

    translated_text = "\n".join(
        translated_parts
    )

    # =====================================================
    # DISPLAY ORIGINAL
    # =====================================================

    st.subheader("🇬🇧 Original English Document")

    st.text_area(
        "English",
        english_text,
        height=250
    )

    # =====================================================
    # DISPLAY TRANSLATION
    # =====================================================

    st.subheader(
        f"🌐 {target_language} Translation"
    )

    st.text_area(
        target_language,
        translated_text,
        height=250
    )

    # =====================================================
    # DOWNLOAD
    # =====================================================

    st.download_button(
        label="⬇️ Download Translation",
        data=translated_text,
        file_name=(
            f"engineering_translation_"
            f"{target_language}.txt"
        ),
        mime="text/plain"
    )

# =========================================================
# EXAMPLE
# =========================================================

st.markdown("---")

st.subheader("💡 Example Engineering Text")

st.write(
    "A transformer is an electrical device that transfers "
    "electrical energy between two circuits."
)

st.write(
    "Robotic systems use sensors, actuators and controllers "
    "to perform automated tasks."
)

st.markdown("---")

st.caption(
    "Powered by Hugging Face Transformers and NLLB-200"
)
