# set-project-web

Web project type plugin for [set-core](https://github.com/tatargabor/set-core). Provides web-specific verification rules, orchestration directives, design integration, and project templates on top of [set-project-base](https://github.com/tatargabor/set-project-base).

> **Status:** Experimental / active development. Built for AI-assisted web projects and shared as a direction for others. The conventions reflect real-world production usage with AI agents across multiple projects. Contributions, forks, and feedback are welcome.

## Why Not Just Use a Smart Agent?

A capable model like Claude already knows SEO best practices, accessibility standards, and security conventions. So why encode them in rule files?

**Consistency across agents.** When an orchestrator runs 5 agents in parallel on different features, each agent makes independent decisions. One might use `next/image`, another writes raw `<img>` tags. The rules create a shared standard that every agent follows.

**Context window efficiency.** Stuffing all conventions into CLAUDE.md wastes tokens on every turn. Path-scoped rules (`paths:` frontmatter) load only when the agent touches relevant files. An agent working on `prisma/schema.prisma` sees data-model conventions; an agent working on `src/components/` sees UI conventions.

**Persistence across sessions.** An agent might know to add error boundaries — but will it remember on session 47? Rules survive session boundaries and apply equally to the first feature and the fiftieth bug fix.

**Orchestration coordination.** Individual agent knowledge can't prevent merge conflicts. When two agents both modify `messages/en.json`, rules serialize those changes. When a schema change merges, rules trigger `prisma generate` automatically.

**Verification at merge time.** Knowing a convention and enforcing it are different. Verification rules catch what agents miss — an `error` severity rule blocks the merge, a `warning` flags it for review.

## What Problem It Solves

When an orchestrator (like set-core) spins up multiple AI agents to build a web application in parallel, each agent needs to know:

- **What conventions to follow** — path-scoped rule files activate only when the agent touches relevant files
- **What to verify before merging** — automated checks catch missing alt text, unsynced locale files, or schema changes without migrations
- **How to coordinate** — directives prevent merge conflicts (serialize i18n changes), trigger post-merge commands (regenerate Prisma client), and flag cross-cutting modifications for review
- **How to match the design** — design integration rules guide agents to use Figma source files and design tokens instead of guessing

## What It Provides

### Templates

- **Next.js App Router** (`nextjs`) — Full-stack Next.js with Prisma, next-intl, shadcn/ui, Figma design integration
- **Generic SPA** (`spa`) — Minimal starting point for any SPA framework

### Convention Rules (13 path-scoped rule files)

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
| `design-integration` | Figma source files, design token mapping, component hierarchy |

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

Plus base rules from `set-project-base` (file-size-limit, no-secrets-in-source, todo-tracking).

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

Plus base directives from `set-project-base` (install-deps, no-parallel-lockfile, config-review).

### Gate Overrides (per-change-type verification)

Different change types get different quality gate configurations:

| Change Type | Override | Rationale |
|-------------|----------|-----------|
| `foundational` | E2E required, smoke warn-only | Infrastructure setup needs full E2E but smoke failures are expected |
| `schema` | Test files not required | Database schema changes may not need their own test files |
| `cleanup-after` | Smoke warn-only | Cleanup changes shouldn't block on smoke |

### Design Integration

The `design-integration.md` rule and Figma support enable design-driven development:

- **Figma source files** in `docs/figma-raw/` — component hierarchy, mock data, icon usage
- **Design tokens** mapped to `tailwind.config.ts` — colors, spacing, typography, radius
- **Component mapping** to shadcn/ui — design components mapped to implementation primitives
- **Automatic setup** — `set-project-web init --type nextjs` prompts for Figma file URL and registers the MCP server

### Engine Integration (Profile Methods)

These methods are called by the set-core orchestration engine:

| Method | What it does |
|--------|-------------|
| `detect_package_manager()` | Checks lockfiles (pnpm → yarn → npm → bun) |
| `detect_test_command()` | Reads package.json for `test`, `test:unit`, `test:ci` |
| `detect_build_command()` | Reads package.json for `build:ci` or `build` |
| `detect_dev_server()` | Reads package.json for `dev` script |
| `bootstrap_worktree()` | `npm install` + `prisma generate` + `playwright install` |
| `post_merge_install()` | `npm install` after merge |
| `security_rules_paths()` | Returns paths to `security.md`, `auth-conventions.md` |
| `security_checklist()` | IDOR, auth middleware, input validation, data scoping, XSS |
| `generated_file_patterns()` | `next-env.d.ts`, `.next/`, `dist/`, `build/`, `.turbo/` |
| `ignore_patterns()` | `node_modules`, `.next`, `dist`, `build`, `.turbo` |
| `gate_overrides(change_type)` | Per-change-type verify gate configuration |

## Quick Start

```bash
# Install
pip install set-project-web

# Initialize a Next.js project (with optional Figma setup)
set-project-web init --type nextjs --target /path/to/project

# List available templates
set-project-web list
```

## Design Principles

- **Generic, not project-specific** — covers universal modern web standards (SEO, a11y, security, performance). No e-commerce logic, no business rules, no framework opinions beyond the chosen template
- **Path-scoped activation** — rules load only when relevant files are touched, keeping the agent's context window efficient
- **Layered inheritance** — base → web → organization-specific. Override or disable any rule without forking
- **Customizable without forking** — disable rules, override severities, add conventions via YAML, or build a layer on top

## Plugin Architecture

```
set-project-base          Universal rules (file size, secrets, TODOs)
  └── set-project-web      Web domain rules (i18n, routing, DB, components, design)
        └── your-org-web   Organization-specific rules (your conventions)
```

Each layer inherits from its parent. Customize via `set/plugins/project-type.yaml` without writing Python.

## What's NOT Included (Yet)

This plugin currently covers **development-time conventions** — what agents should know while writing and reviewing code. It does **not** yet handle:

- **Production deployment** — CI/CD pipelines, Docker images, cloud platform setup
- **Infrastructure** — database provisioning, CDN configuration, monitoring dashboards
- **Runtime operations** — log aggregation, alerting, on-call setup, dependency updates

## Roadmap

Near-term:
- **Deployment integration** — CI/CD templates, Docker configs, and platform-specific deploy rules as opt-in modules
- **Template modules** — opt-in convention packs (e.g., `email`, `payments`, `cms`)
- **Feedback loop** — agents report which rules triggered and which produced false positives

Longer-term:
- **More templates** — Remix, Astro, and framework-agnostic API-only templates
- **Rule auto-fix** — verification rules that can suggest or apply fixes
- **Runtime conventions** — observability, structured logging, and error tracking patterns

## Documentation

- [Plugin Architecture](docs/plugin-architecture.md) — Three-layer hierarchy and customization
- [Template Reference](docs/template-reference.md) — Template files and sections
- [Verification Rules Reference](docs/verification-rules-reference.md) — All rules with check types and YAML schema

## Related

- [set-core](https://github.com/tatargabor/set-core) — The orchestration engine that consumes project type plugins
- [set-project-base](https://github.com/tatargabor/set-project-base) — Abstract base layer with ProjectType ABC and universal rules

## License

MIT
