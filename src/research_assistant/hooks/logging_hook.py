from strands.hooks import (
    HookProvider,
    HookRegistry,
    BeforeToolCallEvent,
    AfterToolCallEvent,
)
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("research_assistant")


class ToolLoggingHook(HookProvider):
    """
    Log all tool invocations with timing information
    """

    def __init__(self):
        self._start_times: dict[str, datetime] = {}

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeToolCallEvent, self.on_before_call)
        registry.add_callback(AfterToolCallEvent, self.on_after_call)

    def _on_before_tool(self, event: BeforeToolCallEvent) -> None:
        tool_use = event.tool_use
        tool_id = tool_use["toolUseId"]
        tool_name = tool_use["name"]
        tool_input = tool_use.get("input", {})

        self._start_times[tool_id] = datetime.now()

        logger.info(f"[TOOL START] {tool_name}")
        logger.debug(f" Input: {tool_input}")

    def _on_after_tool(self, event: AfterToolCallEvent) -> None:
        tool_result = event.tool_result
        tool_id = tool_result["toolUseId"]
        status = tool_result.get("status", "unknown")

        start_time = self._start_times.pop(tool_id, None)
        duration = (datetime.now() - start_time).total_seconds() if start_time else 0

        logger.info(f"[TOOL END] status={status} duration={duration:.2f}s")
