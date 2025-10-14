import logging
logger = logging.getLogger(__name__)

import asyncio

from typing import Optional
from adk_runners import ADKRunners

from ui_components import GameUI

class GameController:
    # Handles game logic and interactions between UI and ADK runners
    
    def __init__(self):
        self.user_input = ""
        self.runners = ADKRunners()
        self.current_ai_response: Optional[dict] = None
        self.current_question = 1
        
        # Create UI with callback references
        self.ui = GameUI(
            on_start_game_callback=self.on_start_game,
            on_yes_callback=lambda: asyncio.run(self.on_yes_click()),
            on_no_callback=lambda: asyncio.run(self.on_no_click()),
            on_start_over_callback=self.start_over
        )
        
        # Start the application with the start screen
        self.ui.create_start_screen()
    
    def on_start_game(self):
        #  Handle start game button click
        user_text = self.ui.get_user_input()

        if not user_text:
            self.ui.show_feedback_message("Please enter something!", "red")
            return
        
        logger.info(f"Start Game button pressed with input: {user_text}")

        # Run async validation using AI
        asyncio.run(self.validate_and_start_game(user_text))
    
    async def validate_and_start_game(self, user_text: str):
        # Validate input withing AI and start game
        
        try:
            # Initialise the validation agent
            await self.runners.initialise_validation_agent()

            # Validate input using game.py validate_input method
            validation_result = await self.runners.validate_input(user_text)

            if validation_result is None:
                # Handle validation error
                logger.error("Validation failed due to error")
                self.ui.show_feedback_message("Validation service unavailable. Please try again.", "red")
                return
            
            # Check validation result
            if validation_result.get("is_valid", True):

                # Input is valid, proceed to game
                self.user_input = user_text
                logger.info(f"Input validated successfully: {self.user_input}")
                
                 # Reset feedback message
                self.ui.show_feedback_message(
                    "Enter the name of an object, animal, or concept you want me to guess.",
                    "gray"
                )
                
                # Switch to game screen
                await self.create_game_screen()

            else:
                # Show rejection reason
                rejection_reason = validation_result.get("reason", "Invalid input")
                logger.info(f"Input validation failed: {rejection_reason}")
                self.ui.show_feedback_message(rejection_reason, "red")
                
        except Exception as e:
            logger.error(f"Error during validation: {e}")
            self.ui.show_feedback_message("Error during validation. Please try again.", "red")
    
    async def create_game_screen(self):
        # Create the main game screen and get initial AI response
        await self.runners.initialise_question_agent()

        # Get AI-generated question or guess
        # Do not include the user input in the prompt
        self.current_ai_response = await self.runners.guess_or_ask(
            "Starting a new game of 20 questions. "
        )
        
        # Format the AI response for display
        question_text = self.format_ai_response_text()
        show_buttons = True
        
        # Create the game screen
        self.ui.create_game_screen(question_text, show_buttons)
        self.ui.update_question_counter(self.current_question)
        
        # Display AI reasoning
        reasoning = self.get_ai_reasoning()
        self.ui.update_reasoning_text(reasoning)

    def format_ai_response_text(self) -> str:
        # Format the AI response into display text for the UI
        if self.current_ai_response and self.current_ai_response.get('action') == 'ask_question':
            return f"My question is: {self.current_ai_response.get('question', 'Are you thinking of something alive?')}"
        elif self.current_ai_response and self.current_ai_response.get('action') == 'make_guess':
            return f"Is it: {self.current_ai_response.get('guess', 'something')}?"
        else:
            return "My question is: Are you thinking of something alive?"
    
    def get_ai_reasoning(self) -> str:
        # Extract reasoning from the current AI response
        if self.current_ai_response and 'reasoning' in self.current_ai_response:
            return self.current_ai_response.get('reasoning', '')
        return ""

    async def on_yes_click(self):
        # Handle yes button click
        logger.info(f"User answered 'Yes' to question {self.current_question}")

        await self.process_answer("yes")
    
    async def on_no_click(self):
        # Handle no button click
        logger.info(f"User answered 'No' to question {self.current_question}")

        await self.process_answer("no")
    
    async def process_answer(self, answer: str):
        # Process the user's answer and get next AI response
        # If it was a guess and user said "Yes", AI wins
        if (self.current_ai_response and 
            self.current_ai_response.get('action') == 'make_guess' and 
            answer.lower() == 'yes'):
            await self.show_game_over_screen("I guessed it! 🎉 AI wins!")
            return
        
        # Check if game is over (20 questions reached)
        if self.current_question >= 20:
            await self.show_game_over_screen("You win! I couldn't guess it in 20 questions.")
            return
        
        # Move to next question
        self.current_question += 1
        self.ui.update_question_counter(self.current_question)
        
        # Send the answer to AI and get next response
        self.current_ai_response = await self.runners.guess_or_ask(answer)
        
        # Format and update the question text
        new_text = self.format_ai_response_text()
        self.ui.update_question_text(new_text)
        
        # Update reasoning display
        reasoning = self.get_ai_reasoning()
        self.ui.update_reasoning_text(reasoning)
        
        logger.info(f"Moving to question {self.current_question}")
    
    async def show_game_over_screen(self, message: str):
        # Show game over message
        self.ui.update_question_text(message)
        self.ui.update_reasoning_text("")  # Clear reasoning text
        logger.info(f"Game over: {message}")
    
    def start_over(self):
        # Handle start over button click
        logger.info("Starting over - returning to start screen")
        self.user_input = ""
        self.current_question = 1
        self.current_ai_response = None
        self.ui.create_start_screen()
    
    def run(self):
        # Start the application
        logger.info("Starting 20 Questions Game")
        self.ui.run()