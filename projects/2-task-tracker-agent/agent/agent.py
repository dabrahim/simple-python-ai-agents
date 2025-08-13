import json

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion

from agent.llm import LlmAction

load_dotenv()


class Agent:
    def __init__(self) -> None:
        self._SYSTEM_PROMPT = "You are a Tasky, an AI agent that helps the user better organize their tasks by calling tools. When you are done, message the user with a message to display them."

        self._messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": self._SYSTEM_PROMPT,
            }
        ]

    def run(self, message: str):
        # TODO : Push the user message to the event stack
        self._messages.append({"role": "user", "content": message})

        client: OpenAI = OpenAI()

        iteration: int = 0

        while True and iteration < 5:
            iteration += 1

            print(f"\n\n{"*" * 20}")
            print(f"Iteration: {iteration}")
            print(f"{"*" * 20}")

            completion = client.chat.completions.parse(
                model="gpt-4.1-2025-04-14",
                messages=self._messages,  # type: ignore
                response_format=LlmAction
            )

            # self._log_completion(completion)

            # choices: list[Choice] = completion.choices
            llm_action: LlmAction | None = completion.choices[0].message.parsed

            if llm_action:
                # TODO: push the tool call to events stack (TOOL_CALL) or consider including reasoning and make it (ASSISTANT_MESSAGE)
                print(f"Reasoning : {llm_action.reasoning}")

                self._messages.append({
                    "role": "assistant",
                    "content": f"Tool call : {llm_action.model_dump_json()}",
                })

                tool_call = llm_action.tool_call

                print(f"Tool call type: {type(tool_call)}")
                print(f"Tool call : {tool_call}")

                tool_result = tool_call.execute()

                # TODO: Push tool call result to events stack
                self._messages.append({
                    "role": "system",
                    "content": f"Tool '{tool_call.name}' executed successfully. Result: {tool_result}"
                })

            else:
                raise Exception("Parsed response is null : No tool call found")

    @staticmethod
    def _log_completion(completion: ChatCompletion) -> None:
        print(json.dumps(completion.to_dict(), indent=2))

        # sample api response
        """
        {
          "id": "<…>",
          "choices": [
            {
              "finish_reason": "stop",
              "index": 0,
              "logprobs": null,
              "message": {
                "content": "Task: Go to the grocery store  \nWhen: Tomorrow afternoon\n\nWould you like to set a specific time, or add a shopping list for your grocery trip?",
                "refusal": null,
                "role": "assistant",
                "annotations": []
              }
            }
          ],
          "created": 1755094512,
          "model": "gpt-4.1-2025-04-14",
          "object": "chat.completion",
          "service_tier": "default",
          "system_fingerprint": "<…>",
          "usage": {
            "completion_tokens": 32,
            "prompt_tokens": 39,
            "total_tokens": 71,
            "completion_tokens_details": {
              "accepted_prediction_tokens": 0,
              "audio_tokens": 0,
              "reasoning_tokens": 0,
              "rejected_prediction_tokens": 0
            },
            "prompt_tokens_details": {
              "audio_tokens": 0,
              "cached_tokens": 0
            }
          }
        }
        """
