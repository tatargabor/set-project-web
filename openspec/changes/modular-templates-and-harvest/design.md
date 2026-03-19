## Context

`deploy_templates()` in set-project-base currently walks the entire template directory and copies all files. There's no concept of "optional" — every file in the template goes to every project.

Production projects accumulate domain-specific rules (GDPR, integrations, email) that are valuable to generalize, but pushing them into the template means all projects get them. We need a selection layer.

## Goals / Non-Goals

**Goals:**
- Template authors can mark rules as core (always) or optional (opt-in)
- Users select modules during `wt-project init` (interactive or `--modules` flag)
- Selected modules are tracked so `init` re-runs deploy the same set
- Harvest skill lets users pull production rules back into templates as optional modules
- Backward compatible: templates without manifest.yaml behave exactly as before (all files deployed)

**Non-Goals:**
- Module dependencies (module A requires module B) — keep it flat for now
- Automatic harvest without user review — always confirm
- Module versioning or update tracking

## Decisions

### D1: manifest.yaml format

```yaml
core:
  - project-knowledge.yaml
  - rules/ui-conventions.md
  - rules/functional-conventions.md
  - rules/auth-conventions.md
  - rules/data-model.md
  - rules/deployment.md

modules:
  gdpr:
    description: "GDPR retention, suppression, data export"
    files:
      - rules/data-privacy.md
  integrations:
    description: "External API patterns (webhooks, retry, rate limiting)"
    files:
      - rules/integrations.md
```

When `manifest.yaml` is absent, all files are treated as core (backward compat).

### D2: Module selection flow

CLI path:
```
wt-project init --project-type web --template nextjs --modules gdpr,integrations
```

Interactive path (when `--modules` not specified and optional modules exist):
```
Core rules: 6 files
Optional modules:
  [x] gdpr          — GDPR retention, suppression, data export
  [ ] integrations   — External API patterns
Select with space, enter to confirm:
```

Since `wt-project init` is a bash script without TUI, the interactive path prints the available modules and asks for comma-separated input.

### D3: Module tracking

Selected modules stored in `set/plugins/project-type.yaml`:
```yaml
type: web
version: 0.1.0
template: nextjs
modules:
  - gdpr
  - integrations
```

On re-init, `deploy_templates()` reads this and deploys core + tracked modules. New modules added to the template show up as "Available" on next init.

### D4: Harvest is a skill, not a CLI command

Harvest requires AI to:
- Read and understand rules content
- Classify as base/web/skip
- Strip project-specific paths and names
- Write generalized version

This is a `/wt:harvest` skill that runs in a Claude session. It:
1. Takes `--from <project-path>` as argument
2. Diffs source project's `.claude/rules/` against template
3. For each candidate: reads content, classifies, proposes generalization
4. Shows summary, user approves/edits
5. Writes approved files into the template repo as optional modules
6. Updates manifest.yaml

### D5: deploy_templates changes

The `deploy_templates()` function gains an optional `modules` parameter (list of module IDs). Resolution:
1. If manifest.yaml exists → deploy core + requested modules
2. If manifest.yaml absent → deploy all files (backward compat)
3. Unknown module ID → warning, skip

## Risks / Trade-offs

- [Manifest out of sync with actual files] → Validate manifest references exist at deploy time, warn on orphans
- [Harvest quality depends on AI] → Always show diff for human review, never auto-merge
- [Interactive selection in bash is clunky] → Keep it simple (comma-separated input), upgrade to TUI later if needed
