# Simple File Agent

A basic AI agent that can interact with files through function calls with conversation memory and follow-up support.

## Description

This agent uses OpenAI's function calling to perform file operations like listing, reading, writing, and appending to files. It's designed as a simple command-line interface that processes user requests, executes appropriate file operations, and supports follow-up conversations.

## Features

- List files in a directory
- Read file contents
- Write new files
- Append to existing files
- Interactive user clarification
- Follow-up conversation support
- Memory system (in development)
- Command-line interface

## Setup

1. Create and activate a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your `.env` file with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   OPEN_AI_MODEL_NAME=gpt-4.1
   MAX_ITERATIONS=10
   MEMORY_FOLDER=.memory
   CHAT_HISTORY_FILE=chat-history.json
   ```
4. Run: `python run.py`

## Project Structure

- `run.py` - Main entry point that starts the agent
- `agent.py` - Core Agent class containing the conversation loop
- `llm.py` - OpenAI client wrapper and completion handling
- `tools.py` - File operation functions and tool definitions
- `memory.py` - Memory management system (in development)
- `system-prompt.md` - System prompt for the agent
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template

## How It Works

1. **Start**: Run `python run.py` and enter your request
2. **Processing**: The agent analyzes your request using OpenAI's function calling
3. **Tool Execution**: Performs the appropriate file operations
4. **Response**: Provides results and asks if you need further help
5. **Follow-up**: Continue the conversation or exit

The agent uses a structured approach with proper error handling and supports iterative conversations where you can ask follow-up questions.