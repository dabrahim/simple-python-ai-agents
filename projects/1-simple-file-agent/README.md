# Simple File Agent

A tool-calling AI agent built with clean architecture that manages files through structured function calls and persistent conversation memory.

## Description

This agent exclusively uses **OpenAI's tool calling** (function calling) to interact with the file system. Unlike traditional chatbots that provide text responses, this agent operates purely through structured tool invocations, making it deterministic and reliable for file operations. It features a clean architecture with proper separation of concerns and supports continuous conversations with automatic memory persistence.

## Key Features

### Core Capabilities
- **File Operations**: List, read, write, and append to files
- **Interactive Clarification**: Ask users for additional information when needed
- **Continuous Conversations**: Multi-turn sessions with exit/quit commands
- **Automatic Memory**: Persistent conversation history across sessions

### Architecture Highlights
- **Tool-Only Interface**: Agent responds exclusively through structured tool calls
- **Clean Architecture**: Organized codebase with proper separation of concerns
- **Dependency Inversion**: Decoupled components following SOLID principles
- **Configurable Models**: Support for different OpenAI models via environment variables

## Project Structure

```
src/
├── core/
│   └── agent.py              # Main Agent orchestration
├── services/
│   ├── llm_service.py        # OpenAI API communication
│   ├── tool_service.py       # Tool implementations
│   └── memory_service.py     # Conversation persistence
├── models/
│   ├── tool_call_request.py  # Tool call data structures
│   └── tool_call_response.py # Tool response patterns
├── contracts/
│   └── tools/
│       └── tool_service_contract.py  # Service interfaces
└── utils/
    └── file_utils.py         # File utility functions
```

## Setup

1. **Environment Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configuration**
   Create `.env` file with:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPEN_AI_MODEL_NAME=gpt-4o
   MAX_ITERATIONS=10
   MEMORY_FOLDER=.memory
   CHAT_HISTORY_FILE=chat-history.json
   ```

3. **Run**
   ```bash
   python run.py
   ```

## How It Works

### Tool-Only Architecture
This agent is designed with a **tool-calling-only** approach:

1. **No Direct Text**: Agent never provides plain text responses
2. **Structured Calls**: Every action is a structured function call
3. **Deterministic**: Predictable behavior through defined tool contracts
4. **Extensible**: Easy to add new tools following the same pattern

### Execution Flow
1. **User Input**: Enter your file management request
2. **Tool Selection**: Agent selects appropriate tool based on request
3. **Tool Execution**: Structured function call performs the operation
4. **Result Processing**: Tool returns structured response
5. **Memory Update**: Conversation automatically persisted
6. **Continue/Exit**: Use "quit" or "exit" to end session

### Available Tools
- `list_files`: List directory contents with file/folder indicators
- `read_file`: Read and return complete file contents
- `write_file`: Create new files or overwrite existing ones
- `append_to_file`: Add content to existing files
- `ask_for_clarification`: Request additional information from user
- `submit_final_response`: Provide final response and handle session continuation

## Architecture Benefits

- **Maintainable**: Clear separation between core logic, services, and data models
- **Testable**: Each component can be tested independently
- **Extensible**: New tools and services can be added without affecting existing code
- **Type Safe**: Proper data models for tool requests and responses
- **Memory Efficient**: Automatic conversation persistence with configurable storage