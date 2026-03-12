## MODIFIED Requirements

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
  design_tokens:
    - tailwind.config.ts
    - src/styles/tokens.*
```

#### Scenario: Orchestrator identifies cross-cutting impact
- **WHEN** a change modifies a file listed under `sidebar` in the registry
- **THEN** the orchestrator knows that `i18n` and `route_labels` files may also need updates

#### Scenario: Verification uses registry for consistency checks
- **WHEN** `opsx:verify` runs and a new sidebar item is detected
- **THEN** the system checks that corresponding entries exist in the `i18n` and `route_labels` files

#### Scenario: Design token changes flagged as cross-cutting
- **WHEN** a change modifies `tailwind.config.ts` theme values
- **THEN** the orchestrator identifies this as a cross-cutting change via the `design_tokens` registry entry
- **AND** other changes depending on those tokens can be flagged for review

### Requirement: Next.js App Router template

The system SHALL provide a `web-nextjs` template that includes:
- Cross-cutting file registry for Next.js App Router projects (app directory, layout files, route groups)
- i18n configuration for `next-intl` (locale files, server/client translation patterns)
- Sidebar/navigation patterns (server component data fetching, client rendering with titleKey)
- Prisma DB patterns (tenant scoping, singleton client, migration workflow)
- Server action conventions (auth guard, revalidatePath, error return type)
- Component conventions (shadcn/ui, button variant policy, file size limits)
- Design integration rule for mapping design tools to the web stack

#### Scenario: Template covers standard Next.js structure
- **WHEN** user initializes with `--type web-nextjs`
- **THEN** the generated `project-knowledge.yaml` includes App Router-aware path patterns
- **AND** `.claude/rules/` files cover: functional-conventions, ui-conventions, auth-conventions, data-model, design-integration
