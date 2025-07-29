from agent import Agent
from agent_tool_service import AgentToolService

task: str = input('Hi there! How can I help you? \nYou>> ')
# message: str = "What's inside my current folder?"

agent: Agent = Agent(AgentToolService())
agent.run(task)