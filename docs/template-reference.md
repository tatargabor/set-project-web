# Template Reference

## Available Templates

| Template | ID | Description |
|----------|----|-------------|
| Next.js App Router | `nextjs` | Full-stack Next.js with Prisma, next-intl, shadcn/ui |
| Generic SPA | `spa` | Minimal starting point for any SPA framework |

## Next.js Template (`nextjs`)

### Files

| File | Purpose |
|------|---------|
| `project-knowledge.yaml` | Cross-cutting file registry + feature registry |
| `rules/functional-conventions.md` | Server actions, DB patterns, form patterns |
| `rules/ui-conventions.md` | shadcn/ui, layout, button policy, i18n rules |
| `rules/auth-conventions.md` | Role hierarchy, session patterns, impersonation |
| `rules/data-model.md` | Prisma conventions, tenant scoping, migrations |
| `rules/deployment.md` | Docker, CI/CD, environment variables |

### project-knowledge.yaml Sections

**cross_cutting_files** — Maps logical roles to file paths:
- `sidebar` — Navigation component files
- `i18n` — Locale/translation files
- `route_labels` — Route label definitions
- `db_schema` — Database schema files
- `design_docs` — Design documentation
- `auth` — Authentication configuration

**features** — Maps feature areas to file scopes:
- Each feature has `touches` (file patterns) and optional `rules_file`
- The rules file activates when editing files in the feature's scope

### Rules Files

Each rules file has a `paths:` frontmatter that controls when it's loaded:

```yaml
---
paths:
  - "src/components/**"
---
```

Rules files are concise (< 100 lines) and reference full docs for details.

## SPA Template (`spa`)

### Files

| File | Purpose |
|------|---------|
| `project-knowledge.yaml` | Minimal cross-cutting file registry with comments |
| `rules/components.md` | Generic component conventions |

### Customization

The SPA template is intentionally minimal. Each section includes comments explaining what to customize for your specific framework.

## Using Templates

```bash
# Initialize with a template
set-project-web init --type nextjs --target /path/to/project

# List available templates
set-project-web list
```

After initialization, all files are yours to customize. The template is a starting point, not a constraint.
