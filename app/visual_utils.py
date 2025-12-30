import time
from typing import Any, Dict, Generator, List

import streamlit as st


def generate_message_stream(content: str) -> Generator[str, None, None]:
    """Yield message content one character at a time."""
    for char in content:
        yield char
        time.sleep(0.01)


def stream_langchain_messages(stream):
    """
    Extract content from LangChain message stream for use with st.write_stream().

    Converts LangGraph's stream_mode="messages" output (which yields tuples of
    (message_chunk, metadata)) into simple content strings that Streamlit can display.

    Args:
        stream: LangGraph stream iterator with stream_mode="messages"

    Yields:
        str: Content chunks from the message stream
    """
    for chunk, metadata in stream:
        if chunk.content:
            yield chunk.content


def display_empty_chat() -> None:
    """
    Display the initial empty chat interface with title, description, chat input, and example suggestions.
    """

    st.title("🦜🔗 LangChain Agent Chat")
    st.markdown(
        "An example of a basic chat application using the `langchain` Python SDK."
    )
    with st.container():
        st.chat_input("How can I help you today?", key="initial_prompt")

        suggestions = st.session_state.starter_prompts

        selected_suggestion = st.pills(
            label="Examples",
            label_visibility="collapsed",
            options=suggestions.keys(),
        )

        # Map the selected suggestion option to its corresponding prompt
        st.session_state.selected_suggestion = suggestions.get(selected_suggestion)


def display_message(message: object, stream_mode: bool = False) -> None:
    """
    Display a single LangGraph message in the Streamlit chat interface.

    Types of messages:
    - Human messages
    - AI messages
    - AI tool calls
    - Tool response messages

    Args:
        message (object): A message object with attributes 'type', 'content', and optionally 'tool_calls' or 'name'.
        stream_mode (bool, optional): If True, simulates streaming/typing effect. Defaults to False.
    """
    role = message.type
    content = message.content

    match role:
        # 1. Human message
        case "human":
            with st.chat_message("user"):
                # simply show the text
                st.markdown(content)
        # 2. Tool response message
        case "tool":
            with st.chat_message("assistant", avatar="🛠️"):
                if stream_mode:
                    with st.spinner("Calling tool..."):
                        time.sleep(0.3)
                with st.expander(f"**tool output**: `{message.name}`"):
                    st.markdown(f"`{content}`")
        # 3. AI message or 4. AI tool call
        case "ai":
            if tool_calls := getattr(message, "tool_calls", None):
                # show tool calls in expanders
                for tool_call in tool_calls:
                    tool_name = tool_call.get("name")
                    tool_args = tool_call.get("args")
                    with st.chat_message("assistant", avatar="🛠️"):
                        if stream_mode:
                            with st.spinner("Calling tool..."):
                                time.sleep(0.3)
                        with st.expander(f"**tool input**: `{tool_name}`"):
                            st.markdown(f"`{tool_args}`")
            else:
                with st.chat_message("assistant"):
                    if stream_mode:
                        stream = generate_message_stream(content)
                        st.write_stream(stream)
                    else:
                        st.markdown(content)
        case _:
            st.warning(f"Unknown message role: {role}")


def display_conversation(messages: list, stream_mode: bool = False) -> None:
    """
    Display a sequence of chat messages in the Streamlit chat interface.

    Args:
        messages (list): List of message objects to display.
        stream_mode (bool, optional): If True, simulates streaming/typing effect for all messages. Defaults to False.
    """
    for message in messages:
        display_message(message, stream_mode=stream_mode)


def unpack_agent_updates(agent_update_list: List[Dict[str, Any]]) -> List[Any]:
    """
    Flatten all messages from a langchain agent.invoke output (stream_mode='updates').

    Args:
        agent_response (list[dict]):
            Output from agent.invoke with stream_mode='updates'.
            Each item is a dict with a single key ('model' or 'tools'), whose value is a dict containing a 'messages' list.

    Returns:
        list: Flat list of all message objects from all 'messages' lists in the input.

    Example:
        >>> output = [
        ...     {'model': {'messages': [AIMessage(...)]}},
        ...     {'tools': {'messages': [ToolMessage(...)]}},
        ... ]
        >>> unpack_agent_updates(output)
        >>> [AIMessage(...), ToolMessage(...)]
    """
    return [m for d in agent_update_list for key in d for m in d[key]["messages"]]
