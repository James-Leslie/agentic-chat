"""
1_basic_agent.py - Introduction to Pydantic AI Agents

This example demonstrates how to create and use a basic Pydantic AI agent
with synchronous operations.
"""

from dotenv import load_dotenv
from pydantic_ai import Agent

# Load environment variables (API keys)
load_dotenv()

# Create a simple agent that uses GPT-4o-mini
agent = Agent(
    "openai:gpt-4o-mini",  # expects an OPENAI_API_KEY environment variable
    system_prompt="You are a helpful assistant that provides concise responses.",
)

if __name__ == "__main__":
    result = agent.run_sync("What is Pydantic?")
    print(result.data)
