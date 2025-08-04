from dotenv import load_dotenv

from src.models.tool_call_response import ToolCallResult
from src.services.llm_service import LlmService
from src.contracts.tools.tool_service_contract import ToolServiceContract
from src.models.tool_call_request import ToolCallRequest

load_dotenv()


class Agent:

    def __init__(self, tool_service: ToolServiceContract, model: str, max_iterations: int = 20):
        self.__tool_service: ToolServiceContract = tool_service
        self.__MAX_ITERATIONS: int = max_iterations

        self.__llm_service: LlmService = LlmService(
            model=model,
            tools_definition=self.__tool_service.get_tools_definition()
        )

    def run(self, task: str):
        iteration_count: int = 0

        # We add the user request to the messages stack
        self.__llm_service.push_user_message(message=task)

        while True and iteration_count < self.__MAX_ITERATIONS:
            iteration_count += 1

            tool_call_request: ToolCallRequest = self.__llm_service.get_next_tool_call()

            # We call the tool and pass the arguments
            tool_call_result: ToolCallResult = self.__tool_service.invoke(
                tool_name=tool_call_request.tool_name,
                tool_args=tool_call_request.tool_arguments
            )

            print(f"\n{'*' * 20}")
            print(f"Tool call result: {type(tool_call_result.content)} — {str(tool_call_result.content)}")

            # We push the tool call response
            self.__llm_service.push_tool_response(
                tool_id=tool_call_request.tool_call_id,
                tool_call_result=tool_call_result.content
            )

            # If this is the final function call, we exit the loop
            if tool_call_result.is_last:
                break
