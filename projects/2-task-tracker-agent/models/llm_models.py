from typing import Union
from pydantic import BaseModel

from agent.tools import CreateTask, MessageUser


class LlmAction(BaseModel):
    reasoning: str
    tool_call: Union[CreateTask, MessageUser]
