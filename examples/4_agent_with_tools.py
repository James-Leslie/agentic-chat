"""
Working with tools

This example demonstrates how to create and use tools with a Pydantic AI agent.
Tools allow agents to perform actions and retrieve information during their reasoning.

There are a number of ways to register tools with an agent:

  - via the @agent.tool decorator — for tools that need access to the agent context
  - via the @agent.tool_plain decorator — for tools that do not need access to the agent context
  - via the tools keyword argument to Agent which can take either plain functions, or instances of Tool

@agent.tool is considered the default decorator since in the majority of cases tools will need access to the agent context.
"""

import random

import nest_asyncio
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

# Load environment variables (API keys)
load_dotenv()

# This is needed if running in a notebook environment
# See here for details: https://ai.pydantic.dev/troubleshooting/
nest_asyncio.apply()


# Create a player schema
class Player(BaseModel):
    name: str = Field(description="The name of the player")


# Create an agent
agent = Agent(
    "openai:gpt-4o-mini",  # expects an OPENAI_API_KEY environment variable
    system_prompt=(
        "You are a dice game, you should roll the dice and see if the number you get "
        "back matches the number the user asked for. "
        "Use the player's name in the response."
    ),
)


# Add a plain tool (which does not need access to the agent context)
@agent.tool_plain
def roll_dice() -> int:
    """Roll two six-sided die and return the sum of the results."""
    return random.randint(1, 6) + random.randint(1, 6)


# Add a tool that uses the agent context
@agent.tool
def get_player_name(ctx: RunContext[str]) -> str:
    """Get the player's name."""
    return ctx.deps.name  # retrieves the name from the dependency


dice_result = agent.run_sync("My guess is 7", deps=Player(name="John"))

# show the messages
for message in dice_result.all_messages():
    print(message)

# show the final response
print(dice_result.data)
