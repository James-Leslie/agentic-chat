# Description: A basic chat application using Streamlit and OpenAI.
# https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps

import os

import streamlit as st
from openai import OpenAI

st.title("💬 ChatGPT-like clone")
st.markdown("An example of a basic chat app using the `openai` Python client library.")

# ------------------------------------------------------ 1. Initialize the OpenAI client
# OpenAI client
client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

# ------------------------------------------------------------ 2. Show previous messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------------------------------------------------------- 3. Accept user input
# ------------------------------------------------- + 4. Generate response and stream it
if prompt := st.chat_input("Ask a question"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
