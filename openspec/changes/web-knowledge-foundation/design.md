## Context

The wt-tools ecosystem orchestrates AI-driven parallel development across git worktrees. It is project-type-agnostic — it manages worktrees, OpenSpec workflows, and agent coordination but has zero domain knowledge about what kind of project it's operating on.

Production experience with a Next.js SaaS application (10+ orchestration cycles, 50+ changes merged) has revealed recurring failure patterns that are predictable and preventable with domain-specific knowledge:

- **i18n drift**: New UI added without translation keys in all locale files (30% of verify failures)
- **Route orphans**: New pages created without sidebar/navigation registration
- **Cross-cutting inconsistency**: Sidebar items, route definitions, and i18n keys out of sync
- **Migration ordering**: DB schema changes deployed before migrations run
- **Convention violations**: Wrong button variants, oversized files, direct SDK calls instead of wrappers

These are not bugs in wt-tools — they are gaps in domain knowledge. A project-knowledge plugin system fills these gaps.

Currently, this knowledge lives as ad-hoc `.claude/rules/` files and CLAUDE.md sections in each consumer project. There is no standardization, no template system, and no way to share learnings across projects.

## Goals / Non-Goals

**Goals:**
- Define a layered project-knowledge plugin architecture (`base` → `domain` → `custom`)
- Extract and generalize web-specific patterns into reusable templates
- Create `project-knowledge.yaml` template system for web frameworks (Next.js, generic SPA)
- Define web-specific verification rules enforceable during `opsx:verify`
- Establish orchestration directives that prevent known conflict patterns
- Design the extension point for third-party/organization-specific project types

**Non-Goals:**
- Implementing the wt-tools core plugin loader changes (that happens in wt-tools repo)
- Runtime code execution or linting — this is knowledge/configuration, not tooling
- Framework-specific code generators (e.g., scaffolding Next.js components)
- Replacing existing `.claude/rules/` mechanism — we build on top of it

## Decisions

### 1. Three-layer plugin hierarchy

```
wt-project-base          (common to all software projects)
  ├── wt-project-web      (web applications: i18n, routing, DB, components)
  ├── wt-project-mobile   (future: mobile apps)
  ├── wt-project-cli      (future: CLI tools)
  └── wt-project-custom   (organization-specific extensions)
```

**Rationale**: A flat plugin system would lead to duplication (every web plugin re-defining "max 400 lines per file"). Inheritance lets domain plugins focus only on domain-specific rules while inheriting universal best practices from base.

**Alternative considered**: Single monolithic knowledge file per project type → rejected because it doesn't compose (a Next.js project with Stripe needs web + payments knowledge).

### 2. Configuration-driven, not code-driven

Project knowledge is expressed as YAML configuration and Markdown templates, not Python code. The plugin system provides:
- `project-knowledge.yaml` — cross-cutting file registry, feature registry
- `.claude/rules/*.md` — path-scoped convention files with frontmatter
- `verification-rules.yaml` — declarative verification checks
- `orchestration-directives.yaml` — orchestration guardrails

**Rationale**: Consumer projects are typically JS/TS. Requiring Python knowledge to customize project rules creates an unnecessary barrier. YAML/Markdown is universally editable.

**Alternative considered**: Python plugin classes with `verify()` methods → rejected for the barrier reason above, but the wt-tools plugin base class (`Plugin`) remains the delivery mechanism.

### 3. Template inheritance via `extends` field

```yaml
# project-knowledge.yaml in a consumer project
extends: wt-project-web/nextjs
# overrides and additions below...
```

**Rationale**: Consumer projects need to customize templates (different sidebar structure, additional locale files) without forking the entire template. The `extends` mechanism lets them override specific sections while inheriting the rest.

### 4. Verification rules as declarative YAML

```yaml
rules:
  - id: i18n-completeness
    description: All UI strings must exist in all locale files
    check: cross-file-key-parity
    files:
      - pattern: "messages/*.json"
    severity: error

  - id: route-registered
    description: New page routes must be registered in navigation config
    check: file-mentions
    source: "src/app/**/page.tsx"
    target: navigation-config  # resolved from cross-cutting registry
    severity: warning
```

**Rationale**: Declarative rules are inspectable, composable, and don't require a runtime. The verification engine in wt-tools interprets them — the plugin only provides the rule definitions.

**Alternative considered**: Bash scripts per check → rejected because they're not composable and hard to override in consumer projects.

### 5. Orchestration directives as named guardrails

```yaml
directives:
  - id: no-parallel-i18n
    description: Never parallelize i18n changes with UI-label changes
    trigger: change-has-tag("i18n")
    action: serialize-with-tag("ui-labels")

  - id: single-i18n-migration
    description: Large i18n migrations should be a single change, not split
    trigger: change-modifies("messages/*.json") AND change-count > 1
    action: warn("Consider merging i18n changes into a single change")
```

**Rationale**: Production experience showed that i18n merge conflicts wasted 2.5+ hours in a single orchestration run. Declarative directives let the orchestrator prevent these patterns without hard-coding them in wt-tools core.

### 6. Delivery via `wt-project init`

```bash
wt-project init --type web-nextjs
# Creates:
#   project-knowledge.yaml (from template)
#   .claude/rules/*.md (path-scoped conventions)
#   verification-rules.yaml
#   orchestration-directives.yaml (merged into orchestration.yaml)
```

**Rationale**: One command to bootstrap all project-knowledge files. The init command reads templates from the installed plugin package and writes them to the consumer project, where they can be customized.

## Risks / Trade-offs

**[Over-generalization]** → Templates derived from a single production project may not fit all web projects.
*Mitigation*: Templates are starting points with clear override mechanisms. Document which parts are opinionated vs universal.

**[Template drift]** → Consumer project customizes templates, then upstream template improves — no merge path.
*Mitigation*: `extends` mechanism with explicit overrides. Future: `wt-project update` command that shows diffs.

**[Verification false positives]** → Rules may flag legitimate exceptions (e.g., a page that intentionally has no sidebar entry).
*Mitigation*: Per-rule `ignore` lists in `verification-rules.yaml`. Severity levels (error vs warning).

**[Plugin dependency on wt-tools changes]** → The plugin architecture needs wt-tools core to support project-knowledge plugins.
*Mitigation*: Phase 1 deliverables (templates, rules files, documentation) are usable immediately as static files. Plugin loading integration is Phase 2.

## Open Questions

1. **Should `wt-project-base` live in its own repo or inside wt-tools?** — Leaning toward wt-tools (it's small and tightly coupled to core), but domain plugins (web, mobile) should be separate repos.

2. **How do verification rules interact with existing smoke tests?** — Verification rules run during `opsx:verify` (pre-merge), smoke tests run post-merge. They complement each other but the boundary needs to be clear.

3. **Should the `.claude/rules/` path patterns be part of the template or generated from `project-knowledge.yaml`?** — Generating them would ensure consistency but adds complexity. Starting with templates seems simpler.
