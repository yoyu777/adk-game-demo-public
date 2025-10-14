# A Simple Python Game using ADK

This is a simple game built using Python and the Google ADK framework.

## Setup and Installation

After cloning the project, it is highly recommended to set up a virtual environment to manage project dependencies and avoid conflicts with other Python packages.

### Set up a virtual environment (using venv)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
.\venv\Scripts\activate
```

### Install dependencies from requirements.txt

Once the virtual environment is activated, install the required packages:
```bash
pip install -r requirements.txt
```

### Deactivate (when finished)

To exit the virtual environment when you are done working on the project, run:
```bash
deactivate
```

## Run the Game

With your environment activated and dependencies installed, you can start the game by executing the main file:
```bash
python main.py
```

## Test and Debug Agents using ADK

The Google ADK includes specialized logging and debugging tools for agents.

### Test the Agent in the Browser (ADK Sandbox)

If your ADK setup includes a web-based sandbox or UI (common for conversational agents), you can test the agent interactively:

**Start the ADK Web Server:**
```bash
adk web
```

**Access the Interface:** Open your browser and navigate to the local server address (usually http://localhost:8000).

**Interact:** Use the provided interface to send queries to the agent. This view often provides real-time insights into the agent's internal state and decision-making process.

### Test the Agent in the Command Line

For quick, non-UI-based testing or integration checks, you can use the ADK's command line runner:

**Run with Agent Query:**
```bash
adk run [agent_name]
```

This bypasses the game interface and sends queries directly to the integrated ADK agent for a direct response.

### Enable Debugging and Tracing

To get detailed, step-by-step logs of the agent's execution, including which tools it selected and the raw LLM calls, set the `ADK_LOG_LEVEL` environment variable:

**On macOS/Linux:**
```bash
ADK_LOG_LEVEL=DEBUG python main.py
```

**On Windows (Command Prompt):**
```cmd
set ADK_LOG_LEVEL=DEBUG
python main.py
```

This is essential for troubleshooting issues like prompt failures, unexpected tool usage, or incorrect context retrieval.