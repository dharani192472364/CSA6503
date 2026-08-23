import streamlit as st

from chatbot import FAQChatbot


# Page configuration
st.set_page_config(
    page_title="College FAQ AI Chatbot",
    page_icon="🎓",
    layout="centered"
)


# Title
st.title("🎓 College FAQ Generative AI Chatbot")

st.write(
    "Ask questions about academics, attendance, "
    "examinations, library, placements, facilities "
    "and student services."
)


# Load chatbot
@st.cache_resource
def load_chatbot():
    return FAQChatbot()


with st.spinner("Loading AI chatbot..."):
    chatbot = load_chatbot()


# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User input
user_query = st.chat_input(
    "Ask your question..."
)


if user_query:

    user_query = user_query.strip()

    # Empty input handling
    if not user_query:

        st.warning(
            "Please enter a question before submitting."
        )

    else:

        # Display user question
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_query
            }
        )

        with st.chat_message("user"):
            st.markdown(user_query)


        # Generate answer
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer, results = chatbot.generate_answer(
                    user_query
                )

            st.markdown(answer)


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


# Sidebar
with st.sidebar:

    st.header("📚 About")

    st.write(
        "This chatbot uses semantic search and "
        "Generative AI to answer college FAQ questions."
    )

    st.subheader("Technologies")

    st.write(
        """
        - Python
        - Streamlit
        - Sentence Transformers
        - FAISS
        - Ollama
        - Llama 3.2
        """
    )

    st.subheader("Example Questions")

    st.write(
        """
        • How can I check my attendance?

        • How do I borrow a library book?

        • How can I prepare for placements?

        • What should I do if Wi-Fi isn't working?

        • Where can I find my syllabus?
        """
    )


# Clear chat button
if st.sidebar.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    st.rerun()
    