from strands.hooks import (
    HookProvider,
    HookRegistry,
    BeforeToolCallEvent,
    BeforeInvocationEvent,
)
from collections import defaultdict


class RateLimitHook(HookProvider):
    """Limit tool calls per agent invocation"""

    def __init__(self, limits: dict[str, int]):
        """
        Args: limits: Dict mapping tool names to max calls per invocation
                        e.g. {"taviliy_search": 10, "save_note": 20}
        """
        self.limits = limits
        self._counts: dict[str, int] = defaultdict(int)

        def register_hooks(self, registry: HookRegistry) -> None:
            registry.add_callback(BeforeInvocationEvent, self._reset_counts)
            registry.add_callback(BeforeToolCallEvent, self._check_limit)

        def _reset_counts(self, event: BeforeInvocationEvent) -> None:
            """Reset counters at start of each agent() call."""
            self._counts.clear()

        def _check_limit(self, event: BeforeToolCallEvent) -> None:
            """Check and enforce rate_limits"""
            tool_name = event.tool_use["name"]

            if tool_name not in self.limits:
                return

            self._counts[tool_name] += 1

            if self._counts[tool_name] > self.limits[tool_name]:
                raise Exception(
                    f"Rate limit exceeded: {tool_name} called {self._counts[tool_name]} times"
                    f"(limit: {self.limits[tool_name]})"
                )
