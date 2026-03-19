## Why

The set-core orchestration system is project-type-agnostic — it knows how to manage worktrees, run OpenSpec workflows, and coordinate agents, but has no understanding of the project it's operating on. When orchestrating a Next.js app vs a Python CLI tool, the same mistakes repeat: missing i18n keys, unregistered routes, sidebar items without translations, DB migrations without design doc updates. These are predictable, domain-specific verification gaps that a knowledge plugin could catch automatically.

Real-world orchestration runs (10+ cycles across a production Next.js SaaS) have proven that 30-40% of wasted iterations come from domain-specific oversights that generic tooling can't prevent. A layered project-knowledge plugin system would eliminate these.

## What Changes

- Define the **wt-project plugin architecture** — a layered system where `set-project-base` provides common rules and `set-project-web` extends it with web-specific knowledge
- Extract and generalize web-specific patterns from production Next.js projects into reusable templates and verification rules
- Create a **project-knowledge.yaml template** system for web projects — cross-cutting file registry, feature registry, verification checklists
- Define **web-specific verification rules** that the orchestrator can enforce during `opsx:verify`
- Establish the **custom project type** extension point so organizations can create their own `wt-project-*` plugins

## Capabilities

### New Capabilities

- `project-plugin-architecture`: Defines the layered plugin system — base vs domain-specific vs custom. How plugins are discovered, loaded, composed. Inheritance model (web extends base). Entry points, configuration, and the interface contract between set-core core and project plugins.

- `web-knowledge-templates`: Template library for web project configuration. Includes `project-knowledge.yaml` templates for Next.js (App Router) and a generic SPA scaffold. Templates cover: cross-cutting file registry (sidebar, i18n, route config, DB schema), feature registry pattern, and the `.claude/rules/` file structure with path-scoped activation.

- `web-verification-rules`: Web-specific verification rules that run during `opsx:verify` and post-merge checks. Rules include: i18n completeness (all UI strings in all locale files), route registration (new pages registered in sidebar/nav config), cross-cutting file consistency (sidebar items match route definitions match i18n keys), DB migration safety (migration before deploy, design doc updated), and component conventions (button variants, file size limits).

- `web-orchestration-directives`: Web-aware orchestration directives and guardrails. Includes: never parallelize i18n changes with UI-label changes, large i18n migrations as single change, smoke test configuration templates, post-merge commands (e.g., `db:generate`), and the `.claude/rules/` pattern for context-efficient convention loading.

### Modified Capabilities

_(none — this is a new project, no existing specs)_

## Impact

- **set-core core**: Will need a plugin loading interface (already has `wt_tools/plugins/base.py` — this defines the project-knowledge plugin contract that extends it)
- **Consumer projects** (sales-raketa, future webshops): Will be able to `wt-project init --type web-nextjs` to scaffold project-knowledge config, `.claude/rules/`, and verification rules
- **OpenSpec verification**: `opsx:verify` gains web-specific checks when `set-project-web` is active
- **Orchestration**: Sentinel gains domain-aware directives (e.g., "don't parallelize i18n changes")
- **Third-party extensibility**: Organizations can create `wt-project-{name}` packages that register via Python entry points, same as existing set-core plugin system
