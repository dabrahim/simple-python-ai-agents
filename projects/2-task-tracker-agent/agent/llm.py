from typing import List
from dotenv import load_dotenv

from openai import OpenAI
from agent.contracts.llm_interface import LLMInterface
from agent.events import Event, EventType
from models.llm_models import LlmAction

load_dotenv()


class OpenAILLM(LLMInterface):
    def __init__(self, model: str = "gpt-4.1-2025-04-14"):
        self.model = model
        self.client = OpenAI()

    def infer_next_action(self, events: List[Event]) -> LlmAction:
        """
        Convert events to messages and get next action from OpenAI.
        """
        messages = self._events_to_messages(events)

        completion = self.client.chat.completions.parse(
            model=self.model,
            messages=messages,  # type: ignore
            response_format=LlmAction
        )

        llm_action = completion.choices[0].message.parsed
        if llm_action is None:
            raise Exception("Failed to parse LLM response")

        return llm_action

    def _events_to_messages(self, events: List[Event]) -> List[dict[str, str]]:
        """Convert events to OpenAI message format."""
        return [self._event_to_message(event) for event in events]

    @staticmethod
    def _event_to_message(event: Event) -> dict[str, str]:
        """Convert a single event to OpenAI message format."""
        match event.type:
            case EventType.SYSTEM_MESSAGE:
                return {"role": "system", "content": str(event.content)}
            case EventType.USER_MESSAGE:
                return {"role": "user", "content": str(event.content)}
            case EventType.ASSISTANT_MESSAGE:
                return {"role": "assistant", "content": str(event.content)}
            case EventType.TOOL_CALL:
                # Convert LlmAction to readable format
                if hasattr(event.content, 'model_dump_json'):
                    return {"role": "assistant", "content": f"Tool call: {event.content.model_dump_json()}"}
                else:
                    return {"role": "assistant", "content": f"Tool call: {str(event.content)}"}
            case EventType.TOOL_RESULT:
                return {"role": "system", "content": f"Tool execution result: {str(event.content)}"}
            case EventType.TOOL_ERROR:
                return {"role": "system", "content": f"Tool error: {str(event.content)}"}
            case EventType.SYSTEM_ERROR:
                return {"role": "system", "content": f"System error: {str(event.content)}"}
            case _:
                return {"role": "system", "content": f"Unknown event: {str(event.content)}"}
