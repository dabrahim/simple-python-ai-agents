from agent.contracts.llm_interface import LLMInterface
from agent.events import Event, EventType
from agent.llm import OpenAILLM
from typing import Optional

from models.llm_models import LlmAction


class Agent:
    def __init__(self, llm: Optional[LLMInterface] = None) -> None:
        system_prompt: str = "You are a Tasky, an AI agent that helps the user better organize their tasks by calling tools. When you are done, message the user with a message to display them."

        self._events: list[Event] = [
            Event(type=EventType.SYSTEM_MESSAGE, content=system_prompt)
        ]

        # Dependency injection for LLM
        self._llm = llm or OpenAILLM()

    @staticmethod
    def print_title(message: str):
        message_length = len(message)
        dots: str = "•" * (message_length + 4)
        print(f"\n{dots}\n• {message} •\n{dots}")

    def run(self, message: str):
        self._events.append(Event(type=EventType.USER_MESSAGE, content=message))

        iteration: int = 0

        while True and iteration < 5:
            iteration += 1

            # self.print_title(f"Iteration: {iteration}")

            try:
                # Use LLM to infer next action
                llm_action: LlmAction = self._llm.infer_next_action(self._events)

                # Add tool call to events
                self._events.append(Event(type=EventType.TOOL_CALL, content=llm_action))

                # print(f"Reasoning : {llm_action.reasoning}")
                self.print_title("REASONING")
                print(f"{llm_action.reasoning}\n")

                tool_call = llm_action.tool_call

                self.print_title("TOOL CALL")
                print(f"Type: {type(tool_call)}")
                print(f"Object : {tool_call}")

                try:
                    tool_result = tool_call.execute()
                    # Add successful tool result to events
                    self._events.append(Event(type=EventType.TOOL_RESULT, content=tool_result))
                except Exception as e:
                    # Add tool error to events
                    self._events.append(Event(type=EventType.TOOL_ERROR, content=str(e)))

            except Exception as e:
                # Add system error to events
                self._events.append(Event(type=EventType.SYSTEM_ERROR, content=str(e)))
                print(f"System error: {e}")
                break
