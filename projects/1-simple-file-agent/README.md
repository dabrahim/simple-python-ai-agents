# Simple File Agent

A basic AI agent that can interact with files through function calls.

## Description

This agent uses OpenAI's function calling to perform file operations like listing, reading, writing, and appending to
files. It's designed as a simple command-line interface that processes user requests and executes appropriate file
operations.

## Features

- List files in a directory
- Read file contents
- Write new files
- Append to existing files
- Interactive user clarification
- Command-line interface

## Setup

1. Create and activate a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your `.env` file with:
   ```
   OPENAI_API_KEY=your_key_here
   LLM_MODEL=gpt-4
   MAX_ITERATIONS=10
   ```
4. Run: `python main.py`

## Files

- `main.py` - Main application loop
- `llm.py` - OpenAI client wrapper
- `tools.py` - File operation functions and tool definitions
- `system-prompt.md` - System prompt for the agent
- `requirements.txt` - Python dependencies