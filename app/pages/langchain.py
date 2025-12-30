# https://docs.langchain.com/oss/python/langchain/quickstart

import streamlit as st
from langchain.agents import create_agent
from langchain_core.messages import convert_to_openai_messages
from langgraph.checkpoint.memory import InMemorySaver

st.title("🦜🔗 LangChain Agent Chat")
st.markdown("An example of a basic chat application using the `langchain` Python SDK.")

# ---------------------------------------------------- 1. Initialize the LangChain agent
if "memory" not in st.session_state:
    st.session_state.memory = InMemorySaver()
    st.session_state.config = {"configurable": {"thread_id": "1"}}

# simple agent without tools
agent = create_agent(
    model="claude-haiku-4-5",
    checkpointer=st.session_state.memory,
    system_prompt="You are a helpful assistant.",
)

# ------------------------------------------------------------ 2. Show previous messages
# Get previous messages from the agent's state
messages = agent.get_state(st.session_state.config).values.get("messages")

if messages:
    # Display chat messages from history on app rerun
    messages = convert_to_openai_messages(messages)
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# ----------------------------------------------------------------- 3. Accept user input
if prompt := st.chat_input("Ask a question"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # --------------------------------------------- + 4. Generate response and render it
    def langchain_stream_to_chunks(stream):
        """Helper function to convert LangChain stream to a generator compatible with Streamlit."""
        for chunk, _ in stream:
            # Only yield non-empty content
            if hasattr(chunk, "content") and chunk.content:
                yield chunk.content

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # Invoke the agent to get a response
        stream = agent.stream(
            {"messages": [{"role": "user", "content": prompt}]},
            config=st.session_state.config,
            stream_mode="messages",
        )
        st.write_stream(langchain_stream_to_chunks(stream))
