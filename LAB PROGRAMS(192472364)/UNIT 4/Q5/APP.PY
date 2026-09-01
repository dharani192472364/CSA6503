
import streamlit as st
from transformers import pipeline
import imageio_ffmpeg
import soundfile as sf
import subprocess
import tempfile
import os

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Engineering Speech-to-Text",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Engineering Speech-to-Text")

st.write(
    "Convert an engineering-related spoken query into "
    "written text using a pre-trained Whisper model."
)

# =========================================================
# FFMPEG
# =========================================================

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# =========================================================
# LOAD WHISPER
# =========================================================

@st.cache_resource
def load_model():
    return pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-tiny"
    )

with st.spinner("Loading Whisper model..."):
    model = load_model()

st.success("Whisper model loaded successfully!")

# =========================================================
# UPLOAD AUDIO
# =========================================================

audio_file = st.file_uploader(
    "Upload an engineering-related audio file",
    type=["mp3", "wav", "m4a", "ogg", "flac"]
)

# =========================================================
# SPEECH TO TEXT
# =========================================================

if audio_file is not None:

    st.audio(audio_file)

    if st.button("🎯 Convert Speech to Text"):

        input_file = None
        output_file = None

        try:

            # -------------------------------------------------
            # SAVE UPLOADED FILE
            # -------------------------------------------------

            extension = os.path.splitext(
                audio_file.name
            )[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=extension
            ) as f:

                f.write(audio_file.getvalue())
                input_file = f.name

            # -------------------------------------------------
            # CREATE WAV FILE
            # -------------------------------------------------

            output_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".wav"
            ).name

            st.info("Converting audio to WAV...")

            command = [
                FFMPEG,
                "-y",
                "-i",
                input_file,
                "-ar",
                "16000",
                "-ac",
                "1",
                "-sample_fmt",
                "s16",
                output_file
            ]

            process = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if process.returncode != 0:

                st.error("Audio conversion failed.")
                st.code(process.stderr)

                st.stop()

            # -------------------------------------------------
            # READ WAV DIRECTLY USING SOUNDFILE
            # -------------------------------------------------

            st.info("Reading converted audio...")

            audio_data, sample_rate = sf.read(
                output_file,
                dtype="float32"
            )

            # -------------------------------------------------
            # TRANSCRIBE USING NUMPY ARRAY
            # -------------------------------------------------

            st.info("Converting speech to text...")

            result = model(
                {
                    "raw": audio_data,
                    "sampling_rate": sample_rate
                }
            )

            text = result["text"].strip()

            # -------------------------------------------------
            # DISPLAY RESULT
            # -------------------------------------------------

            st.subheader("📝 Transcribed Engineering Query")

            st.text_area(
                "Recognized Text",
                text,
                height=150
            )

            st.success(
                "Speech successfully converted to text!"
            )

        except Exception as e:

            st.error(
                f"Error during transcription: {e}"
            )

        finally:

            if input_file and os.path.exists(input_file):
                os.remove(input_file)

            if output_file and os.path.exists(output_file):
                os.remove(output_file)

# =========================================================
# EXAMPLES
# =========================================================

st.markdown("---")

st.subheader("💡 Example Engineering Queries")

st.write(
    "• Explain the working principle of a hydraulic system."
)

st.write(
    "• What is the purpose of a transformer?"
)

st.write(
    "• Explain the working principle of a robotic arm."
)

st.write(
    "• What are the components of a bridge?"
)

st.write(
    "• Explain the function of a microcontroller."
)

st.markdown("---")

st.caption(
    "Powered by Hugging Face Transformers and Whisper"
)