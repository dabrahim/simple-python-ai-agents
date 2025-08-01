from dotenv import load_dotenv

from src.services.llm_service import LlmService
from src.contracts.tools.tool_service_contract import ToolServiceContract
from src.models.tool_call_request import ToolCallRequest

load_dotenv()


class Agent:

    # TODO : Implement proper memory (i.e save user preferences)
    # messages: list = memory.load_chat_history()

    def __init__(self, tool_service: ToolServiceContract, max_iterations: int = 10):
        self.__tool_service: ToolServiceContract = tool_service
        self.__MAX_ITERATIONS: int = max_iterations
        self.__llm_service: LlmService = LlmService(
            model="gpt-4.1",
            tools=self.__tool_service.get_tools_definition()
        )
        # self.memory: Memory = Memory()

    def run(self, task: str):
        iteration_count: int = 0

        # We add the user request to the messages stack
        self.__llm_service.push_user_message(message=task)

        while True and iteration_count < self.__MAX_ITERATIONS:
            iteration_count += 1

            tool_call_request: ToolCallRequest = self.__llm_service.get_next_tool_call()

            # We call the tool and pass the arguments
            tool_call_result = self.__tool_service.invoke(
                tool_name=tool_call_request.tool_name,
                tool_args=tool_call_request.tool_arguments
            )

            print(f"\n{'*' * 20}")
            print(f"Tool call result: {type(tool_call_result)} — {str(tool_call_result)}")

            # TODO : If it's a file read, count the number of tokens and make sure it can fit inside the content window

            # We push the tool call response
            self.__llm_service.push_tool_response(
                tool_id=tool_call_request.tool_call_id,
                tool_call_result=tool_call_result
            )

            # self.memory.save_chat_history(self.messages)

            if tool_call_request.tool_name == "submit_final_response":
                # If the user has a follow-up message, we add it to the conversation history
                if tool_call_result is not None:
                    self.__llm_service.push_user_message(message=str(tool_call_result))

                    # We reset the iteration count
                    iteration_count = 0
                else:
                    break  # The user doesn't have a follow-up question — we end it here
