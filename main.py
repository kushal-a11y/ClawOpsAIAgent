from dotenv import load_dotenv
from planner import Planner
from tool_registry import ToolRegistry
from discord_tool import send_discord_message
from discord_bot import run_discord_bot


def execute_plan(plan, registry: ToolRegistry) -> None:
    print("\nValidated Plan:")
    print(plan.model_dump_json(indent=2))

    print("\nExecuting plan:")
    for step in plan.plan:
        print(f"Step {step.step}: action={step.action}, input={step.input}")
        if not registry.has_tool(step.action):
            print({"ok": False, "error": f"Unknown tool: {step.action}"})
            continue

        handler = registry.get_handler(step.action)
        result = handler(step.input)
        print(f"Result: {result}")

def build_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(
        name="send_discord_message",
        description="Send a plain text messgae to discord via webhook.",
        handler=send_discord_message
    )
    return registry

def main() -> None:
    load_dotenv()

    registry = ToolRegistry()
    registry.register(
        name="send_discord_message",
        description="Send a plain text message to Discord via webhook.",
        handler=send_discord_message,
    )

    goal = input("Enter goal: ").strip()
    planner = Planner(tools_prompt=registry.get_tools_prompt())

    try:
        plan = planner.create_plan(goal)
    except Exception as exc:
        print(f"Planning/validation failed: {exc}")
        return

    execute_plan(plan, registry)


if __name__ == "__main__":
    main()
