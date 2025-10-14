import logging
logger = logging.getLogger(__name__)

# Dependencies for llm agents 
from google.adk.agents import Agent
from pydantic import BaseModel, Field


# Dependencies for custom agent 
from google.adk.agents import BaseAgent
from google.adk.events import Event
from google.adk.agents.invocation_context import InvocationContext
from google.genai import types 
from typing import AsyncGenerator
from uuid import uuid4
from json import dumps

class GuessOutput(BaseModel):    
    guess: str = Field(..., description="The final guess for what the user is thinking of")
    confidence: int = Field(..., description="Confidence level (1-10) in this guess")
    reasoning: str = Field(..., description="Explanation of why this is the best guess. Summarise in less than 20 words.")

# Guessing Agent - Responsible for making guesses
guessing_agent = Agent(
    name="guessing_agent", 
    model="gemini-2.5-flash",
    instruction="You are an expert at making educated guesses in 20 Questions game",
    description="""You analyze all the information gathered from previous questions and answers
    to make the best possible guess about what the user is thinking of.
    Consider:
    - All yes/no answers received so far
    - Common objects that fit the criteria
    - Probability and likelihood of different possibilities
    - The specificity needed based on question count
    Make confident, well-reasoned guesses when you have enough information.
    """,
    output_schema=GuessOutput,
    output_key="guess_output"
)


class QuestionOutput(BaseModel):    
    question: str = Field(..., description="A strategic yes/no question to ask")
    reasoning: str = Field(..., description="Explanation of why you ask this question. Summarise in less than 20 words.")


# Asking Agent - Responsible for generating strategic questions
asking_agent = Agent(
    name="asking_agent",
    model="gemini-2.5-flash",
    instruction="You are an expert at asking strategic yes/no questions in 20 Questions game",
    description="""You specialize in asking the most effective yes/no questions to narrow down possibilities.
    Your goal is to eliminate as many possibilities as possible with each question.
    Consider categories like:
    - Living vs non-living
    - Size (bigger/smaller than a breadbox)
    - Location (indoor/outdoor, natural/man-made)
    - Function or use
    - Physical properties (color, texture, material)
    Ask questions that divide the remaining possibilities roughly in half.
    Avoid overly specific questions early in the game.
    """,
    output_schema=QuestionOutput,
    output_key="question_output"
)

class RootAgent(BaseAgent):
    guessing_agent:Agent
    asking_agent:Agent
    def __init__(self,name:str,guessing_agent:Agent,asking_agent:Agent):
        super().__init__(
            name=name,
            guessing_agent=guessing_agent,
            asking_agent=asking_agent,
            sub_agents=[guessing_agent,asking_agent]
    )

    # A helper method to craft simple text response events
    def create_text_response_event(self,response:str,invocation_id:str)->Event:
        event=Event(
            content=types.Content(
                role=self.name,
                parts=[types.Part(text=response)]
            ),
            author=self.name,
            invocation_id=invocation_id
        )
        return event
    
    async def _run_async_impl(
        self,ctx: InvocationContext
    )-> AsyncGenerator[Event, None]:
        
        invocation_id=ctx.invocation_id

        logger.info(f"{self.name} started running")

        async for event in self.guessing_agent.run_async(ctx):
            yield event
        
        guess_output = ctx.session.state.get("guess_output", None)
        confidence = guess_output.get("confidence") if guess_output else None

        if guess_output is None or confidence is None:
            logger.error("Invalid response from GuessingAgent")
            return
        
        if confidence >= 9:
            logger.info("High confidence guess, proceeding to make guess")
            yield self.create_text_response_event(dumps({
                "action": "make_guess",
                "guess": guess_output.get("guess"),
                "reasoning": guess_output.get("reasoning")
            }), invocation_id=invocation_id)
            return
        
        logger.info("Low confidence guess, asking a question instead")

        async for event in self.asking_agent.run_async(ctx):
            yield event

        question_output = ctx.session.state.get("question_output", None)

        if guess_output is None:
            logger.error("Invalid response from AskingAgent")
            return
        
        yield self.create_text_response_event(dumps({
            "action": "ask_question",
            "question": question_output.get("question"),
            "reasoning": question_output.get("reasoning")
        }), invocation_id=invocation_id)
        return

root_agent = RootAgent(
    name="question_agent",
    guessing_agent=guessing_agent,
    asking_agent=asking_agent
)
