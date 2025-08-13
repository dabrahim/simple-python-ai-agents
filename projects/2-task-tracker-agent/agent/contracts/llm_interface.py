from abc import ABC, abstractmethod
from typing import List

from agent.events import Event
from models.llm_models import LlmAction


class LLMInterface(ABC):

    @abstractmethod
    def infer_next_action(self, events: List[Event]) -> LlmAction:
        pass
