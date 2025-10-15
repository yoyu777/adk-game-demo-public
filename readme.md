# A Simple Python Game using ADK

This is a simple game built using Python and the Google ADK framework.

You will play the "20 questions" game with an AI - you think of a word, and the AI tries to read your mind by asking you up to 20 yes/no question.

The architecture of the application:
<img width="960" height="540" alt="Beyond the prompt" src="https://github.com/user-attachments/assets/8daabbbb-4af7-4c79-af76-9e13bcc7613e" />

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

## Get and set up Gemini API Key

This project uses Google's Gemini AI model, which requires an API key for authentication.

### Step 1: Get your API Key from Google AI Studio

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click on "Get API Key" or "Create API Key"
4. Create a new API key for your project
5. Copy the generated API key (it will look like: `AIzaSyA...`)

### Step 2: Create a .env file

In the root directory of the project (same folder as `main.py`), create a file named `.env`:

```bash
touch .env
```

### Step 3: Add your API key to the .env file

Open the `.env` file in a text editor and add your API key:

```env
GOOGLE_API_KEY=your_actual_api_key_here
```

Replace `your_actual_api_key_here` with the API key you copied from Google AI Studio.

### Step 4: Verify the setup

Make sure your `.env` file:
- Is in the root directory of the project
- Contains the correct API key
- Is **NOT** committed to version control (it should be in `.gitignore`)

**Important:** Never share your API key publicly or commit it to version control. The `.env` file should be kept private and secure.

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


## `tkinter`

The tkinter package (“Tk interface”) is the standard Python interface to the Tcl/Tk GUI toolkit. Both Tk and tkinter are available on most Unix platforms, including macOS, as well as on Windows systems.

https://docs.python.org/3/library/tkinter.html
