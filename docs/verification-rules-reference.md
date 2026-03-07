# Verification Rules Reference

## Web-Specific Rules

These rules are provided by `wt-project-web` on top of the base rules.

### i18n-completeness (error)
All locale files must contain the same set of translation keys.

- **Check type**: `cross-file-key-parity`
- **Files**: `messages/*.json`
- **Behavior**: Compares dot-path leaf keys across all matching files
- **Example failure**: Key `nav.reports` exists in `hu.json` but not `en.json`

### route-registered (warning)
New page routes should be referenced in the navigation config.

- **Check type**: `file-mentions`
- **Source**: `src/app/**/page.tsx` (excluding API, login, register, error)
- **Target**: Files under `cross_cutting_files.sidebar`
- **Example failure**: New `src/app/(dashboard)/reports/page.tsx` with no sidebar entry

### cross-cutting-consistency (warning)
Sidebar items, route labels, and i18n keys must stay in sync.

- **Check type**: `cross-reference`
- **Groups**: sidebar + route_labels + i18n files
- **Key pattern**: `route-segment` — extracts route names and cross-checks

### migration-safety (error)
Schema changes must have corresponding migration files.

- **Check type**: `schema-migration-sync`
- **Schema**: `prisma/schema.prisma`
- **Migrations**: `prisma/migrations/`
- **Design doc**: `docs/design/data-model.md`

### ghost-button-text (warning)
Ghost buttons must be icon-only — no text content allowed.

- **Check type**: `pattern-absence`
- **Files**: `src/components/**/*.tsx`
- **Pattern**: `variant="ghost"` followed by text content

## Base Rules (inherited)

These come from `wt-project-base` and apply to all project types.

### file-size-limit (warning)
Source files should not exceed 400 lines.

### no-secrets-in-source (error)
Source files should not contain hardcoded API keys, passwords, or secrets.

### todo-tracking (info)
TODO/FIXME/HACK comments should reference an issue or change.

## Check Types

See `verification-rules/SCHEMA.md` for the full schema documentation including all check types, configuration options, and override mechanisms.

## Customization

See [Plugin Architecture](plugin-architecture.md) for how to add custom rules, disable rules, or override rule configuration via `wt/plugins/project-type.yaml`.
