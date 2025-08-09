import json

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessageToolCall
from typing import Any
from src.models.tool_call_request import ToolCallRequest

from openai.types.chat.chat_completion import Choice

from src.services.memory_service import MemoryService
from src.contracts.logger_interface import LoggerInterface
from src.services.console_logger_service import ConsoleLoggerService
from src.utils.file_utils import read_file

load_dotenv()


class LlmService:
    def __init__(self, model: str, tools_definition: list, logger: LoggerInterface = None):
        self.__client: OpenAI = OpenAI()
        self.model = model
        self.tools_definition = tools_definition
        self.__logger = logger or ConsoleLoggerService()

        self.__SYSTEM_PROMPT: str = read_file("system-prompt.md")
        self.messages: list = [
            {
                "role": "system",
                "content": self.__SYSTEM_PROMPT
            }
        ]

        self.__memory: MemoryService = MemoryService(self.__logger)

    def get_next_tool_call(self) -> ToolCallRequest:
        # TODO : Handle edge cases : http errors, llm refusal and miscellaneous errors
        # TODO : Monitor tokens count
        completion: ChatCompletion = self.__client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools_definition,
        )

        first_completion_choice: Choice = completion.choices[0]

        # Check whether the response is a tool call
        # If it's a tool call, extract all the details and return them
        if first_completion_choice.finish_reason == "tool_calls" and first_completion_choice.message.tool_calls:
            # We add the tool call to the messages history
            self.__push_message(first_completion_choice.message.to_dict())

            # We retrieve the tool name & arguments
            tool_call: ChatCompletionMessageToolCall = first_completion_choice.message.tool_calls[0]

            tool_name: str = tool_call.function.name
            tool_arguments: dict = json.loads(tool_call.function.arguments)
            tool_call_id: str = tool_call.id

            self.__logger.log("", log_type='tool_call', tool_name=tool_name, tool_args=tool_arguments)

            return ToolCallRequest(
                tool_name=tool_name,
                tool_args=tool_arguments,
                tool_call_id=tool_call_id
            )

        else:
            # If it's not a tool call, raise an exception
            raise Exception(f"Unknown completion: {first_completion_choice}")

    def push_user_message(self, message: str) -> None:
        self.__push_message({
            "role": "user",
            "content": message
        })

    def push_tool_response(self, tool_id: str, tool_call_result: Any) -> None:
        self.__push_message({
            "role": "tool",
            "tool_call_id": tool_id,
            "content": str(tool_call_result)
        })

    def __push_message(self, message: dict) -> None:
        self.messages.append(message)
        self.__memory.save_chat_history(self.messages)
