# Project Overview

**agentic-chat** is a collection of educational Streamlit chat applications demonstrating different approaches to building Generative AI chat interfaces.

## Purpose
This repository serves as a hands-on learning resource for developers exploring AI chat applications. It provides working examples that showcase:
- Direct integration with LLM APIs (OpenAI SDK)
- Framework-based development (LangChain)
- Advanced agentic features, e.g. tool calling

## Tech Stack
- **Frontend:** Streamlit (for rapid UI prototyping)
- **AI/LLM Frameworks:**
  - OpenAI Python SDK (direct API usage)
  - LangChain v1.x (agent framework)
- **Package Management:** uv (modern Python package manager)
- **Python Version:** 3.13+

## Project Structure
- [`app/app.py`](app/app.py) - Main entry point and shared configuration
- [`app/pages/`](app/pages/) - Individual chat example implementations
  - [`openai.py`](app/pages/openai.py) - Basic chat using OpenAI SDK directly
  - [`langchain.py`](app/pages/langchain.py) - Chat using LangChain framework
  - [`tool_calling.py`](app/pages/tool_calling.py) - Agent with tool execution capabilities
- [`app/visual_utils.py`](app/visual_utils.py) - Shared UI rendering utilities

# Essential Tools

## 1. Python Package Management - `uv`
**CRITICAL:** Use `uv` for ALL Python package operations. NEVER use `pip`, `python`, or `conda`.

**Common Commands:**
- `uv run <script>` - Run any Python script
- `uvx <package>` - Run a package as a CLI tool
- `uv add/remove <package>` - Add/remove dependency
- `uv sync` - Sync dependencies

**⚠️ IMPORTANT:** `uv` is a new tool (2024). When unsure about any `uv` command or behavior, ALWAYS search the official documentation: `https://docs.astral.sh/uv/`.