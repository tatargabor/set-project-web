# wt-project-web

Web project type plugin for [wt-tools](https://github.com/anthropics/wt-tools). Provides web-specific verification rules, orchestration directives, and project templates on top of [wt-project-base](https://github.com/anthropics/wt-project-base).

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

### Verification Rules
- `i18n-completeness` — All locale files must have the same keys
- `route-registered` — New pages should appear in navigation
- `cross-cutting-consistency` — Sidebar, routes, and i18n stay in sync
- `migration-safety` — Schema changes need migration files
- `ghost-button-text` — Ghost buttons must be icon-only

Plus all base rules from `wt-project-base` (file-size-limit, no-secrets-in-source, todo-tracking).

### Orchestration Directives
- i18n serialization and consolidation
- Post-merge conditional commands (db:generate, install)
- Cross-cutting file review flags
- Context efficiency guidelines

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
