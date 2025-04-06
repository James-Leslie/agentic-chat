# Pydantic AI Tutorial Project

A tutorial project for learning and experimenting with Pydantic AI, a powerful framework for building AI applications with Large Language Models (LLMs).

## Project Overview

This project provides a structured learning path for Pydantic AI, featuring:

- Step-by-step tutorial examples
- Clean, well-documented code
- Progressive learning from basic to advanced concepts
- Focus on practical implementation patterns

## Learning Path

The examples in the `examples/` directory are organized to introduce Pydantic AI concepts progressively:

1. **Basic Agents**: Creating and running simple AI agents
2. **Function Tools**: Extending agents with custom tools and functionality
3. **Structured Results**: Working with type-safe, validated outputs
4. **More to come!** Future tutorials will cover streaming, chat history, and more

## Project Structure

```
pydantic-ai-tutorial/
├── .cursor/           # Cursor AI IDE configuration
├── examples/          # Tutorial examples
│   ├── 1_basic_agent.py
│   ├── 2_agent_with_tools.py
│   ├── 3_structured_results.py
│   └── README.md      # Example-specific documentation
├── pyproject.toml     # Project dependencies
└── README.md          # This file
```

## Getting Started

1. Clone this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   or with uv:
   ```bash
   uv pip install -r requirements.txt
   ```
4. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
5. Run the examples:
   ```bash
   python examples/1_basic_agent.py
   ```

## Features Covered

- ✅ Basic AI agents
- ✅ Function tools
- ✅ Structured results with Pydantic models
- 🔲 Streaming responses
- 🔲 Chat history and conversations
- 🔲 Error handling and retries
- 🔲 Multi-agent systems

## Resources

- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [OpenAI API Documentation](https://platform.openai.com/docs/introduction)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## License

MIT
