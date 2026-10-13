# Configuring web-search with the user

You are configuring the `web-search` open-bot plugin on this desktop for the user.
Walk them through it step by step. Never print or echo secret values; fill
them with the write-only commands shown here.

## What this plugin needs

- The plugin gives the agent one command for web searches across three providers:
  Brave (free 2 000/month), Tavily (free 1 000/month), then Cloudflare Web Search
  (paid per search) as the safety net. It auto-falls-back when a free quota is used up
  and notifies the user when everything free is exhausted.
- At least one provider must be configured before the plugin is useful.
  The two free keys take minutes to create; the Cloudflare keys are optional and
  only needed if the user wants the paid fallback.

## Settings

Change with `ob-plugin settings web-search KEY=value` (or the Plugins page).

| key | type | default | what to ask the user |
| --- | ---- | ------- | -------------------- |
| order | string | brave,tavily,cloudflare | Keep the default unless they want a specific provider first. |
| default_limit | number | 5 | How many results per search (1-10). Default is fine. |
| brave_monthly_quota | number | 2000 | Matches Brave's free plan; raise only if they upgrade. |
| tavily_monthly_quota | number | 1000 | Matches Tavily's free plan; raise only if they upgrade. |
| cf_provider | enum | ceramic | Upstream engine Cloudflare uses (ceramic / exa / linkup). ceramic is cheapest ($0.25/1000). |
| cf_gateway | string | default | Their AI Gateway id; `default` exists on every account. |
| notify_on_exhausted | bool | true | Keep on so the user learns when free quotas run out. |

## Keys — two ways to fill them

Each of Brave and Tavily can be filled either as a **secret setting on the Plugins
page** (easiest: the user types it themselves) or as a **vault key**. The plugin reads
the setting first, then the vault. Cloudflare keys are vault-only.

On the Plugins page (values are hidden once saved):

- `brave_api_key` — paste the Brave Search API key here.
- `tavily_api_key` — paste the Tavily API key here.

Or fill the vault with `ob-plugin vault web-search SLUG=value` (write-only; never
echo the value):

- `brave-api-key` — Brave Search API key. The user creates one at
  https://api-dashboard.search.brave.com (sign up, free plan, then "API Keys" → create).
  Ask: "Do you want the free Brave key? It's 2 000 searches/month."
- `tavily-api-key` — Tavily API key. The user creates one at
  https://app.tavily.com (sign up, free plan, the key is on the home page).
  Ask: "Do you also want the free Tavily key? 1 000 searches/month, used as backup."
- `cf-account-id` — Cloudflare account id (dash.cloudflare.com → any domain/account
  overview → "Account ID" on the right). Not secret-sensitive but write-only is fine.
- `cf-api-token` — Cloudflare API token with **Account → Workers AI → Read** and
  **Account → AI Gateway → Read** permissions. Create at dash.cloudflare.com →
  My Profile → API Tokens. The account must have AI Gateway credits loaded, or a
  provider key (Ceramic/Exa/Linkup) stored under AI Gateway → Provider Keys with
  alias `default` — otherwise every Cloudflare call fails with
  `web_search_byok_not_configured`.

All keys are optional; configure at least one provider. The plugin skips unconfigured
providers automatically.

## Walkthrough

1. Check what is already there: `ob-plugin settings web-search` and `ob-plugin vault web-search`.
2. Offer the two free keys first (Brave, Tavily) — the user can paste them on the
   Plugins page (`brave_api_key`, `tavily_api_key`), or you fill the vault as each
   key is confirmed:
   `ob-plugin vault web-search brave-api-key=...`
3. Offer the Cloudflare fallback last; remind them it needs credits or a gateway
   provider key, not just a token.
4. Remind: settings stay at defaults unless they say otherwise.

## Verify

- `ob-plugin-web-search-search "cloudflare workers ai" --limit 3` → JSON with
  `ok:true`, a `provider` and 1-3 `items`.
- `ob-plugin-web-search-search usage` → counters and `resetsOn` date.
- If the first call returns `free_quota_exhausted` while keys were just filled,
  re-check which vault slugs are still empty (`ob-plugin vault web-search`).

## Troubleshooting

- `web_search_byok_not_configured` (Cloudflare) — no AI Gateway credits and no
  provider key on the gateway. Load credits or add a Ceramic/Exa/Linkup key with
  alias `default` under AI Gateway → Provider Keys.
- `HTTP 401` on Brave/Tavily — wrong or revoked key; refill the vault slug.
- `free_quota_exhausted` right after setup — both free keys are missing; only
  Cloudflare was tried and it is not configured either.
- Reset the local counters for testing: delete `~/.open-bot/web-search/usage.json`.
