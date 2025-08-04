from typing import Any


class ToolCallResult:
    def __init__(self, content: Any = None, exit_loop: bool = False):
        self.content = content
        self.is_last = exit_loop