# wt-project-web

Web project type plugin for [wt-tools](https://github.com/tatargabor/wt-tools). Provides web-specific verification rules, orchestration directives, and project templates on top of [wt-project-base](https://github.com/tatargabor/wt-project-base).

> **Status:** Experimental / active development. I built this for my own AI-assisted web projects and am sharing it as a possible direction for others. The conventions reflect my preferences and what I've found works well with AI agents — your mileage may vary. Contributions, forks, and feedback are welcome.

## Why This Exists

AI agents building web applications make predictable mistakes: they forget SEO metadata, skip error boundaries, expose secrets via `NEXT_PUBLIC_`, write inaccessible markup, and create i18n merge conflicts when working in parallel. These aren't edge cases — they happen on every non-trivial project.

**wt-project-web** encodes modern web development standards as machine-readable rules, so agents get it right the first time without needing project-specific instructions for universal concerns.

The plugin is designed to be **customizable without forking** — disable rules you disagree with, override severities, add your own conventions via YAML, or build a layer on top (e.g., `wt-project-your-org`) that inherits everything and adds organization-specific rules.

## What Problem It Solves

When an orchestrator (like wt-tools) spins up multiple AI agents to build a web application in parallel, each agent needs to know:

- **What conventions to follow** — path-scoped rule files activate only when the agent touches relevant files (editing a component triggers UI conventions, not deployment rules)
- **What to verify before merging** — automated checks catch missing alt text, unsynced locale files, or schema changes without migrations
- **How to coordinate** — directives prevent merge conflicts (serialize i18n changes), trigger post-merge commands (regenerate Prisma client), and flag cross-cutting modifications for review

Without this, every project needs a massive CLAUDE.md stuffed with web conventions. With it, `wt-project init --project-type web --template nextjs` sets up all conventions automatically.

## Design Principles

- **Generic, not project-specific** — covers universal modern web standards (SEO, a11y, security, performance). No e-commerce logic, no business rules, no framework opinions beyond the chosen template
- **Path-scoped activation** — rules load only when relevant files are touched, keeping the agent's context window efficient
- **Layered inheritance** — base → web → organization-specific. Override or disable any rule without forking
- **Convention over configuration** — sensible defaults that work for 90% of Next.js projects. Customize the remaining 10% via YAML overrides

## Current State

Production-ready for Next.js App Router projects. The `nextjs` template provides a complete set of conventions covering 12 areas of modern web development: UI, functional patterns, auth, data model, deployment, testing, integrations, SEO, accessibility, performance, security, and error handling.

The `spa` template is a minimal starting point for other frameworks (React SPA, Vue, Svelte) — it provides the structure but expects projects to fill in framework-specific conventions.

**Not just for greenfield projects.** The conventions are designed for iterative development with wt-tools — you can use them for the initial build and then keep building on the same codebase with the same rules. Agents pick up the conventions on every change, whether it's the first feature or the fiftieth. This means bug fixes, refactors, and new features all get the same quality guardrails automatically.

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
