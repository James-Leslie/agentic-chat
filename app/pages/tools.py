# https://docs.langchain.com/oss/python/langchain/quickstart
import time

import streamlit as st
import sympy
from langchain.agents import create_agent
from langchain.messages import AIMessage, AIMessageChunk, HumanMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver

st.title("🦜🔗 LangChain Agent Chat")
st.markdown("Tool calling example using the `langchain` Python SDK.")

# ---------------------------------------------------- 1. Initialize the LangChain agent
if "memory" not in st.session_state:
    st.session_state.memory = InMemorySaver()
    st.session_state.config = {"configurable": {"thread_id": "1"}}


# Create a calculation tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression.
    Args:
        expression (str): Python arithmetic expression to calculate.
    Returns:
        str: The result of the calculation.
    """
    try:
        time.sleep(3)  # Simulate some delay
        result = sympy.sympify(expression).evalf()
        return result
    except Exception as e:
        return f"Error calculating expression: {e}"


# Create the agent by combining the LLM and the tool(s)
agent = create_agent(
    model="gpt-5-nano",  # doesn't work with anthropic models currently (message chunk content is a list instead of str)
    tools=[calculate],
    checkpointer=st.session_state.memory,
    system_prompt="You are a helpful maths assistant. Use your calculator to help with maths problems.",
)

# ------------------------------------------------------------ 2. Show previous messages
# Get previous messages from the agent's state
messages = agent.get_state(st.session_state.config).values.get("messages")

if messages:
    # Extract all tool calls for all messages
    # ToolMessages do not contain the args used to call the tool, so we need to find the
    # corresponding tool call from the AIMessage that initiated it.
    tool_calls = {
        call["id"]: call
        for message in messages
        if hasattr(message, "tool_calls")
        for call in message.tool_calls
    }
    # Display chat messages from history on app rerun
    for message in messages:
        # Tool response message
        if isinstance(message, ToolMessage):
            with st.chat_message("assistant", avatar="🛠️"):
                # Find the corresponding tool call to get args
                tool_call_args = tool_calls.get(message.tool_call_id).get("args", {})
                # Show the tool call as an expander
                with st.expander(f"**`{message.name}`**"):
                    st.markdown("**Args:**")
                    for arg in tool_call_args.keys():
                        st.markdown(f"`{arg}`:")
                        st.code(tool_call_args[arg])
                    st.markdown("**Output:**")
                    st.write(message.content)
        # AI message or Human message
        elif isinstance(message, (AIMessage, HumanMessage)) and message.content:
            with st.chat_message(message.type):
                st.markdown(message.content)


# ----------------------------------------------------------------- 3. Accept user input
if prompt := st.chat_input("Ask a question"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        response = ""
        tool_spinner_active = False
        spinner_context = None

        stream = agent.stream(
            {"messages": [{"role": "user", "content": prompt}]},
            config=st.session_state.config,
            stream_mode=["messages", "updates"],
        )

        for stream_mode, data in stream:
            if stream_mode == "messages":
                token, metadata = data

                # --- 1. Detect tool call in AIMessageChunk ---
                if isinstance(token, AIMessageChunk):
                    tool_calling = (
                        hasattr(token, "tool_calls") and token.tool_calls
                    ) or (hasattr(token, "tool_call_chunks") and token.tool_call_chunks)
                    if tool_calling:
                        if not tool_spinner_active:
                            spinner_context = st.spinner("Calling tool...")
                            spinner_context.__enter__()
                            tool_spinner_active = True
                        continue
                    if not tool_spinner_active and token.content:
                        response += token.content
                        placeholder.markdown(response)

                # --- 2. ToolMessage means tool is done ---
                elif isinstance(token, ToolMessage):
                    if tool_spinner_active and spinner_context:
                        spinner_context.__exit__(None, None, None)
                        spinner_context = None
                        tool_spinner_active = False

        st.rerun()  # Hack: would be better to handle the tool expander in the loop above
