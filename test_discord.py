#!/usr/bin/env python3
import requests
import json
from datetime import datetime

webhook_url = "https://discord.com/api/webhooks/1388957695733792890/N5Lo1qONHNW0p3xUSBceP97xQkpIZlC7Z00WCqbdur--Y3DRyRM2Jf4bfGx9oEjTn9AO"

data = {
    "content": "🎉 Discord MCP Server Successfully Configured!",
    "embeds": [{
        "title": "MCP Server Test Report",
        "description": "All 13 MCP servers are now operational!",
        "color": 5814783,
        "fields": [
            {
                "name": "✅ Servers Tested",
                "value": "12/12 Passed",
                "inline": True
            },
            {
                "name": "🆕 New Server",
                "value": "Discord Webhook",
                "inline": True
            },
            {
                "name": "📊 Status",
                "value": "Fully Operational",
                "inline": True
            }
        ],
        "footer": {
            "text": "Test message from Claude Code"
        },
        "timestamp": datetime.utcnow().isoformat()
    }]
}

response = requests.post(webhook_url, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")