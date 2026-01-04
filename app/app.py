# https://docs.langchain.com/oss/python/langchain/quickstart

import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

st.set_page_config(
    page_title="Agent chat",  # Shows up as the name of the browser tab
    page_icon=":material/robot:",  # Favicon for the browser tab
    layout="centered",
)

pg = st.navigation(
    [
        st.Page("pages/openai.py", title="OpenAI", icon=":material/cyclone:"),
        st.Page("pages/langchain.py", title="LangChain", icon=":material/raven:"),
        st.Page(
            "pages/tool_calling.py", title="Tool Calling", icon=":material/handyman:"
        ),
    ],
    position="top",
)
pg.run()
