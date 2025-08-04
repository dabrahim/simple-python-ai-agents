import os
from src.core.agent import Agent
from src.services.tool_service import AgentToolService

model: str | None = os.getenv('OPEN_AI_MODEL_NAME')

if model is None:
    raise ValueError('No model provided in the environment')

agent: Agent = Agent(tool_service=AgentToolService(), model=model)
task: str = input("Hi there! How can I help you? \nYou>> ")

while task not in ('exit', 'quit'):
    agent.run(task)
    task = input('[ "quit" to exit ]>>> ').strip()