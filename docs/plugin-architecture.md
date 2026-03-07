# Plugin Architecture

## Three-Layer Hierarchy

```
wt-project-base          Universal rules (file size, secrets, lockfile conflicts)
  └── wt-project-web      Web domain rules (i18n, routing, DB, components)
        └── your-org-web   Organization-specific rules (your linter, your conventions)
```

Each layer inherits all rules and directives from its parent. You only define what's new or different.

## How It Works

### 1. Package provides rules (Python)

Each project type is a Python package with an entry point:

```toml
# pyproject.toml
[project.entry-points."wt_tools.project_types"]
web = "wt_project_web:WebProjectType"
```

The class extends `BaseProjectType` and defines rules + directives:

```python
class WebProjectType(BaseProjectType):
    def get_verification_rules(self):
        return super().get_verification_rules() + [
            VerificationRule(id="i18n-completeness", ...)
        ]
```

### 2. YAML overlay customizes per-project

`wt/plugins/project-type.yaml` in each project:

```yaml
type: web

custom_rules:
  - id: audit-log-required
    description: "All API routes must call auditLog()"
    check: file-mentions
    severity: error

disabled_rules:
  - ghost-button-text

rule_overrides:
  file-size-limit:
    config:
      max_lines: 600
```

### 3. Resolver merges everything

```
Package rules (base → web → custom-type)
  + custom_rules        (appended)
  - disabled_rules      (filtered out)
  ~ rule_overrides      (config merged)
  + .local-overrides.yaml (personal, gitignored)
  = FINAL RESOLVED SET
```

View the final set: `wt-project-base resolve --project-dir .`

## Creating a Custom Project Type

### Option A: YAML only (no Python)

Just edit `wt/plugins/project-type.yaml` — add custom_rules, disable what you don't need. No package required.

### Option B: Python package (reusable across projects)

```bash
mkdir my-project-type && cd my-project-type
```

```python
# my_project_type/project_type.py
from wt_project_base import BaseProjectType  # or WebProjectType

class MyProjectType(BaseProjectType):
    @property
    def info(self):
        return ProjectTypeInfo(name="my-type", version="0.1.0", ...)

    def get_verification_rules(self):
        return super().get_verification_rules() + [...]
```

```toml
# pyproject.toml
[project.entry-points."wt_tools.project_types"]
my-type = "my_project_type:MyProjectType"
```

```bash
pip install -e .
wt-project init --project-type my-type
```

## Discovery

Project types are discovered via Python entry points (`wt_tools.project_types`). Any installed package with this entry point is available:

```bash
wt-project list-types
```

## Feedback Loop

Record anonymized feedback about rules:

```bash
wt-project-base feedback record \
  --rule-id migration-safety \
  --issue false_positive \
  --context "Seed file changes trigger migration check" \
  --fix-type add_exclude \
  --fix-value "**/seed.*"
```

Export for sharing upstream:

```bash
wt-project-base feedback export --project-dir .
```
