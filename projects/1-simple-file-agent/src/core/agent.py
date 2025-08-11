from dotenv import load_dotenv

from src.models.tool_call_response import ToolCallResult
from src.services.llm_service import LlmService
from src.contracts.tool_service_interface import ToolServiceInterface
from src.contracts.logger_interface import LoggerInterface
from src.services.console_logger_service import ConsoleLoggerService
from src.models.tool_call_request import ToolCallRequest

load_dotenv()


class Agent:

    def __init__(self, tool_service: ToolServiceInterface, model: str, max_iterations: int = 20,
                 logger: LoggerInterface | None = None):
        self.__tool_service: ToolServiceInterface = tool_service
        self.__MAX_ITERATIONS: int = max_iterations
        self.__logger = logger or ConsoleLoggerService()

        self.__llm_service: LlmService = LlmService(
            model=model,
            tools_definition=self.__tool_service.get_tools_definition(),
            logger=self.__logger
        )

    def run(self, task: str):
        iteration_count: int = 0

        self.__logger.log_progress("Starting task processing...")

        # We add the user request to the messages stack
        self.__llm_service.push_user_message(message=task)

        while True and iteration_count < self.__MAX_ITERATIONS:
            iteration_count += 1

            tool_call_request: ToolCallRequest = self.__llm_service.get_next_tool_call()

            # We call the tool and catch any exceptions to feed back to the LLM
            try:
                tool_call_result: ToolCallResult = self.__tool_service.invoke(
                    tool_call=tool_call_request,
                )
            except Exception as e:
                error_message = f"Tool execution failed: {str(e)}"
                self.__logger.log_error(error_message)

                # Create error result to feed back to LLM
                tool_call_result = ToolCallResult(
                    content=error_message,
                    exit_loop=False
                )

            self.__logger.log_tool_result(tool_call_result.content)

            # We push the tool call response
            self.__llm_service.push_tool_response(
                tool_id=tool_call_request.tool_call_id,
                tool_call_result=tool_call_result.content
            )

            # If this is the final function call, we exit the loop
            if tool_call_result.exit_loop:
                break
