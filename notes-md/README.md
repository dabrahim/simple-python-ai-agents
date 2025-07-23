# Python AI Agents Mono Repo

A simple mono repository structure for hosting multiple standalone Python AI agent projects. Each project is self-contained with its own dependencies and can be developed independently.

## Repository Structure

```
simple-python-ai-agents/
├── README.md                    # This file
├── projects/                    # All projects go here
│   └── 1-simple-file-agent/    # Example project
│       ├── main.py
│       ├── llm.py
│       ├── tools.py
│       ├── requirements.txt
│       ├── .env.example
│       └── README.md
└── scripts/                     # Optional: shared utility scripts
```

## Getting Started

### Prerequisites
- Python 3.8+ installed on your system
- Basic understanding of virtual environments
- Your favorite IDE/editor (VS Code recommended)

### Setting Up Your Development Environment

#### 1. Clone and Navigate
```bash
git clone <your-repo-url>
cd simple-python-ai-agents
```

#### 2. Python Virtual Environment Management

**Why Virtual Environments?**
Virtual environments isolate your project dependencies, preventing conflicts between different projects. Each project in this mono repo will have its own virtual environment.

**For each project, you'll create a separate virtual environment:**

```bash
# Navigate to your project
cd projects/1-simple-file-agent

# Create virtual environment
python -m venv venv

# Activate it (Linux/Mac)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Important Notes:**
- Always activate the virtual environment before working on a project
- Your terminal prompt will show `(venv)` when activated
- Use `deactivate` to exit the virtual environment
- Never commit the `venv/` folder to git (it's in .gitignore)

## Creating a New Project

### Step-by-Step Process

#### 1. Create Project Directory
```bash
# From the repo root
mkdir projects/your-new-project-name
cd projects/your-new-project-name
```

#### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

#### 3. Create Basic Project Structure
```bash
# Create essential files
touch main.py
touch requirements.txt
touch README.md
touch .env.example
```

#### 4. Install Initial Dependencies
```bash
# Install common dependencies (optional)
pip install python-dotenv

# Save to requirements.txt
pip freeze > requirements.txt
```

#### 5. Create Basic Project Files

**main.py** - Your main application entry point:
```python
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    print("Hello from your new project!")

if __name__ == "__main__":
    main()
```

**README.md** - Project documentation:
```markdown
# Your Project Name

## Description
Brief description of what this project does.

## Setup
1. Create and activate virtual environment: `python -m venv venv && source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and configure
4. Run: `python main.py`

## Dependencies
List your main dependencies here.
```

**.env.example** - Environment variables template:
```
# Add your environment variables here
API_KEY=your_api_key_here
DEBUG=True
```

## Dependency Management

### Understanding requirements.txt
The `requirements.txt` file lists all Python packages your project needs. It's created using:

```bash
# After installing packages
pip freeze > requirements.txt
```

### Best Practices
1. **Always use virtual environments** - Never install packages globally
2. **Pin versions** - Use `==` for exact versions in production
3. **Separate dev dependencies** - Consider `requirements-dev.txt` for development tools
4. **Update regularly** - Keep dependencies current for security

### Example requirements.txt structure:
```
# Core dependencies
requests==2.31.0
python-dotenv==1.0.0

# AI/ML dependencies
openai==1.97.0
langchain==0.1.0

# Development dependencies (optional)
pytest==7.4.0
black==23.0.0
```

## Working with Multiple Projects

### Daily Workflow
1. **Navigate to project**: `cd projects/your-project`
2. **Activate environment**: `source venv/bin/activate`
3. **Start coding**: Work on your project files
4. **Install new packages**: `pip install package-name`
5. **Update requirements**: `pip freeze > requirements.txt`
6. **Deactivate when done**: `deactivate`

### Switching Between Projects
```bash
# Working on project A
cd projects/project-a
source venv/bin/activate
python main.py
deactivate

# Switch to project B
cd ../project-b
source venv/bin/activate
python main.py
deactivate
```

## IDE Setup (PyCharm Guide)

### PyCharm Configuration (Recommended for this setup)

PyCharm handles mono repos with multiple Python projects exceptionally well. Here's how to set it up:

#### 1. Opening the Mono Repo
1. **Open PyCharm**
2. **File → Open** and select your `simple-python-ai-agents` folder
3. **Choose "This Window"** when asked
4. PyCharm will recognize this as a multi-project setup

#### 2. Setting Up Python Interpreters for Each Project

**For your first project (1-simple-file-agent):**
1. **Go to File → Settings** (Ctrl+Alt+S on Windows/Linux, Cmd+, on Mac)
2. **Navigate to Project → Python Interpreter**
3. **Click the gear icon → Add...**
4. **Select "Virtualenv Environment" → "New Environment"**
5. **Set Location to**: `projects/1-simple-file-agent/venv`
6. **Base interpreter**: Your system Python (usually auto-detected)
7. **Click OK**

**For future projects:**
- Repeat the above steps for each new project
- Each project gets its own interpreter pointing to its own `venv` folder

#### 3. Project Structure Setup
1. **Right-click on `projects` folder** in Project view
2. **Select "Mark Directory as → Sources Root"**
3. This helps PyCharm understand your project structure

#### 4. Run Configurations
**Setting up run configuration for 1-simple-file-agent:**
1. **Run → Edit Configurations**
2. **Click + → Python**
3. **Name**: "Simple File Agent"
4. **Script path**: `projects/1-simple-file-agent/main.py`
5. **Python interpreter**: Select the venv you created for this project
6. **Working directory**: `projects/1-simple-file-agent`
7. **Click OK**

**For future projects:**
- Create similar run configurations for each project
- Always set the working directory to the project folder
- Use the project-specific interpreter

#### 5. Terminal Setup
PyCharm's terminal will automatically activate the correct virtual environment when you:
1. **Open terminal** (Alt+F12 or View → Tool Windows → Terminal)
2. **Navigate to your project folder**: `cd projects/1-simple-file-agent`
3. PyCharm will automatically activate the venv for that project

#### 6. Code Quality Tools
**Enable for each project:**
1. **File → Settings → Tools → Python Integrated Tools**
2. **Set Default test runner** to pytest (if you plan to use it)
3. **Tools → Python Integrated Tools → Docstring format** to your preference

**Enable inspections:**
1. **File → Settings → Editor → Inspections**
2. **Enable Python inspections** (most are enabled by default)
3. **Consider enabling**:
   - PEP 8 coding style violation
   - Unused local variable
   - Unreachable code

#### 7. Working with Multiple Projects Daily

**Switching between projects:**
1. **Use the Project view** to navigate between project folders
2. **Terminal automatically switches** environments when you cd to different projects
3. **Run configurations** are project-specific
4. **Each project maintains its own interpreter and dependencies**

**Best practices:**
- **Keep PyCharm open** at the repo root level
- **Use separate terminal tabs** for different projects if working simultaneously
- **Create bookmarks** for frequently accessed files (Ctrl+F11)

#### 8. Adding New Projects in PyCharm

When you create a new project following the README steps:
1. **Create the project folder structure** as described in the README
2. **In PyCharm, right-click the new project folder**
3. **Select "Add as Content Root"** if it doesn't appear automatically
4. **Set up a new interpreter** following step 2 above
5. **Create a run configuration** following step 4 above

#### 9. Environment Variables in PyCharm
1. **Run → Edit Configurations**
2. **Select your run configuration**
3. **Environment variables → Add**
4. **Or use .env files** (PyCharm supports python-dotenv automatically)

#### 10. Debugging Setup
1. **Set breakpoints** by clicking in the gutter next to line numbers
2. **Run in debug mode** using the debug button or Shift+F9
3. **Each project debugs independently** with its own interpreter

### Alternative IDEs

#### VS Code Configuration
If you prefer VS Code, the `.vscode/settings.json` file is already configured for you.

1. **Install Python extension** by Microsoft
2. **Open the repo root** in VS Code
3. **Select interpreter** for each project: Ctrl+Shift+P → "Python: Select Interpreter"
4. **Choose the venv** from each project's folder

#### Other IDEs
- **Vim/Neovim**: Use `python-mode` or `coc-python`
- **Sublime Text**: Install `Anaconda` package
- **Atom**: Install `ide-python` package

## Common Patterns and Best Practices

### Environment Variables
Always use `.env` files for configuration:
```python
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
```

### Project Organization
```
your-project/
├── main.py              # Entry point
├── config.py            # Configuration
├── utils/               # Utility functions
│   ├── __init__.py
│   └── helpers.py
├── models/              # Data models
│   ├── __init__.py
│   └── user.py
├── tests/               # Unit tests
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt     # Dependencies
├── .env.example        # Environment template
└── README.md           # Documentation
```

### Error Handling
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Your code here
    pass
except Exception as e:
    logger.error(f"Error occurred: {e}")
    raise
```

## Troubleshooting

### Common Issues

#### "Module not found" errors
- **Cause**: Virtual environment not activated or dependency not installed
- **Solution**: Activate venv and install missing packages

#### "Permission denied" errors
- **Cause**: Trying to install packages globally
- **Solution**: Activate virtual environment first

#### Virtual environment not working
- **Cause**: Python not in PATH or venv corrupted
- **Solution**: Recreate virtual environment

```bash
# Delete old venv
rm -rf venv

# Create new one
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### IDE not recognizing dependencies
- **Cause**: Wrong Python interpreter selected
- **Solution**: Select interpreter from project's venv folder

### Debugging Tips
1. **Check Python version**: `python --version`
2. **Check active environment**: `which python`
3. **List installed packages**: `pip list`
4. **Check environment variables**: `printenv` (Linux/Mac) or `set` (Windows)

## Git Best Practices

### .gitignore
Your `.gitignore` should include:

```gitignore
# Virtual environments
venv/
env/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Environment variables
.env

# IDE
.vscode/
../.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

### Commit Structure
```
feat(project-name): add new feature
fix(project-name): fix bug in module
docs(project-name): update README
refactor(project-name): restructure code
```

## Adding Shared Utilities (Optional)

If you need shared code across projects:

1. Create `shared/` directory at repo root
2. Create utilities there
3. Install in editable mode in each project:
```bash
cd projects/your-project
source venv/bin/activate
pip install -e ../../shared
```

## Getting Help

### Resources
- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
- [pip Documentation](https://pip.pypa.io/en/stable/)
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)

### Next Steps
1. Create your first project following the guide above
2. Set up your IDE with the configurations provided
3. Start coding!
4. When you need a new project, repeat the "Creating a New Project" steps

Remember: Each project is completely independent. You can use different Python versions, different dependencies, and different coding styles in each project. The mono repo structure just keeps everything organized in one place.