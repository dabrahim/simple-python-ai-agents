from typing import Any


class ToolCallResult:
    def __init__(self, content: Any = None, exit_loop: bool = False):
        self.content = content
        self.exit_loop = exit_loop