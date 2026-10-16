#!/usr/bin/env python3
"""Assemble open-bot.plugin.json from the sources in src/ (no JSON escaping by hand)."""
import json
import pathlib

root = pathlib.Path(__file__).parent
tool = (root / "src/tool.ts").read_text()
skill = (root / "src/skill.md").read_text()

manifest = {
    "$schema": "/home/agent/.config/opencode/skills/plugin/open-bot.plugin.schema.json",
    "id": "web-search",
    "name": "Web Search",
    "version": "0.1.0",
    "description": (
        "Web search for the agent: Brave and Tavily free tiers with automatic "
        "monthly-quota fallback, then Cloudflare Web Search as the paid safety net; "
        "notifies the user when free quotas run out."
    ),
    "author": "shpaw415",
    "repo": "shpaw415/web-search",
    "category": "utilities",
    "tags": ["search", "web", "brave", "tavily", "cloudflare", "agent"],
    "permissions": {
        "vaultCreate": ["brave-api-key", "tavily-api-key", "cf-account-id", "cf-api-token"],
        "notifications": True,
    },
    "tools": [{"name": "search", "content": tool}],
    "configs": [
        {"key": "order", "label": "Provider fallback order", "def": "brave,tavily,cloudflare"},
        {"key": "default_limit", "label": "Default results per search (1-10)", "type": "number", "min": 1, "max": 10, "def": "5"},
        {"key": "brave_monthly_quota", "label": "Brave free quota per month", "type": "number", "min": 0, "def": "2000"},
        {"key": "tavily_monthly_quota", "label": "Tavily free quota per month", "type": "number", "min": 0, "def": "1000"},
        {"key": "brave_api_key", "label": "Brave Search API key (or vault brave-api-key)", "type": "secret", "def": ""},
        {"key": "tavily_api_key", "label": "Tavily API key (or vault tavily-api-key)", "type": "secret", "def": ""},
        {"key": "cf_provider", "label": "Cloudflare upstream provider", "type": "enum", "options": ["ceramic", "exa", "linkup"], "def": "ceramic"},
        {"key": "cf_gateway", "label": "Cloudflare AI Gateway id", "def": "default"},
        {"key": "notify_on_exhausted", "label": "Notify when free quotas are exhausted", "type": "bool", "def": "true"},
    ],
    "skills": [
        {
            "name": "web-search",
            "description": (
                "Search the web for current information with ob-plugin-web-search-search "
                "(Brave/Tavily free with quota fallback, Cloudflare paid). Use for any query "
                "needing fresh web results: news, prices, docs, facts, verification."
            ),
            "body": skill,
        }
    ],
}

out = root / "open-bot.plugin.json"
out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
print(f"wrote {out} ({out.stat().st_size} bytes, tool {len(tool)} chars)")
