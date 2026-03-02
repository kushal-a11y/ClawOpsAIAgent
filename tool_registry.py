from typing import Callable, Dict, Any


class ToolRegistry:
    def __init__(self) -> None:
        # Internal map:
        # tool_name -> {"description": str, "handler": callable}
        self._tools: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, description: str, handler: Callable[[str], dict]) -> None:
        # Register one executable tool.
        # handler takes one string input and returns a result dict.
        self._tools[name] = {
            "description": description,
            "handler": handler,
        }

    def has_tool(self, name: str) -> bool:
        # Used by execution engine to block unknown actions safely.
        return name in self._tools

    def get_handler(self, name: str) -> Callable[[str], dict]:
        # Returns function to execute for a valid action.
        return self._tools[name]["handler"]

    def get_tools_prompt(self) -> str:
        # Converts registry into prompt text for LLM planner.
        # This constrains planning to known tools.
        lines = []
        for name, meta in self._tools.items():
            lines.append(f"- {name}: {meta['description']}")
        return "\n".join(lines)

    def list_tool_names(self) -> list[str]:
        # Helper for debugging/validation/reporting
        return list(self._tools.keys())
