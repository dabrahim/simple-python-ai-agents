from src.contracts.logger_interface import LoggerInterface
import json


class ConsoleLoggerService(LoggerInterface):
    """
    Enhanced console logger with improved visual formatting for AI agent interactions.
    Provides clear, hierarchical output with appropriate visual emphasis.
    """

    def __init__(self):
        """Initialize console logger with improved formatting."""
        self.max_content_length = 100  # Max chars before ellipsizing

    def log(self, message: str, **kwargs) -> None:
        """
        Display enhanced formatted messages based on message type.
        
        Args:
            message: The message to display
            **kwargs: Formatting options:
                - log_type: 'tool_call', 'tool_result', 'agent_response', 'user_prompt', 'progress', 'error'
                - tool_name: Name of tool being called
                - tool_args: Tool arguments dict
                - content: Content to display (will be ellipsized if too long)
                - show_separator: Override separator behavior
        """
        log_type = kwargs.get('log_type', 'default')
        
        if log_type == 'tool_call':
            self._log_tool_call(kwargs.get('tool_name', ''), kwargs.get('tool_args', {}))
        elif log_type == 'tool_result':
            self._log_tool_result(kwargs.get('content', ''))
        elif log_type == 'agent_response':
            self._log_agent_response(message)
        elif log_type == 'user_prompt':
            self._log_user_prompt(message)
        elif log_type == 'progress':
            self._log_progress(message)
        elif log_type == 'error':
            self._log_error(message)
        else:
            # Default simple logging
            print(f"  {message}")

    def _log_tool_call(self, tool_name: str, tool_args: dict) -> None:
        """Log tool call with clean formatting."""
        print(f"\n🔧 Calling: {tool_name}")
        if tool_args:
            # Format args nicely, truncate if too long
            args_str = json.dumps(tool_args, indent=None, separators=(',', ':'))
            if len(args_str) > 60:
                args_str = args_str[:57] + "..."
            print(f"   └─ Args: {args_str}")

    def _log_tool_result(self, content: str) -> None:
        """Log tool result with ellipsizing for long content."""
        content_str = str(content)
        
        if len(content_str) <= self.max_content_length:
            print(f"   ✓ Result: {content_str}")
        else:
            truncated = content_str[:self.max_content_length] + "..."
            print(f"   ✓ Result: {truncated}")
            print(f"   └─ ({len(content_str)} chars total)")

    def _log_agent_response(self, message: str) -> None:
        """Log final agent response with clear visual separation."""
        print(f"\n{'=' * 60}")
        print(f"🤖 AGENT RESPONSE")
        print(f"{'=' * 60}")
        print(f"{message}")
        print(f"{'=' * 60}\n")

    def _log_user_prompt(self, message: str) -> None:
        """Log user interaction prompts."""
        print(f"\n❓ {message}")

    def _log_progress(self, message: str) -> None:
        """Log progress/status updates."""
        print(f"⏳ {message}")

    def _log_error(self, message: str) -> None:
        """Log errors with clear visual indication."""
        print(f"❌ Error: {message}")