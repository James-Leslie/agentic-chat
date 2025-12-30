# https://docs.langchain.com/oss/python/langchain/quickstart
import os

import streamlit as st
import sympy
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from visual_utils import display_conversation, unpack_agent_updates

st.title("🦜🔗 LangChain Agent Chat")
st.markdown("An example of a basic chat application using the `langchain` Python SDK.")

# ---------------------------------------------------- 1. Initialize the LangChain agent
if "memory" not in st.session_state:
    st.session_state.memory = InMemorySaver()
    st.session_state.config = {"configurable": {"thread_id": "1"}}

# initialize model using custom endpoint
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


def calculate(expression: str) -> str:
    """Calculate a mathematical expression.
    Args:
        expression (str): Python arithmetic expression to calculate.
    Returns:
        str: The result of the calculation.
    """
    try:
        result = sympy.sympify(expression).evalf()
        return str(result)
    except Exception as e:
        return f"Error calculating expression: {e}"


# create the agent by combining the model and the function
agent = create_agent(
    model=llm,
    tools=[calculate],
    checkpointer=st.session_state.memory,
    system_prompt="You are a helpful maths assistant. Use your calculator to help with maths problems.",
)

# ------------------------------------------------------------ 2. Show previous messages
# Get previous messages from the agent's state
messages = agent.get_state(st.session_state.config).values.get("messages")

if messages:
    # Display chat messages from history on app rerun
    # See visual_utils.py for implementation of display_conversation
    display_conversation(messages)


# ----------------------------------------------------------------- 3. Accept user input
if prompt := st.chat_input("Ask a question"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # --------------------------------------------- + 4. Generate response and render it

    # Display assistant response in chat message container
    # Invoke the agent to get a response
    stream = agent.stream(
        {"messages": [{"role": "user", "content": prompt}]},
        config=st.session_state.config,
        stream_mode="updates",
    )
    for update in stream:
        # Unpack messages from the agent update
        messages = unpack_agent_updates([update])
        # Display the conversation so far
        display_conversation(messages, stream_mode=True)
