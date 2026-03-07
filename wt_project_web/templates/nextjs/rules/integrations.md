---
paths:
  - "src/lib/billing/**"
  - "src/lib/llm/**"
  - "src/lib/research/**"
  - "src/app/api/webhooks/**"
  - "src/app/api/stripe/**"
  - "src/app/api/billing/**"
---

# External Integrations

## Webhook Handling
- Webhook endpoints SHALL be idempotent — store event ID in a unique column, skip duplicates
- Log all webhook events to a dedicated table before processing
- Key lifecycle events (subscription created/updated/deleted, payment success/failure) SHALL update local state synchronously

## Provider Patterns
- Use lazy singletons for API clients — initialize on first use, not at import
- Primary + fallback pattern: define a primary provider and a fallback (e.g., Anthropic primary, OpenAI fallback)
- NEVER expose provider-internal env vars or API keys in client-side code or logs

## Retry & Backoff
- External API calls SHALL use retry with exponential backoff (3x default)
- Set reasonable timeouts — don't let external calls block indefinitely
- Circuit breaker: disable flaky sources in production, enable via feature flag

## Rate Limiting
- Respect upstream rate limits — implement per-source rate limiters
- Health check external services before use when startup cost is high
- Log rate limit hits for monitoring

## Scraping / Enrichment
- Fetch first, fall back to headless browser if content is insufficient
- Abstract source names — never show raw source identifiers in UI
- Cache enrichment results with TTL to avoid redundant calls
