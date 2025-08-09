import os
from src.core.agent import Agent
from src.services.tool_service import AgentToolService
from src.services.console_logger_service import ConsoleLoggerService

model: str | None = os.getenv('OPEN_AI_MODEL_NAME')

if model is None:
    raise ValueError('No model provided in the environment')

logger = ConsoleLoggerService()
agent: Agent = Agent(tool_service=AgentToolService(logger=logger), model=model, logger=logger)

print("🤖 AI File Agent - Ready to help with your files and folders!")
print("   Type 'quit' or 'exit' to end the session\n")

task: str = input("How can I help you? \n👤 You: ").strip()

while task not in ('exit', 'quit'):
    agent.run(task)
    print()  # Add spacing between interactions
    task = input('👤 You: ').strip()