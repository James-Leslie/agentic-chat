"""
1_basic_agent.py - Introduction to Pydantic AI Agents

This example demonstrates how to create and use a basic Pydantic AI agent
with synchronous operations.
"""

import nest_asyncio
from dotenv import load_dotenv
from pydantic_ai import Agent

# Load environment variables (API keys)
load_dotenv()

# This is needed if running in a notebook environment
# See here for details: https://ai.pydantic.dev/troubleshooting/
nest_asyncio.apply()

# Create a simple agent that uses GPT-4o-mini
agent = Agent(
    "openai:gpt-4o-mini",  # expects an OPENAI_API_KEY environment variable
    system_prompt="You are a helpful assistant that provides concise responses.",
)

# Example usage of basic agent
response = agent.run_sync("What is Pydantic?")
print(response.data)
print(response.all_messages())


response = agent.run_sync(
    user_prompt="What was my previous question?",
    message_history=response.new_messages(),
)
print(response.data)
