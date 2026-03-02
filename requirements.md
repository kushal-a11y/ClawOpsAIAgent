1. Go to the Discord Developer Portal and create a new application.  
2. Open the application and click **Bot** in the left sidebar.  
3. Click **Add Bot**.  
4. Under **Token**, click **Reset Token** or **Copy** and save it as `DISCORD_BOT_TOKEN`.  
5. Go to **OAuth2 → URL Generator**.  
6. Select **bot** scope.  
7. Select permissions: **Read Messages/View Channels**, **Send Messages**, **Read Message History**.  
8. Open the generated URL and authorize the bot into your server.  
9. In Discord app, enable **Developer Mode** (User Settings → Advanced).  
10. Right‑click your command channel → **Copy ID** and save it as `COMMAND_CHANNEL_ID`.  

That’s the full sequence. If you want, I can also give the minimal permission set for a read‑only bot or add a command prefix setup.

Detailed description of what you have done in this chat:
You set the project goal to build a structured AI workflow planning agent, not a chatbot. You defined the architecture: user goal → planner → JSON plan → schema validation → execution engine → tool integration. You chose Python and set strict requirements: deterministic planning, JSON only, no markdown, schema enforcement, and a real integration. You decided to avoid API keys by using Ollama locally instead of OpenAI. You installed Ollama, pulled a model, and set `.env` values for `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, and `DISCORD_WEBHOOK_URL`. You implemented the core code modules: `tool_registry.py` for tool registration and prompt injection, `plan_schema.py` for Pydantic validation, `planner.py` for strict planning with Ollama and JSON parsing, `discord_tool.py` for sending webhook messages, and `main.py` for the CLI flow. You tested the pipeline by running `python main.py`, entering a goal, receiving a valid plan, and executing the Discord webhook successfully. You hit a `TypeError` in `tool_registry.py` caused by incorrectly setting `_tools` to a `Dict[...]` type instead of an actual dict, and you fixed it. You clarified the current behavior: Discord is only an output target and input is via terminal, not via Discord. You asked how to get a Discord webhook URL, and you learned how to set up the webhook. You asked how to get a Discord bot token and channel ID for receiving commands, and you learned the developer portal steps, OAuth2 bot invite, permissions, and copying the channel ID. You asked for `requirements.txt` and got the dependency list including `discord.py` for a future bot listener. You discussed the shift in scope from a one‑tool demo to a broader personal agent with many apps, and you chose Phase 1 as adding a Discord bot input channel.

Complete “goal book” for a full AI agent that can receive natural language from any app and perform commanded operations:

1) Core mission
Build a production‑structured personal agent platform that accepts natural‑language commands from multiple input channels and executes them safely across many apps.

2) Required architecture components
- Input adapters: Discord bot, email listener, web UI, mobile app, Slack/Telegram, API endpoint.
- Planner: LLM system that converts NL into structured plans (JSON) using a fixed schema, temperature 0.
- Schema enforcement: validation to reject malformed or unsafe plans.
- Executor: executes steps deterministically, tool by tool, with a registry and clear error handling.
- Tool layer: each app integration is isolated, versioned, tested, and documented.
- Safety layer: allowlists, confirmation flows, scope limits, rate limits, and audit logs.

3) Functional requirements
- Accept NL from any connected channel (Discord, Slack, web API, etc.).
- Translate NL to strict plan structure.
- Validate plan before execution.
- Map actions to registered tools only.
- Execute steps and report results to the originating channel.
- Support multi‑step workflows.

4) Tool requirements (minimum viable multi‑app set)
- Messaging: Discord, Slack, Telegram.
- Email: SMTP or Gmail API.
- Calendar: Google Calendar API.
- File operations: local file read/write, search, and report.
- Web fetch: HTTP GET/POST tool with domain allowlist.
- Social posting: requires OAuth and platform approvals (Instagram, X, LinkedIn).

5) Security and safety requirements
- Tool allowlists per channel/user.
- Confirmation required for destructive or external actions (sending email, posting publicly, payments).
- Secrets stored in `.env` or vault, never in code.
- Structured logging of plans and executions.

6) Reliability requirements
- Deterministic planner output.
- Retry logic for transient failures.
- Clear error messages in the response channel.
- Timeouts for external calls.

7) Observability requirements
- Execution logs with timestamps, tool names, results.
- Plan and execution trace stored for debugging.
- Optional analytics of tool usage and failures.

8) Deployment requirements
- Local mode (single user, Ollama).
- Server mode (multi‑user, hosted LLM or self‑hosted).
- Containerization (Docker) for reproducibility.

9) Roadmap from current state
- Phase 1: Discord bot input (receive commands, respond with results).
- Phase 2: Add 2–3 core tools (email, calendar, web fetch).
- Phase 3: Safety layer and confirmations.
- Phase 4: Multi‑channel input (Slack/web API).
- Phase 5: OAuth‑based social tools.

10) Executor requirements (critical)
- Only execute validated actions.
- No dynamic code execution from LLM output.
- Every tool call returns a structured result.
- Provide a final summary back to the user channel.

If you want, I can convert this into a formal system requirements doc, or move directly to implementing Phase 1 in code.