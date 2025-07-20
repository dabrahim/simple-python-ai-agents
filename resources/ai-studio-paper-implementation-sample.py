import json
import datetime


# --- HELPER / MOCK LLM ---
# This class simulates an LLM to make the code runnable without an API key.
# It follows a script for a specific task to demonstrate the agent's reasoning flow.
class MockLLM:
    def __init__(self):
        self.call_count = 0
        # A pre-programmed script of responses for our specific scenario
        self.responses = [
            # 1. First thought: Decompose the problem.
            json.dumps({
                "thought": "The user wants to know the weather and what to wear in the capital of France. I need to first find the capital of France, then get the weather for that city, and finally reason about what to wear. My first step is to find the capital of France using the web search tool.",
                "action": {
                    "tool_name": "search_web",
                    "tool_input": "capital of France"
                }
            }),
            # 2. Second thought: Use the information found.
            json.dumps({
                "thought": "The search result says the capital of France is Paris. Now I need to get the weather in Paris. I will use the get_current_weather tool.",
                "action": {
                    "tool_name": "get_current_weather",
                    "tool_input": "Paris"
                }
            }),
            # 3. Third thought: Synthesize the final answer.
            json.dumps({
                "thought": "The weather in Paris is 15°C and cloudy. This is cool weather. I should recommend wearing layers, like a sweater and a light jacket. I now have all the information needed to answer the user's question.",
                "action": {
                    "tool_name": "respond_to_user",
                    "tool_input": "The weather in Paris, the capital of France, is currently 15°C and cloudy. I would recommend wearing a sweater and a light jacket."
                }
            })
        ]

    def call(self, prompt: str) -> str:
        """Simulates calling an LLM API."""
        print("--- LLM PROMPT ---")
        print(prompt)
        print("--------------------")
        if self.call_count < len(self.responses):
            response = self.responses[self.call_count]
            self.call_count += 1
            return response
        return json.dumps({
            "thought": "I seem to be stuck in a loop. I should ask the user for clarification.",
            "action": {"tool_name": "ask_clarifying_question",
                       "tool_input": "I'm having trouble proceeding. Can you please clarify your request?"}
        })


# ==============================================================================
# §3.3 ACTION MODULE: Handles tool use and interaction with the environment
# ==============================================================================
class ActionModule:
    """
    Executes actions decided by the Brain. This module acts as the agent's 'hands'.
    It translates the brain's desired action into a real function call.
    This directly implements the concepts of Tool Using (§3.3.2) and Embodied Action (§3.3.3).
    """

    def __init__(self, memory_module):
        # Tools are registered here. The agent can only use tools that are in this dictionary.
        self._tools = {
            "search_web": self._search_web,
            "get_current_weather": self._get_current_weather,
            "summarize_memory": self._summarize_memory,
            "respond_to_user": self._respond_to_user,
            "ask_clarifying_question": self._ask_clarifying_question
        }
        self.memory_module = memory_module  # Give tools access to memory

    def execute(self, tool_name: str, tool_input: str) -> str:
        """Executes a given tool with the provided input."""
        if tool_name not in self._tools:
            return f"Error: Tool '{tool_name}' not found."
        try:
            # Call the corresponding private method
            return self._tools[tool_name](tool_input)
        except Exception as e:
            return f"Error executing tool '{tool_name}': {e}"

    # --- Tool Implementations ---
    def _search_web(self, query: str) -> str:
        """A mock tool to search the web."""
        print(f"ACTION: Searching web for '{query}'...")
        if "capital of france" in query.lower():
            return "The capital of France is Paris."
        return "Sorry, I can't find information on that."

    def _get_current_weather(self, city: str) -> str:
        """A mock tool to get the weather."""
        print(f"ACTION: Getting weather for '{city}'...")
        if city.lower() == "paris":
            return "The weather in Paris is 15°C and cloudy."
        return f"Sorry, I don't have weather information for {city}."

    def _summarize_memory(self, _: str) -> str:
        """A tool for the agent to manage its own memory, as per §3.1.3."""
        print("ACTION: Summarizing agent memory...")
        summary = self.memory_module.summarize()
        return f"Memory has been summarized. New summary: {summary}"

    def _respond_to_user(self, response_text: str) -> str:
        """
        A special tool to give the final response to the user.
        This enforces the constraint that all LLM outputs are function calls.
        """
        print(f"ACTION: Responding to user -> '{response_text}'")
        # This return value signals the agent loop to stop.
        return f"FINAL_RESPONSE:{response_text}"

    def _ask_clarifying_question(self, question_text: str) -> str:
        """A special tool to ask the user for help when stuck."""
        print(f"ACTION: Asking user for clarification -> '{question_text}'")
        return f"CLARIFICATION:{question_text}"


# ==============================================================================
# §3.2 PERCEPTION MODULE: Senses the environment
# ==============================================================================
class PerceptionModule:
    """
    Processes inputs from the environment (user, tools) and formats them
    into a standardized 'Observation' string for the Brain to process.
    This models the expansion of the agent's perception from just text to multimodal sources.
    """

    def perceive_user_input(self, user_input: str) -> str:
        return f"Observation: The user has tasked me with the following: '{user_input}'"

    def perceive_tool_output(self, tool_name: str, tool_output: str) -> str:
        return f"Observation: The tool '{tool_name}' returned the following output: '{tool_output}'"


# ==============================================================================
# §3.1.3 MEMORY MODULE
# ==============================================================================
class MemoryModule:
    """
    Stores the agent's history of observations and actions.
    This implements the memory concepts discussed in §3.1.3 of the paper.
    """

    def __init__(self):
        self.history = []

    def add_entry(self, observation: str, thought: str, action: dict):
        self.history.append({
            "observation": observation,
            "thought_and_action": f"Thought: {thought}\nAction: Executed tool '{action['tool_name']}' with input '{action['tool_input']}'"
        })

    def get_context(self) -> str:
        """Formats the history into a string to be included in the LLM prompt."""
        if not self.history:
            return "This is the first step. I have no prior history."

        context_str = "Here is my history of previous steps (observation, my thought process, and my action):\n"
        for entry in self.history:
            context_str += f"- {entry['observation']}\n- {entry['thought_and_action']}\n\n"
        return context_str

    def summarize(self) -> str:
        """A placeholder for a real summarization call to an LLM."""
        summary = f"Summarized {len(self.history)} steps. Key activities include searching and getting weather."
        # In a real system, you would call an LLM to summarize self.history
        # and then replace self.history with the summary.
        self.history = [{"summary": summary}]
        return summary


# ==============================================================================
# §3.1 BRAIN MODULE: The core reasoning and planning engine
# ==============================================================================
class BrainModule:
    """
    The central controller of the agent, powered by an LLM.
    It performs reasoning and planning to decide the next action.
    This implementation emphasizes the Plan Formulation and Reflection stages (§3.1.4).
    """

    def __init__(self, llm_instance: MockLLM, memory_module: MemoryModule):
        self.llm = llm_instance
        self.memory = memory_module

    def _construct_prompt(self, current_observation: str) -> str:
        """
        Constructs the full ReAct-style prompt for the LLM.
        This prompt guides the LLM through the "think, act" cycle.
        """
        # This prompt structure is the core of the reasoning and planning module.
        prompt = f"""
You are an autonomous agent tasked with solving a user's request. You operate in a loop of Thought -> Action.

**Your Goal:** Fulfill the user's request by thinking step-by-step and using the available tools.

**Available Tools:**
- `search_web(query: str)`: Searches the web for information. Use for finding facts or general knowledge.
- `get_current_weather(city: str)`: Gets the current weather for a specific city.
- `summarize_memory()`: Condenses your memory if it gets too long.
- `respond_to_user(response_text: str)`: Use this tool ONLY when you have a complete and final answer for the user.
- `ask_clarifying_question(question_text: str)`: Use this tool if you are stuck or need more information from the user.

**Your Response Format:**
You MUST respond in a valid JSON format with two keys: "thought" and "action".
- `thought`: Your step-by-step reasoning about the current situation, your plan, and what you will do next.
- `action`: A dictionary containing the `tool_name` and `tool_input` for the tool you will use next.

---
**History:**
{self.memory.get_context()}

---
**Current Situation:**
{current_observation}

---
**Your Turn:**
Please provide your response in the specified JSON format.
"""
        return prompt

    def plan_and_reason(self, current_observation: str) -> (str, dict):
        """
        1. Constructs the prompt with current observation and memory.
        2. Calls the LLM.
        3. Parses the LLM's response to extract the thought and action.
        """
        prompt = self._construct_prompt(current_observation)
        llm_response_str = self.llm.call(prompt)

        try:
            # The LLM's textual response is parsed into a structured plan (thought + action)
            response_json = json.loads(llm_response_str)
            thought = response_json.get("thought", "No thought was provided.")
            action = response_json.get("action", {})
            if "tool_name" not in action or "tool_input" not in action:
                raise ValueError("LLM response is missing 'tool_name' or 'tool_input' in 'action'")
            return thought, action
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing LLM response: {e}\nResponse was: {llm_response_str}")
            # Self-correction: If the LLM fails, the brain decides to ask for help.
            return "I failed to generate a valid action.", {"tool_name": "ask_clarifying_question",
                                                            "tool_input": "My internal processing failed. Could you please rephrase your request?"}


# ==============================================================================
# The main Agent class that orchestrates the entire process
# ==============================================================================
class LLMAgent:
    """
    The complete LLM-based agent, integrating all modules.
    It follows the conceptual framework from Figure 2 of the paper,
    operating in a Perception -> Brain -> Action loop.
    """

    def __init__(self, max_steps: int = 5):
        print("Initializing agent...")
        self.max_steps = max_steps

        # Initialize modules
        self.memory = MemoryModule()
        # The ActionModule needs access to memory for the 'summarize_memory' tool
        self.action_module = ActionModule(self.memory)
        self.perception_module = PerceptionModule()
        # The Brain needs the LLM and Memory to reason
        self.brain = BrainModule(MockLLM(), self.memory)
        print("Agent initialized successfully.")

    def run(self, user_task: str):
        """The main execution loop of the agent."""
        print(f"\n--- Starting Agent Run for Task: '{user_task}' ---")

        # 1. PERCEPTION: Agent perceives the initial user task.
        current_observation = self.perception_module.perceive_user_input(user_task)

        for step in range(self.max_steps):
            print(f"\n--- Step {step + 1} ---")
            print(f"OBSERVATION: {current_observation}")

            # 2. BRAIN: Agent thinks, reasons, and plans the next action.
            thought, action = self.brain.plan_and_reason(current_observation)

            print(f"THOUGHT: {thought}")
            print(f"PLANNED ACTION: {action}")

            # Store the current state in memory before acting
            self.memory.add_entry(current_observation, thought, action)

            # 3. ACTION: Agent executes the planned action.
            tool_output = self.action_module.execute(action['tool_name'], action['tool_input'])

            # Check for termination conditions
            if tool_output.startswith("FINAL_RESPONSE:"):
                final_answer = tool_output.replace("FINAL_RESPONSE:", "").strip()
                print(f"\n--- Task Completed ---")
                print(f"Final Answer: {final_answer}")
                return
            elif tool_output.startswith("CLARIFICATION:"):
                question = tool_output.replace("CLARIFICATION:", "").strip()
                print(f"\n--- Agent Needs Help ---")
                print(f"Clarification Request: {question}")
                return

            # 4. PERCEPTION (Loop): Agent perceives the output of its action.
            current_observation = self.perception_module.perceive_tool_output(action['tool_name'], tool_output)

        print("\n--- Agent reached max steps without a final answer. ---")


# --- Main Execution ---
if __name__ == "__main__":
    # The user provides a high-level task that requires multiple steps.
    task = "What is the weather in the capital of France, and what should I wear?"

    # Create an agent instance and run the task.
    agent = LLMAgent(max_steps=5)
    agent.run(task)