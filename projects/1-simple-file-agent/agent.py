import json

from dotenv import load_dotenv

from openai.types.chat import ChatCompletion, ChatCompletionMessageToolCall
from openai.types.chat.chat_completion import Choice

from llm import get_completion
from memory import Memory
from agent_tool_service import AgentToolService
from utils import read_file

load_dotenv()


class Agent:

    # TODO : Implement proper memory (i.e save user preferences)
    # messages: list = memory.load_chat_history()

    def __init__(self, tool_service: AgentToolService, max_iterations: int = 10):
        self.tool_service: AgentToolService = tool_service
        self.MAX_ITERATIONS: int = max_iterations

        # self.memory: Memory = Memory()

        self.SYSTEM_PROMPT: str = read_file("system-prompt.md")
        self.messages: list = [
            {
                "role": "system",
                "content": self.SYSTEM_PROMPT,
            }
        ]

    def run(self, task: str):
        iteration_count: int = 0

        self.messages.append({
            "role": "user",
            "content": task,
        })

        while True and iteration_count < self.MAX_ITERATIONS:
            iteration_count += 1

            # Call the llm and retrieve the next tool call
            # TODO : Handle edge cases : http errors, llm refusal and miscellaneous errors
            # TODO : Monitor tokens count
            completion: ChatCompletion = get_completion(self.messages,
                                                        self.tool_service.get_tools_definition())

            print(f"\n{"*" * 20}")
            print(completion)

            first_completion_choice: Choice = completion.choices[0]

            # We parse the response to make sure it's a proper tool call
            # TODO : Wrap this inside a new class
            if first_completion_choice.finish_reason == "tool_calls" and first_completion_choice.message.tool_calls:
                # We add the tool call to the messages history
                self.messages.append(completion.choices[0].message.to_dict())

                # We retrieve the tool name & arguments
                tool_call: ChatCompletionMessageToolCall = first_completion_choice.message.tool_calls[0]
                tool_name: str = tool_call.function.name
                tool_arguments: dict = json.loads(tool_call.function.arguments)
                tool_call_id: str = tool_call.id

                print(f"\n{"*" * 20}")
                print(f"Tool called: {tool_name}")
                print(f"Tool arguments: {tool_arguments}")

                # We call the tool and pass the arguments
                tool_call_result = self.tool_service.invoke(tool_name, tool_arguments)

                print(f"\n{"*" * 20}")
                print(f"Tool call result: {type(tool_call_result)} — {str(tool_call_result)}")

                # We push the tool call response
                # TODO : If it's a file read, count the number of tokens and make sure it can fit inside the content window
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": str(tool_call_result)
                })

                # self.memory.save_chat_history(self.messages)

                if tool_name == "submit_final_response":
                    # If the user has a follow-up message, we add it to the conversation history
                    if tool_call_result is not None:
                        self.messages.append({
                            "role": "user",
                            "content": str(tool_call_result),
                        })

                        # We reset the iteration count
                        iteration_count = 0
                    else:
                        break  # The user doesn't have a follow-up question — we end it here

            else:
                raise Exception("Something went wrong. The agent didn't call a tool.")
