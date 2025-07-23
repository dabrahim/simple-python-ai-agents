# Simple Python AI Agents

A simple mono repo for learning Python and experimenting with LLM-based technologies. Each project is standalone and self-contained.

## Purpose

This repo is designed for:
- **Learning Python fundamentals** through hands-on AI projects
- **Experimenting with LLMs** (OpenAI, Anthropic, etc.)
- **Building simple AI agents** without complex frameworks (for now)
- **Rapid prototyping** of AI ideas

I'll add more projects as I learn new things :)

## Structure

```
projects/
├── 1-project-a/
└── 2-project-b/
```

Each project has its own:
- Virtual environment (`venv/`)
- Dependencies (`requirements.txt`)
- Environment variables (`.env`)
- Documentation (`README.md`)

## Quick Start

### Trying out existing projects (e.g : 1-simple-file-agent)
```bash
cd projects/1-simple-file-agent
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python main.py
```

### Adding new projects
```bash
# Create project folder
mkdir projects/my-new-agent
cd projects/my-new-agent

# Set up virtual environment
python -m venv venv
source venv/bin/activate

# Create basic files
touch main.py requirements.txt .env.example README.md

# Start coding!
```