# Streamlit chat examples
Simple examples of using Streamlit for Generative AI chat applications.

## Environment setup

### 1. Environment variables
This app requires certain environment variables to be set for API keys.   
You can use the provided `.env.example` file as a template to create your own `.env` file.   
Make sure to set the values of the necessary API keys using your own keys.

Accounts you will need to sign up for:
- [Anthropic](https://platform.claude.com)
- [LangSmith](https://smith.langchain.com)

> ⚠️ IMPORTANT: Without this file and the correct API keys, the app will not function properly.

### 2. Python dependencies
```bash
uv sync
```

### 3. Run the main app
The main entry point is `app/app.py`. All example chat apps are in the `app/pages/` folder and will appear as selectable pages in the Streamlit sidebar.

```bash
uv run streamlit run app/app.py
```

## File structure
The main structure of the app is as follows:
```
app/
|__ app.py
|__ pages/
|____ <page1>.py
|____ <page2>.py
|__ visual_utils.py
```

`app.py` is the main entry point for the Streamlit app.   
This file performs a few tasks that are common to all pages:
- Loads environment variables from the `.env` file
- Sets up the Streamlit page configuration
- Define the page navigation structure

This means we don't have to repeat these steps in each example page.

The `pages/` folder contains different example chat applications. Each file in this folder represents a separate page in the Streamlit app.   
Current example pages include:
- `openai.py`: Basic chat app that uses the `openai` Python SDK directly.
- `langchain.py`: Chat app that uses the `langchain` Python SDK.
- `tool_calling.py`: Chat app that demonstrates calling tools using the `langchain` Python SDK.

Lastly, `visual_utils.py` contains utility functions for rendering chat messages in the Streamlit app.

## References
- [Build a basic LLM chat app | Streamlit](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)

## To do:
  - Use `StreamlitCallbackHandler` to display thoughts and actions of agent
    - https://docs.langchain.com/oss/python/integrations/callbacks/streamlit#additional-scenarios
    - https://github.com/langchain-ai/langchain-community/blob/main/libs/community/langchain_community/callbacks/streamlit/streamlit_callback_handler.py