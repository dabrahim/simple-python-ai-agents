from abc import ABC, abstractmethod


class LLMInterface(ABC):

    @abstractmethod
    def get_next_step(self):
        pass
