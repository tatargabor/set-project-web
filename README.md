# wt-project-web

Web project type plugin for [wt-tools](https://github.com/tatargabor/wt-tools). Provides web-specific verification rules, orchestration directives, and project templates on top of [wt-project-base](https://github.com/tatargabor/wt-project-base).

> **Status:** Experimental / active development. I built this for my own AI-assisted web projects and am sharing it as a possible direction for others. The conventions reflect my preferences and what I've found works well with AI agents — your mileage may vary. Contributions, forks, and feedback are welcome.

## Why Not Just Use a Smart Agent?

A capable model like Claude already knows SEO best practices, accessibility standards, and security conventions. So why encode them in rule files?

**Consistency across agents.** When an orchestrator runs 5 agents in parallel on different features, each agent makes independent decisions. One might use `next/image`, another writes raw `<img>` tags. One adds `generateMetadata`, another forgets. The rules create a shared standard that every agent follows, regardless of which change it's working on.

**Context window efficiency.** Stuffing all conventions into CLAUDE.md wastes tokens on every turn — UI rules load when the agent is editing a Prisma migration. Path-scoped rules (`paths:` frontmatter) load only when the agent touches relevant files. An agent working on `prisma/schema.prisma` sees data-model conventions; an agent working on `src/components/` sees UI conventions. Neither wastes context on the other's domain.

**Persistence across sessions.** An agent might know to add error boundaries — but will it remember on session 47 of iterative development? Rules survive session boundaries. They apply equally to the first feature and the fiftieth bug fix.

**Orchestration coordination.** Individual agent knowledge can't prevent merge conflicts. When two agents both modify `messages/en.json`, rules can serialize those changes. When a schema change merges, rules can trigger `prisma generate` automatically. This is coordination logic, not domain knowledge — agents can't infer it from training data.

**Verification at merge time.** Knowing a convention and enforcing it are different things. Verification rules catch what agents miss under pressure — an `error` severity rule blocks the merge, a `warning` flags it for review. This is a safety net, not a substitute for agent capability.

## What Problem It Solves

When an orchestrator (like wt-tools) spins up multiple AI agents to build a web application in parallel, each agent needs to know:

- **What conventions to follow** — path-scoped rule files activate only when the agent touches relevant files
- **What to verify before merging** — automated checks catch missing alt text, unsynced locale files, or schema changes without migrations
- **How to coordinate** — directives prevent merge conflicts (serialize i18n changes), trigger post-merge commands (regenerate Prisma client), and flag cross-cutting modifications for review

## Design Principles

- **Generic, not project-specific** — covers universal modern web standards (SEO, a11y, security, performance). No e-commerce logic, no business rules, no framework opinions beyond the chosen template
- **Path-scoped activation** — rules load only when relevant files are touched, keeping the agent's context window efficient
- **Layered inheritance** — base → web → organization-specific. Override or disable any rule without forking
- **Customizable without forking** — disable rules you disagree with, override severities, add your own conventions via YAML, or build a layer on top (e.g., `wt-project-your-org`) that inherits everything and adds organization-specific rules

## Current State

The `nextjs` template provides conventions covering 12 areas of modern web development: UI, functional patterns, auth, data model, deployment, testing, integrations, SEO, accessibility, performance, security, and error handling. These conventions are based on real-world usage with AI agents and reflect patterns that have proven to reduce common mistakes.

The `spa` template is a minimal starting point for other frameworks (React SPA, Vue, Svelte) — it provides the structure but expects projects to fill in framework-specific conventions.

**Designed for iterative development.** The conventions work for the initial build and for ongoing development on the same codebase. Agents pick up the rules on every change — bug fixes, refactors, and new features all get the same guardrails. This is not a one-shot scaffolding tool; it's a living knowledge layer that stays relevant as the project evolves.

## What's NOT Included (Yet)

This plugin currently covers **development-time conventions** — what agents should know while writing and reviewing code. It does **not** yet handle:

- **Production deployment** — CI/CD pipelines, Docker images, cloud platform setup (Vercel, AWS, etc.)
- **Infrastructure** — database provisioning, CDN configuration, monitoring dashboards
- **Runtime operations & maintenance** — log aggregation, alerting, on-call setup, dependency updates

The deployment.md rule file covers deployment *conventions* (migration-first deploys, health checks, env var hygiene), but the actual deployment automation and production maintenance workflows are planned for future versions.

## Roadmap

Near-term:
- **Deployment integration** — CI/CD templates, Docker configs, and platform-specific deploy rules as opt-in modules
- **Template modules** — opt-in convention packs (e.g., `email`, `payments`, `cms`) that add domain-specific rules without bloating the core template
- **Feedback loop** — agents report which rules triggered, which were useful, and which produced false positives, feeding back into rule refinement

Longer-term:
- **More templates** — Remix, Astro, and framework-agnostic API-only templates
- **Rule auto-fix** — verification rules that can suggest or apply fixes, not just flag violations
- **Consumer override UX** — simpler YAML-based customization for per-project rule tuning
- **Runtime conventions** — observability, structured logging, and error tracking patterns as opt-in modules

## Quick Start

```bash
# Install
pip install wt-project-web

# Initialize a Next.js project
wt-project-web init --type nextjs --target /path/to/project

# List available templates
wt-project-web list
```

## What It Provides

### Templates
- **Next.js App Router** (`nextjs`) — Full-stack Next.js with Prisma, next-intl, shadcn/ui
- **Generic SPA** (`spa`) — Minimal starting point for any SPA framework

### Convention Rules (12 path-scoped rule files)

| Rule File | Covers |
|-----------|--------|
| `ui-conventions` | shadcn/ui, responsive breakpoints, toast, skeleton, empty states |
| `functional-conventions` | Server actions, API route handlers, Prisma, multi-step forms |
| `auth-conventions` | NextAuth v5, roles, middleware, bcrypt |
| `data-model` | Prisma schema, migrations, seeding, state machines |
| `deployment` | Migration-first deploy, health check, env var documentation |
| `testing-conventions` | Testing diamond, Playwright E2E, cold-visit tests, port isolation |
| `integrations` | Webhooks, API clients, retry with backoff |
| `seo-conventions` | Metadata, Open Graph, JSON-LD, sitemap, robots, canonical/hreflang |
| `accessibility` | WCAG 2.1 AA, semantic HTML, ARIA, focus, contrast, reduced motion |
| `performance` | Core Web Vitals, next/image, next/font, caching, bundle hygiene |
| `security` | CSP, HSTS, CORS, rate limiting, input validation, NEXT_PUBLIC_ safety |
| `error-handling` | Error boundaries, not-found pages, loading states, global-error |

### Verification Rules (11 web-specific)

| Rule | Severity | Check |
|------|----------|-------|
| `i18n-completeness` | error | All locale files must have the same keys |
| `route-registered` | warning | New pages should appear in navigation |
| `cross-cutting-consistency` | warning | Sidebar, routes, and i18n stay in sync |
| `migration-safety` | error | Schema changes need migration files |
| `ghost-button-text` | warning | Ghost buttons must be icon-only |
| `functional-test-coverage` | warning | Feature changes need Playwright tests |
| `page-metadata` | warning | Public pages must export metadata for SEO |
| `image-alt-text` | warning | Images must have alt text for accessibility |
| `env-example-sync` | warning | New env vars must be in .env.example |
| `error-boundary-exists` | warning | App must have error.tsx, global-error.tsx, not-found.tsx |
| `no-public-secrets` | error | NEXT_PUBLIC_ must not prefix secret-like vars |

Plus base rules from `wt-project-base` (file-size-limit, no-secrets-in-source, todo-tracking).

### Orchestration Directives (7 web-specific)

| Directive | Action | Trigger |
|-----------|--------|---------|
| `no-parallel-i18n` | serialize | Changes modifying locale files |
| `consolidate-i18n` | warn | Multiple changes touch locale files |
| `db-generate` | post-merge | Schema changes → `pnpm db:generate` |
| `db-seed` | post-merge | Schema changes → `pnpm db:seed` |
| `cross-cutting-review` | flag-for-review | Cross-cutting file modifications |
| `playwright-setup` | warn | First Playwright test file created |
| `env-example-review` | flag-for-review | .env.example modifications |

Plus base directives from `wt-project-base` (install-deps, no-parallel-lockfile, config-review).

## Plugin Architecture

```
wt-project-base          Universal rules (file size, secrets, TODOs)
  └── wt-project-web      Web domain rules (i18n, routing, DB, components)
        └── your-org-web   Organization-specific rules (your conventions)
```

Each layer inherits from its parent. Customize via `wt/plugins/project-type.yaml` without writing Python.

## Documentation

- [Plugin Architecture](docs/plugin-architecture.md) — Three-layer hierarchy and customization
- [Template Reference](docs/template-reference.md) — Template files and sections
- [Verification Rules Reference](docs/verification-rules-reference.md) — All rules with check types
