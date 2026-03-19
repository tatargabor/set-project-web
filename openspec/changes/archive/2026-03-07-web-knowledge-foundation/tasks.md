## 1. Project Structure and Base Configuration

- [x] 1.1 Create the `set-project-web` Python package structure (`pyproject.toml`, `set_project_web/__init__.py`, entry point registration under `set_tools.project_types`)
- [x] 1.2 Define the `ProjectType` base class interface in a shared module — `info`, `get_templates()`, `get_verification_rules()`, `get_orchestration_directives()` methods
- [x] 1.3 Implement `WebProjectType` class that extends `ProjectType` with web-specific template discovery
- [x] 1.4 Create the `wt-project init --type <type>` CLI command that scaffolds files from a template into the consumer project

## 2. Next.js App Router Template

- [x] 2.1 Create `templates/nextjs/project-knowledge.yaml` — cross-cutting file registry (sidebar, i18n, route labels, DB schema, design docs) and feature registry (auth, email, copilot, etc.) with path patterns for Next.js App Router
- [x] 2.2 Create `templates/nextjs/rules/functional-conventions.md` — server actions, DB patterns (Prisma tenant scoping, singleton client), form patterns (Pattern A dialog, Pattern B toggle), revalidatePath, logActivity
- [x] 2.3 Create `templates/nextjs/rules/ui-conventions.md` — shadcn/ui stack, layout patterns, button variant policy (ghost = icon-only), table conventions, dialog patterns, i18n mandatory rules
- [x] 2.4 Create `templates/nextjs/rules/auth-conventions.md` — role hierarchy, centralized role checking helpers, impersonation patterns, platform admin separation
- [x] 2.5 Create `templates/nextjs/rules/data-model.md` — Prisma conventions (cuid IDs, snake_case mapping, tenant-scoped models, polymorphic entities, state machines)
- [x] 2.6 Create `templates/nextjs/rules/deployment.md` — migration-first deploy, port allocation, Docker patterns, dev server configuration

## 3. Generic SPA Template

- [x] 3.1 Create `templates/spa/project-knowledge.yaml` — minimal cross-cutting file registry (router config, i18n, API client) with explanatory comments for customization
- [x] 3.2 Create `templates/spa/rules/components.md` — generic component conventions (file size, naming, state management placeholder)

## 4. Verification Rules Engine

- [x] 4.1 Create `verification-rules/i18n-completeness.yaml` — cross-file-key-parity check definition for JSON locale files with nested key dot-path comparison
- [x] 4.2 Create `verification-rules/route-registered.yaml` — file-mentions check that new page files are referenced in navigation config, with exclusion patterns for API/auth routes
- [x] 4.3 Create `verification-rules/cross-cutting-consistency.yaml` — cross-reference check between sidebar items, route labels, and i18n keys
- [x] 4.4 Create `verification-rules/migration-safety.yaml` — schema-migration-sync check for Prisma migration patterns
- [x] 4.5 Create `verification-rules/component-conventions.yaml` — file-line-count and pattern-absence checks (file size limit, button variant policy)
- [x] 4.6 Document the verification rule YAML schema (check types, severity levels, ignore lists, consumer override mechanism)

## 5. Orchestration Directives

- [x] 5.1 Create `directives/i18n-serialization.yaml` — no-parallel-i18n and consolidate-i18n directives
- [x] 5.2 Create `directives/post-merge.yaml` — conditional post-merge commands (db:generate on schema change, install on package.json change)
- [x] 5.3 Create `directives/smoke-test.yaml` — smoke test configuration template with timeout, env, fix_timeout, retry settings
- [x] 5.4 Create `directives/cross-cutting-review.yaml` — flag-for-review directive for cross-cutting file changes
- [x] 5.5 Create `directives/context-efficiency.yaml` — guidelines for CLAUDE.md vs .claude/rules/ separation, context window budget rules

## 6. Documentation

- [x] 6.1 Write `docs/plugin-architecture.md` — explains the three-layer hierarchy (base → domain → custom), discovery mechanism, extends/override model, and how to create a custom project type
- [x] 6.2 Write `docs/template-reference.md` — documents all template files, their sections, and customization points
- [x] 6.3 Write `docs/verification-rules-reference.md` — documents all check types, severity levels, ignore lists, and how to add custom rules
- [x] 6.4 Update `README.md` with project overview, quick start, and link to docs
