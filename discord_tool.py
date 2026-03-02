import os
import requests


def send_discord_message(message: str) -> dict:
    # Read the webhook URL from environment variables
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        # Fail fast if the URL is missing
        return {"ok": False, "error": "DISCORD_WEBHOOK_URL is missing"}

    # Discord webhook payload expects "content"
    payload = {"content": message}

    try:
        # Send HTTP POST to Discord
        response = requests.post(webhook_url, json=payload, timeout=15)

        # Success is any 2xx response
        if 200 <= response.status_code < 300:
            return {"ok": True, "status_code": response.status_code}

        # Non-2xx responses return error info
        return {
            "ok": False,
            "status_code": response.status_code,
            "error": response.text,
        }
    except Exception as exc:
        # Catch network/timeouts and return readable error
        return {"ok": False, "error": str(exc)}
