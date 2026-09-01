import streamlit as st
import torch
from diffusers import StableDiffusionPipeline

st.title("Engineering Image Generator")

@st.cache_resource
def load_model():
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5"
    )
    return pipe.to("cuda" if torch.cuda.is_available() else "cpu")

pipe = load_model()

prompt = st.text_input(
    "Enter an engineering image prompt:",
    "A modern suspension bridge over a river"
)

if st.button("Generate Image"):
    image = pipe(prompt, num_inference_steps=20).images[0]
    st.image(image, caption=prompt)
    