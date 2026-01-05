import sympy
from langchain.agents import create_agent


def calculate(expression: str) -> str:
    """Calculate a mathematical expression.
    Args:
        expression (str): Python arithmetic expression to calculate.
    Returns:
        str: The result of the calculation.
    """
    try:
        result = sympy.sympify(expression).evalf()
        return str(result)
    except Exception as e:
        return f"Error calculating expression: {e}"


# create the agent by combining the model and the function
agent = create_agent(
    model="claude-haiku-4-5",
    tools=[calculate],
    system_prompt="You are a helpful maths assistant. Use your calculator to help with maths problems.",
)
