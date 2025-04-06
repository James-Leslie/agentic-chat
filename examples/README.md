# Pydantic AI Tutorial Examples
This folder contains tutorial examples for learning Pydantic AI, a powerful framework for building AI applications with LLMs.

## Running the Examples
Each example can be run using `uv`:

```bash
uv run examples/1_basic_agent.py
```

## Examples Overview

### 1. Basic Agent

**1_basic_agent.py**: Introduction to creating and running a basic Pydantic AI agent.
- Creates a simple agent with GPT-4o-mini
- Demonstrates how to make a synchronous query
- Shows how to access the response data

### 2. Agents with Tools

**2_agent_with_tools.py**: Using function tools with Pydantic AI agents.
- Demonstrates how to create tools using the `@agent.tool` decorator
- Shows how tools can access the RunContext
- Includes examples of parameter validation and error handling
- Demonstrates how the agent can use multiple tools in a single conversation

### 3. Structured Results

**3_structured_results.py**: Working with structured, type-safe outputs.
- Shows how to define output schemas using Pydantic models
- Demonstrates validation of structured outputs
- Includes examples of field constraints and validation
- Shows how to access and work with the structured data

## Learning Path

It's recommended to go through the examples in order, as they build on concepts introduced in previous examples. Each tutorial introduces progressively more advanced features of the Pydantic AI framework.

Future tutorials may cover:
- Streaming responses
- Chat history and conversation management
- Error handling and retries
- Multi-agent systems
- Integration with external APIs

## Troubleshooting

If your examples get stuck:

1. Check your OpenAI API key is valid and has sufficient credits
2. Ensure you have a stable internet connection
3. Look for any error messages in the console output
4. Make sure you have the latest version of pydantic-ai installed

Happy coding with Pydantic AI! 