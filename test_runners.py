
import asyncio
import json

from adk_runners import ADKRunners

async def test_agents():
    runners = ADKRunners()

    # Test validation agent
    print("=== Testing Validation Agent ===")
    await runners.initialise_validation_agent()
    validation_result = await runners.validate_input("elephant")
    print(f"Validation result: {json.dumps(validation_result, indent=2)}")
    
    # Test question agent
    print("\n=== Testing Question Agent ===")
    await runners.initialise_question_agent()
    
    # Test initial question
    question_result = await runners.guess_or_ask("Starting a new game of 20 questions.")
    print(f"Initial question result: {json.dumps(question_result, indent=2)}")
    
    # Test follow-up with a "yes" answer
    if question_result:
        followup_result = await runners.guess_or_ask("yes")
        print(f"Follow-up result after 'yes': {json.dumps(followup_result, indent=2)}")
        
        # Test follow-up with a "no" answer
        followup_result2 = await runners.guess_or_ask("no")
        print(f"Follow-up result after 'no': {json.dumps(followup_result2, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_agents())