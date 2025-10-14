import logging

# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()

import json

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from google.genai import types 
# For creating message Content/Parts
# This is installed with ADK doesn't need to install separaterly

from validation_agent.agent import root_agent as validation_agent
from question_agents.agent import root_agent as question_agent

from uuid import uuid4
USER_ID = str(uuid4())


class ADKRunners:
    def __init__(self):
        return

    async def initialise_validation_agent(self):
        session_service = InMemorySessionService()
        app_name="ValidationAgent"
        self.validation_agent_session=await session_service.create_session(
            app_name=app_name, 
            user_id=USER_ID
        )
        self.validation_agent_runner=Runner(
            agent=validation_agent,
            session_service=session_service,
            app_name=app_name
        )
        logger.info("Validation agent initialized")
        return
    
    async def validate_input(self,user_input="elephant"):
        try:
            async for event in self.validation_agent_runner.run_async(
                user_id=USER_ID,
                session_id=self.validation_agent_session.id,
                new_message=types.Content(role='user', parts=[types.Part(text=user_input)])
            ):
                if(event.is_final_response()):
                    logger.debug(event.content.parts[0].text)
                    return json.loads(event.content.parts[0].text)
                else:
                    pass
        except Exception as e:
            logger.error(f"Error during validation: {e}")
            return None
        
    async def initialise_question_agent(self):
        session_service = InMemorySessionService()
        app_name="QuestionAgent"
        self.question_agent_session=await session_service.create_session(
            app_name=app_name, 
            user_id=USER_ID
        )
        self.question_agent_runner=Runner(
            agent=question_agent,
            session_service=session_service,
            app_name=app_name
        )
        logger.info("Question agent initialized")
        return


    async def guess_or_ask(self, game_context="Starting a new game of 20 questions"):
        try:
            async for event in self.question_agent_runner.run_async(
                user_id=USER_ID,
                session_id=self.question_agent_session.id,
                new_message=self.query_to_content(game_context)
            ):
                try:
                    # is_final_response() is only used by ADK
                    # so we need to determine if this is the final response ourselves
                    response=json.loads(event.content.parts[0].text)
                    if("action" in response):
                        logger.info(f"Response: {response}")
                        return response
                except Exception as e:
                    logger.error(f"Error parsing JSON response: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error during guess_or_ask: {e}")
            return None

    def query_to_content(self,query):
        return types.Content(role='user', parts=[types.Part(text=query)])
