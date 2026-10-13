# web-search (open-bot plugin)

Web search for your open-bot desktop agent, with automatic provider fallback:

| order | provider | cost |
| ----- | -------- | ---- |
| 1 | **Brave Search API** | free plan: 2 000 searches/month |
| 2 | **Tavily** | free plan: 1 000 searches/month |
| 3 | **Cloudflare Web Search** | pay per search via AI Gateway credits or BYOK |

The agent runs one command:

```sh
ob-plugin-web-search-search "best 3d printer under 300$" --limit 5
```

- `auto` tries providers in the configured order, skipping unconfigured or
  quota-exhausted ones, and returns the first answer (JSON).
- When the free monthly quotas are used up and no paid provider is configured, the tool
  exits with `free_quota_exhausted` and posts one dashboard notification per day saying
  the user should wait for the monthly reset (1st) or configure a paid provider.
- `ob-plugin-web-search-search usage` shows the per-provider monthly counters.

## Install

```sh
ob-plugin install web-search
ob-plugin guide web-search   # walkthrough for the API keys
```

## Keys

Brave and Tavily keys can be pasted by the user on the Plugins page (secret settings
`brave_api_key`, `tavily_api_key`) or filled in the vault. The plugin reads the
setting first, then the vault.

| vault slug | where to get it |
| ---------- | --------------- |
| `brave-api-key` | https://api-dashboard.search.brave.com — free plan, 2 000 req/month |
| `tavily-api-key` | https://app.tavily.com — free plan, 1 000 req/month |
| `cf-account-id` + `cf-api-token` | Cloudflare dash → account id; API token needs **Workers AI: Read** + **AI Gateway: Read**. The account needs AI Gateway credits, or a provider key (Ceramic/Exa/Linkup) stored on the gateway. |

## Settings

| key | default | what it does |
| --- | ------- | ------------ |
| `order` | `brave,tavily,cloudflare` | provider fallback order |
| `default_limit` | `5` | results per search (1-10) |
| `brave_monthly_quota` | `2000` | local counter ceiling for Brave |
| `tavily_monthly_quota` | `1000` | local counter ceiling for Tavily |
| `cf_provider` | `ceramic` | upstream provider Cloudflare uses (`ceramic`, `exa`, `linkup`) |
| `cf_gateway` | `default` | Cloudflare AI Gateway id |
| `notify_on_exhausted` | `true` | dashboard notification when free quotas run out |

Counters live in `~/.open-bot/web-search/usage.json` and reset automatically each month.
