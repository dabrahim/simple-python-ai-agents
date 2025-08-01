from src.core.agent import Agent
from src.services.agent_tool_service import AgentToolService

task: str = input('Hi there! How can I help you? \nYou>> ')
# message: str = "What's inside my current folder?"

agent: Agent = Agent(AgentToolService())
agent.run(task)