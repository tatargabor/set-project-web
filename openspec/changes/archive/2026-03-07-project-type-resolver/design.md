## Context

set-project-base defines `ProjectType` ABC and `BaseProjectType`. set-project-web extends it with `WebProjectType`. Companies install these packages and run `wt-project init --project-type web` which writes `set/plugins/project-type.yaml`.

Currently the YAML only stores metadata (type name, version). Rules and directives come exclusively from the Python package — no local customization possible without forking.

The resolver and feedback system both live in **set-project-base** because they're universal — any project type (base, web, future custom types) needs them.

We work from **set-project-web** repo but the code goes into `/home/tg/code2/set-project-base/`.

## Goals / Non-Goals

**Goals:**
- Companies can add, disable, and override rules/directives via YAML without touching Python packages
- Structured feedback format that's anonymized by design (rule_id-based, no project/company names)
- `feedback export` CLI produces shareable YAML for upstream improvements
- `resolve` CLI shows the final merged ruleset for debugging
- Backward compatible — existing `project-type.yaml` files work unchanged

**Non-Goals:**
- Telemetry / automatic feedback submission (future, opt-in)
- Rule execution engine (opsx:verify runs rules, resolver just provides the list)
- GUI for rule management
- Directive execution engine (sentinel uses directives, resolver provides them)

## Decisions

### D1: Resolver lives in set-project-base, not set-core

**Choice**: `set_project_base/resolver.py`

**Why**: The resolver needs to import `ProjectType`, `VerificationRule`, etc. These are Python classes in set-project-base. Keeping resolver in the same package avoids circular dependencies. set-core (bash) calls it via `_wt_python` helper.

**Alternative**: Put resolver in set-core as bash/jq. Rejected — YAML parsing + Python class merging is much cleaner in Python.

### D2: Single YAML file with managed + custom sections

**Choice**: Extend `set/plugins/project-type.yaml` with custom sections below the managed header.

```yaml
# === Managed by wt-project init (do not edit above) ===
type: web
version: 0.1.0

# === Project customizations (edit freely) ===
custom_rules: [...]
disabled_rules: [...]
rule_overrides: {}
custom_directives: [...]
disabled_directives: [...]
```

**Why**: One file to find, one file to commit. The managed/custom boundary is clear via comments.

**Alternative**: Separate files (`project-type.yaml` + `custom-rules.yaml`). Rejected — splits related config unnecessarily.

### D3: Feedback as structured YAML lessons in wt/knowledge/lessons/

**Choice**: Lessons stored as YAML files with a fixed schema:

```yaml
# wt/knowledge/lessons/rule-feedback.yaml
lessons:
  - rule_id: migration-safety
    issue: false_positive
    context: "Seed file changes trigger migration check"
    suggested_fix:
      type: add_exclude
      value: "**/seed.*"
    timestamp: "2026-03-07"
```

**Why**: YAML is human-readable, diffable, committable. The schema forces anonymization — there's no field for project name or file paths. `rule_id` is the join key back to the upstream package.

**Alternative**: JSON in shodh-memory. Rejected — not portable, not easy to share as PR.

### D4: Merge order: package → YAML overlay

```
Package rules (BaseProjectType → WebProjectType → CegxType)
  + custom_rules (appended)
  - disabled_rules (filtered out by id)
  ~ rule_overrides (config merged by id)
  = FINAL RESOLVED SET
```

**Why**: Simple, predictable. Same model as CSS specificity — more specific wins.

### D5: `.local-overrides.yaml` for personal (gitignored) customizations

**Choice**: Optional `set/plugins/.local-overrides.yaml` with same format, applied after `project-type.yaml`.

**Why**: Developer might want to temporarily disable a rule locally without affecting the team.

## Risks / Trade-offs

- **[Risk] YAML schema drift** — Custom rules use same dataclass fields as Python rules. If we add fields to VerificationRule, YAML might miss them → Mitigation: resolver validates YAML entries against dataclass fields, warns on unknown keys.

- **[Risk] Feedback quality** — Lessons might be too vague to act on → Mitigation: CLI prompts for required fields (rule_id, issue type, suggested_fix). Export validates completeness.

- **[Trade-off] Single file vs split** — One YAML file is simpler but gets long with many custom rules → Acceptable for v1; can add `custom_rules_dir: rules.d/` later if needed.
