from agent import Agent
from tools import tools_definition

task: str = input('Hi there! How can I help you? \nYou>> ')
# message: str = "What's inside my current folder?"

agent: Agent = Agent(tools_definition)
agent.run(task)