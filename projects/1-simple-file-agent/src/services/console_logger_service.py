from src.contracts.logger_interface import LoggerInterface
from typing import Dict, Any
import json


class ConsoleLoggerService(LoggerInterface):
    """
    Console implementation of specialized AI agent logging.
    Provides clear, hierarchical output with professional visual formatting.
    """

    def __init__(self, max_content_length: int = 100):
        """
        Initialize console logger.
        
        Args:
            max_content_length: Maximum characters before content is truncated
        """
        self.max_content_length = max_content_length

    def log_tool_call(self, tool_name: str, tool_args: Dict[str, Any] = None) -> None:
        """Log tool call with clean formatting and truncated arguments."""
        print(f"\n🔧 Calling: {tool_name}")
        if tool_args:
            args_str = json.dumps(tool_args, indent=None, separators=(',', ':'))
            if len(args_str) > 60:
                args_str = args_str[:57] + "..."
            print(f"   └─ Args: {args_str}")

    def log_tool_result(self, content: Any) -> None:
        """Log tool result with ellipsizing for long content."""
        content_str = str(content)
        
        if len(content_str) <= self.max_content_length:
            print(f"   ✓ Result: {content_str}")
        else:
            truncated = content_str[:self.max_content_length] + "..."
            print(f"   ✓ Result: {truncated}")
            print(f"   └─ ({len(content_str)} chars total)")

    def log_agent_response(self, message: str) -> None:
        """Log final agent response with clear visual separation."""
        print(f"\n{'=' * 60}")
        print(f"🤖 AGENT RESPONSE")
        print(f"{'=' * 60}")
        print(f"{message}")
        print(f"{'=' * 60}\n")

    def log_progress(self, message: str) -> None:
        """Log progress/status updates with hourglass icon."""
        print(f"⏳ {message}")

    def log_error(self, message: str) -> None:
        """Log errors with clear visual indication."""
        print(f"❌ Error: {message}")

    def log_user_prompt(self, message: str) -> None:
        """Log user interaction prompts with question mark icon."""
        print(f"\n❓ {message}")