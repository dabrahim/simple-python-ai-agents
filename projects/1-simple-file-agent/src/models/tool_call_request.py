class ToolCallRequest:
    def __init__(self, tool_name: str, tool_args: dict, tool_call_id: str):
        self.tool_name = tool_name
        self.tool_arguments = tool_args
        self.tool_call_id = tool_call_id