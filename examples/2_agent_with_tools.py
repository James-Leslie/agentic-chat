"""
2_agent_with_tools.py - Working with tools in Pydantic AI

This example demonstrates how to create and use tools with a Pydantic AI agent.
Tools allow agents to perform actions and retrieve information during their reasoning.
"""

import random
from datetime import datetime

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext

# Load environment variables (API keys)
load_dotenv()

# Create an agent with tools
agent = Agent(
    "openai:gpt-4o-mini",  # expects an OPENAI_API_KEY environment variable
    system_prompt="You are a helpful assistant that can perform various tasks using tools.",
)


# Function tools are defined using the @agent.tool decorator
@agent.tool
def get_current_time(ctx: RunContext, timezone: str = "UTC") -> str:
    """Get the current date and time in the specified timezone.

    Args:
        ctx: The run context
        timezone: The timezone to use (default: "UTC")
    """
    import pytz

    if timezone not in pytz.all_timezones:
        raise ValueError(f"Invalid timezone: {timezone}")

    now = datetime.now(tz=pytz.timezone(timezone))
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")


@agent.tool
def roll_dice(ctx: RunContext, sides: int = 6) -> int:
    """Roll a dice with the specified number of sides. Default is 6 sides."""
    if sides < 2:
        raise ValueError("A dice must have at least 2 sides.")
    return random.randint(1, sides)


@agent.tool
def calculate_area(ctx: RunContext, length: float, width: float) -> float:
    """Calculate the area of a rectangle with the given length and width."""
    return length * width


if __name__ == "__main__":
    # Run the agent with a prompt that will likely trigger tool usage
    print("Tool example - querying the time")
    result = agent.run_sync("What time is it right now?")
    print(result.data)
    print("-" * 50)

    print("Tool example - rolling dice")
    result = agent.run_sync("Roll a 20-sided dice for me.")
    print(result.data)
    print("-" * 50)

    print("Tool example - calculating area")
    result = agent.run_sync(
        "What's the area of a rectangle that's 5.5 meters by 3.2 meters?"
    )
    print(result.data)
    print("-" * 50)

    # Example of a more complex interaction where the agent needs to use multiple tools
    print("Complex example - using multiple tools")
    result = agent.run_sync(
        "Tell me what time it is, then roll two dice - one with 6 sides and one with 10 sides. "
        "Finally, calculate the area of a square with sides equal to the sum of the dice rolls."
    )
    print(result.data)
