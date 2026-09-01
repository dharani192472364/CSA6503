
import streamlit as st
import torch
from diffusers import StableDiffusionPipeline, DDIMScheduler

st.title("Engineering Image Prompt Comparison")

@st.cache_resource
def load_model():

    model_id = "runwayml/stable-diffusion-v1-5"

    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float32
    )

    # Use DDIM instead of PNDM
    pipe.scheduler = DDIMScheduler.from_config(
        pipe.scheduler.config
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"

    pipe = pipe.to(device)

    return pipe


pipe = load_model()

prompt1 = st.text_input(
    "Prompt 1",
    "A simple bridge over a river"
)

prompt2 = st.text_input(
    "Prompt 2",
    "A futuristic suspension bridge over a river at night"
)


if st.button("Generate Images"):

    with st.spinner("Generating images..."):

        image1 = pipe(
            prompt1,
            num_inference_steps=10
        ).images[0]

        image2 = pipe(
            prompt2,
            num_inference_steps=10
        ).images[0]

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            image1,
            caption="Prompt 1",
            use_container_width=True
        )

    with col2:
        st.image(
            image2,
            caption="Prompt 2",
            use_container_width=True
        )

    st.success("Images generated successfully!")

    st.write("### Comparison")
    st.write(
        "The first prompt generates a simple bridge, "
        "while the second prompt generates a futuristic "
        "bridge with a night environment."
    )
