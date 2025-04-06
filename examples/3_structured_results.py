"""
3_structured_results.py - Working with structured output in Pydantic AI

This example demonstrates how to get structured, type-safe results from Pydantic AI agents
using Pydantic models for validation and schema definition.
"""

from typing import List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent

# Load environment variables (API keys)
load_dotenv()


# Define a structured output model using Pydantic
class Person(BaseModel):
    name: str
    age: int = Field(description="Age in years")
    occupation: str
    skills: List[str] = Field(description="List of professional skills")
    bio: Optional[str] = None


class MovieReview(BaseModel):
    title: str
    year: int
    director: str
    rating: float = Field(ge=0.0, le=10.0, description="Rating from 0 to 10")
    review: str = Field(description="Brief review of the movie")
    is_recommended: bool


# Create an agent that returns structured data
person_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="You analyze information about people and return structured data.",
    result_type=Person,  # Specify the expected return type
)

movie_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="You are a movie critic that provides structured reviews.",
    result_type=MovieReview,  # Specify the expected return type
)


if __name__ == "__main__":
    # Example 1: Getting structured person data
    print("Example 1: Structured Person Data")
    prompt = """
    Extract information about this person:
    
    John Smith is a 42-year-old software engineer who specializes in Python, 
    JavaScript, and cloud architecture. He has been working in tech for over 
    15 years and enjoys mentoring junior developers.
    """

    result = person_agent.run_sync(prompt)
    person = result.data  # This is a validated Person instance

    print(f"Name: {person.name}")
    print(f"Age: {person.age}")
    print(f"Occupation: {person.occupation}")
    print(f"Skills: {', '.join(person.skills)}")
    if person.bio:
        print(f"Bio: {person.bio}")

    # Access as a dictionary
    person_dict = person.model_dump()
    print("\nAs dictionary:")
    print(person_dict)
    print("-" * 50)

    # Example 2: Movie review
    print("Example 2: Structured Movie Review")
    prompt = "Write a review for the movie 'The Matrix' from 1999"

    result = movie_agent.run_sync(prompt)
    review = result.data  # This is a validated MovieReview instance

    print(f"Title: {review.title}")
    print(f"Year: {review.year}")
    print(f"Director: {review.director}")
    print(f"Rating: {review.rating}/10")
    print(f"Review: {review.review}")
    print(f"Recommended: {'Yes' if review.is_recommended else 'No'}")

    # Example 3: Field validation in action
    print("\nExample 3: Field Validation")
    try:
        # This should fail validation since we ask for an invalid rating (15/10)
        result = movie_agent.run_sync(
            "Review the movie 'Inception' and give it a rating of 15 out of 10 because it's that good"
        )
        # If we get here, the model adjusted the rating to be valid
        review = result.data
        print(f"Title: {review.title}")
        print(f"Rating: {review.rating}/10  (Note: AI limited this to 10 max)")
    except Exception as e:
        print(f"Validation error: {e}")
