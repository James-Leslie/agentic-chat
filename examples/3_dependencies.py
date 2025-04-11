"""
Dependencies in Pydantic AI

This example demonstrates how to pass dependencies to an agent using a dataclass.

The dependencies are passed to the agent using the `deps` parameter in the `run_sync` method.

The dependencies are accessed in the system prompt using the `RunContext` object.

The `RunContext` object is passed to the system prompt as an argument.

"""

import uuid
from typing import List, Optional

import nest_asyncio
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

# Load environment variables (API keys)
load_dotenv()

# This is needed if running in a notebook environment
# See here for details: https://ai.pydantic.dev/troubleshooting/
nest_asyncio.apply()


# Define order schema
class Order(BaseModel):
    """Details of a customer order"""

    order_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: str = Field(description="The status of the order", default="pending")
    items: List[str]


# Define customer schema
class Customer(BaseModel):
    """Details of a customer"""

    customer_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(description="The name of the customer")
    email: Optional[str] = None
    orders: Optional[List[Order]] = None


# Define structured output schema
class ResponseModel(BaseModel):
    """Structured output schema"""

    response: str = Field(description="The response to the user's last message")
    needs_escalation: bool = Field(
        description="Whether the customer needs to be escalated"
    )
    follow_up_required: bool = Field(
        description="Whether the customer needs to be followed up with"
    )
    sentiment: str = Field(description="The sentiment of the customer's last message")


# Agent with structured output and dependencies
agent = Agent(
    model="openai:gpt-4o-mini",
    result_type=ResponseModel,
    deps_type=Customer,
    retries=3,
    system_prompt=(
        "You are an intelligent customer support agent. "
        "Analyze queries carefully and provide structured responses. "
        "Always respond in a friendly and professional manner. "
    ),  # This prompt is the same for every interaction
)


# Add dynamic system prompt based on dependencies
@agent.system_prompt
def add_customer_details(ctx: RunContext[Customer]) -> str:
    # Access the dependency via ctx.deps
    name = ctx.deps.name
    orders = ctx.deps.orders
    return f"You are assisting {name}. They have the following orders: {orders}"


# create an example customer
customer = Customer(
    name="Bob",
    orders=[Order(order_id="123", status="pending", items=["Blue Jeans", "T-Shirt"])],
)

print(customer)
print(customer.orders)

# Run the agent synchronously, passing the dependency instance
result = agent.run_sync(
    "What did I order?",
    deps=customer,  # Pass the dependency instance here
)

print(result.data)
