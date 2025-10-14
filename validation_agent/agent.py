from pydantic import BaseModel, Field

from google.adk.agents import LlmAgent


class ValidationOutput(BaseModel):
    is_valid: bool = Field(..., description="Indicates if the input is a valid object for the game.")
    reason: str = Field(..., description="Explanation of why the input is valid or not.")

root_agent = LlmAgent(
    name="validation_agent",
    model="gemini-2.5-flash", # Or your preferred Gemini model
    instruction="You are incharge of validate user's initial input",
    description="""The user is going to play a game of 20 Questions.
    Before starting the game, you need to validate the user's input to ensure it is a valid object for the game.
    A valid object should be a noun like the name of an object, an animal, or a concept, and not too obscure.
    For example, "cat", "car", "apple" are valid, but "quantum entanglement" or "the number seven" are not.
    """,
    output_schema=ValidationOutput
)