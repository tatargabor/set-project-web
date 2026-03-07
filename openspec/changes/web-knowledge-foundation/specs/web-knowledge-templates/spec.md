## ADDED Requirements

### Requirement: Cross-cutting file registry

The `project-knowledge.yaml` template SHALL include a `cross_cutting_files` section that maps logical roles to file paths. This registry tells the orchestrator which files are affected by cross-cutting changes.

```yaml
cross_cutting_files:
  sidebar:
    - src/components/app-sidebar.tsx
    - src/components/platform-sidebar.tsx
  navigation:
    - src/app/**/layout.tsx
  i18n:
    - messages/*.json
  route_labels:
    - src/lib/route-labels.ts
  db_schema:
    - prisma/schema.prisma
  design_docs:
    - docs/design/*.md
```

#### Scenario: Orchestrator identifies cross-cutting impact
- **WHEN** a change modifies a file listed under `sidebar` in the registry
- **THEN** the orchestrator knows that `i18n` and `route_labels` files may also need updates

#### Scenario: Verification uses registry for consistency checks
- **WHEN** `opsx:verify` runs and a new sidebar item is detected
- **THEN** the system checks that corresponding entries exist in the `i18n` and `route_labels` files

### Requirement: Feature registry pattern

The template SHALL include a `features` section that documents the project's feature areas and their associated file patterns:

```yaml
features:
  auth:
    paths:
      - src/lib/auth.ts
      - src/app/login/**
      - src/app/register/**
    rules_file: .claude/rules/auth-conventions.md
  email:
    paths:
      - src/lib/email/**
      - src/app/api/imap/**
      - src/app/**/email-*/**
    rules_file: .claude/rules/email-conventions.md
```

#### Scenario: Path-scoped rules map to features
- **WHEN** an agent edits a file matching `src/lib/email/**`
- **THEN** the `email-conventions.md` rules are activated for that context

### Requirement: Next.js App Router template

The system SHALL provide a `web-nextjs` template that includes:
- Cross-cutting file registry for Next.js App Router projects (app directory, layout files, route groups)
- i18n configuration for `next-intl` (locale files, server/client translation patterns)
- Sidebar/navigation patterns (server component data fetching, client rendering with titleKey)
- Prisma DB patterns (tenant scoping, singleton client, migration workflow)
- Server action conventions (auth guard, revalidatePath, error return type)
- Component conventions (shadcn/ui, button variant policy, file size limits)

#### Scenario: Template covers standard Next.js structure
- **WHEN** user initializes with `--type web-nextjs`
- **THEN** the generated `project-knowledge.yaml` includes App Router-aware path patterns
- **AND** `.claude/rules/` files cover: functional-conventions, ui-conventions, auth-conventions, data-model

### Requirement: Generic SPA template

The system SHALL provide a `web-spa` template as a minimal starting point for single-page applications that do not fit the Next.js template. It SHALL include:
- Basic cross-cutting file registry (router config, i18n, API client)
- Component conventions (file size, naming)
- State management patterns placeholder

#### Scenario: Generic template is minimal and customizable
- **WHEN** user initializes with `--type web-spa`
- **THEN** the generated config has fewer defaults than framework-specific templates
- **AND** each section includes comments explaining what to customize

### Requirement: Rules file structure with path-scoped activation

Each `.claude/rules/*.md` template file SHALL include a YAML frontmatter `paths:` section that specifies which source files trigger the rule's activation:

```yaml
---
paths:
  - "src/components/**"
  - "src/app/**/*.tsx"
---
# UI Conventions
...
```

Rules files SHALL contain only decision-critical rules, NOT full documentation copies. Each file SHALL reference its full documentation source:
```markdown
Full reference: `docs/design/<topic>.md`
```

#### Scenario: Rules activate only for matching paths
- **WHEN** an agent edits `src/components/sidebar.tsx`
- **THEN** only rules with matching path patterns (e.g., `src/components/**`) are loaded
- **AND** rules for unrelated paths (e.g., `prisma/migrations/**`) are NOT loaded

#### Scenario: Rules file stays concise
- **WHEN** a rules file is generated from a template
- **THEN** it contains fewer than 100 lines of actual rule content
- **AND** it references a full documentation file for detailed explanations
