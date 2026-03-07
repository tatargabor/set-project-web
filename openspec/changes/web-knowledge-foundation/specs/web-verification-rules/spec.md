## ADDED Requirements

### Requirement: i18n completeness check

The system SHALL provide a verification rule that checks all locale files contain the same set of keys. When a key exists in one locale file but not another, the rule SHALL report it as an error.

```yaml
- id: i18n-completeness
  check: cross-file-key-parity
  files:
    pattern: "messages/*.json"
  severity: error
  description: All UI strings must exist in all locale files
```

#### Scenario: Missing translation key detected
- **WHEN** `messages/hu.json` contains key `nav.dashboard` but `messages/en.json` does not
- **THEN** verification reports an error: "Missing key 'nav.dashboard' in messages/en.json"

#### Scenario: All keys present
- **WHEN** all locale files contain identical key sets (values may differ)
- **THEN** the i18n completeness check passes

#### Scenario: Nested key comparison
- **WHEN** locale files use nested JSON structures (e.g., `{ "nav": { "dashboard": "..." } }`)
- **THEN** the check compares the full dot-path of every leaf key

### Requirement: Route registration check

The system SHALL provide a verification rule that checks new page routes are registered in the navigation configuration (sidebar, menu, or route labels).

```yaml
- id: route-registered
  check: file-mentions
  source:
    pattern: "src/app/**/page.tsx"
    exclude: ["src/app/api/**", "src/app/login/**", "src/app/register/**"]
  target: cross-cutting.sidebar
  severity: warning
  description: New page routes should be registered in navigation config
```

#### Scenario: New page without sidebar entry
- **WHEN** a new `src/app/(dashboard)/reports/page.tsx` is created
- **AND** no reference to "reports" exists in the sidebar configuration
- **THEN** verification reports a warning: "Route '/reports' may need a sidebar entry"

#### Scenario: API route excluded from check
- **WHEN** a new `src/app/api/webhooks/route.ts` is created
- **THEN** the route registration check does NOT flag it (API routes are excluded)

### Requirement: Cross-cutting consistency check

The system SHALL provide a verification rule that checks consistency between cross-cutting files. When a new entry is added to one cross-cutting file, the rule SHALL check that corresponding entries exist in related files.

```yaml
- id: cross-cutting-consistency
  check: cross-reference
  groups:
    - name: navigation
      files:
        - role: sidebar
        - role: route_labels
        - role: i18n
      key_pattern: route-segment
  severity: warning
```

#### Scenario: Sidebar item without i18n key
- **WHEN** a new sidebar item with `titleKey: "reports"` is added
- **AND** `messages/hu.json` does not contain `nav.reports`
- **THEN** verification reports a warning: "Sidebar item 'reports' missing i18n key 'nav.reports'"

#### Scenario: All cross-cutting files in sync
- **WHEN** sidebar items, route labels, and i18n keys all reference the same set of routes
- **THEN** the cross-cutting consistency check passes

### Requirement: DB migration safety check

The system SHALL provide a verification rule that checks database migration safety practices:
1. Schema changes have corresponding migration files
2. Design documentation is updated when schema changes
3. Migration ordering is correct (no gaps, no duplicates)

```yaml
- id: migration-safety
  check: schema-migration-sync
  schema_file: prisma/schema.prisma  # or equivalent
  migrations_dir: prisma/migrations/
  design_doc: docs/design/data-model.md
  severity: error
```

#### Scenario: Schema change without migration
- **WHEN** `prisma/schema.prisma` is modified (new model or field)
- **AND** no new migration file exists in `prisma/migrations/`
- **THEN** verification reports an error: "Schema changes detected without corresponding migration"

#### Scenario: Schema change without design doc update
- **WHEN** a new model is added to the schema
- **AND** `docs/design/data-model.md` is not modified in the same change
- **THEN** verification reports a warning: "New model added — consider updating data-model.md"

### Requirement: Component convention checks

The system SHALL provide verification rules for frontend component conventions:

```yaml
- id: file-size-limit
  check: file-line-count
  pattern: "src/**/*.{tsx,ts}"
  max_lines: 400
  severity: warning

- id: button-variant-policy
  check: pattern-absence
  pattern: "src/components/**/*.tsx"
  forbidden: 'variant="ghost".*>[^<]*<'  # ghost with text content
  severity: warning
  description: Ghost buttons must be icon-only
```

#### Scenario: Oversized component file
- **WHEN** a component file exceeds 400 lines
- **THEN** verification reports a warning: "File exceeds 400 line limit — consider splitting"

#### Scenario: Ghost button with text
- **WHEN** a component uses `<Button variant="ghost">Delete</Button>` (ghost with text)
- **THEN** verification reports a warning: "Ghost buttons should be icon-only"

### Requirement: Verification rule severity levels

Each verification rule SHALL have a `severity` field with one of:
- `error` — blocks merge, must be fixed
- `warning` — reported but does not block
- `info` — informational, logged only

Consumer projects SHALL be able to override severity levels per rule.

#### Scenario: Consumer downgrades a rule severity
- **WHEN** the base template defines `i18n-completeness` as `error`
- **AND** the consumer's `verification-rules.yaml` overrides it to `warning`
- **THEN** the rule reports warnings instead of errors

### Requirement: Per-rule ignore lists

Each verification rule SHALL support an `ignore` list for legitimate exceptions:

```yaml
- id: route-registered
  ignore:
    - src/app/(dashboard)/secret-admin/page.tsx
    - src/app/preview/page.tsx
```

#### Scenario: Ignored file is not flagged
- **WHEN** a file is listed in a rule's `ignore` list
- **THEN** that file is excluded from the rule's checks
