"""
Working with structured output in Pydantic AI

This example demonstrates how to get structured, type-safe results from Pydantic AI agents
using Pydantic models for validation and schema definition.
"""

from enum import Enum

import nest_asyncio
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent

# Load environment variables (API keys)
load_dotenv()

# This is needed if running in a notebook environment
# See here for details: https://ai.pydantic.dev/troubleshooting/
nest_asyncio.apply()


# Define an enum for the sentiment of the user's last message
# See here for details: https://docs.pydantic.dev/1.10/usage/types/#enums-and-choices
class Sentiment(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"


# Define a structured output model using Pydantic
class ResponseModel(BaseModel):
    response: str = Field(description="The response to the user's last message")
    sentiment: Sentiment


# Create an agent that returns structured data
agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="You are a helpful customer support agent.",
    result_type=ResponseModel,
)

# Example usage of agent with structured output
response = agent.run_sync(
    "Please stop passing me from one department to another! I need help reseting my password"
)
print(response.data.model_dump_json(indent=2))
