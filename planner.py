import json
import os
import requests
from plan_schema import ExecutionPlan


class Planner:
    def __init__(self, tools_prompt: str) -> None:
        # Text list of tools inserted into the prompt
        self.tools_prompt = tools_prompt

        # Ollama config (local by default)
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

    def _build_prompt(self, goal: str) -> str:
        # Builds the strict prompt the model must follow
        return f"""
            You are a workflow planner.
            
            Available tools:
            {self.tools_prompt}
            
            User goal:
            {goal}
            
            Return ONLY valid JSON with this exact structure:
            {{
              "goal": "string",
              "plan": [
                {{
                  "step": 1,
                  "action": "tool_name",
                  "input": "string"
                }}
              ]
            }}
            
            Rules:
            - Output JSON only.
            - No markdown.
            - No explanation text.
            - Use only available tools.
            - Keep steps minimal and deterministic.
            """.strip()

    def _call_ollama(self, prompt: str) -> str:
        # Calls Ollama local API and returns raw text response
        url = f"{self.ollama_base_url}/api/generate"
        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0},
        }
        resp = requests.post(url, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "").strip()

    def _parse_json_strict(self, text: str) -> dict:
        # Converts model output to Python dict; throws if invalid JSON
        return json.loads(text)

    def create_plan(self, goal: str) -> ExecutionPlan:
        # Full planning pipeline: prompt -> LLM -> JSON -> schema validation
        prompt = self._build_prompt(goal)
        raw = self._call_ollama(prompt)
        parsed = self._parse_json_strict(raw)
        return ExecutionPlan.model_validate(parsed)
