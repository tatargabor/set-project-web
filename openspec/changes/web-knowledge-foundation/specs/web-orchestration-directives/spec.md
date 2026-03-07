## ADDED Requirements

### Requirement: i18n parallelization guard

The system SHALL provide an orchestration directive that prevents i18n translation changes from running in parallel with UI-label changes. This prevents merge conflicts on locale files.

```yaml
- id: no-parallel-i18n
  trigger: change-modifies("messages/*.json")
  action: serialize
  with: changes-modifying("messages/*.json")
  description: Serialize changes that modify locale files to prevent merge conflicts
```

#### Scenario: Two i18n changes serialized
- **WHEN** change A modifies `messages/hu.json` to add navigation labels
- **AND** change B modifies `messages/hu.json` to add form labels
- **THEN** the orchestrator runs them sequentially, not in parallel

#### Scenario: i18n change runs parallel with unrelated change
- **WHEN** change A modifies `messages/hu.json`
- **AND** change B only modifies `src/lib/auth.ts`
- **THEN** they MAY run in parallel (no locale file conflict)

### Requirement: Single i18n migration directive

The system SHALL provide a directive that warns when multiple changes each modify locale files, suggesting consolidation into a single change.

```yaml
- id: consolidate-i18n
  trigger: plan-has-multiple-changes-modifying("messages/*.json")
  action: warn
  message: "Multiple changes modify locale files — consider consolidating into a single i18n change"
```

#### Scenario: Plan with 3 separate i18n changes
- **WHEN** an orchestration plan includes 3 changes that each add keys to locale files
- **THEN** the orchestrator warns: "Consider consolidating into a single i18n change"
- **AND** the warning is logged but does not block execution

### Requirement: Post-merge command configuration

The system SHALL provide orchestration directives for post-merge commands that must run after changes are merged to the main branch.

```yaml
- id: db-generate
  trigger: change-modifies("prisma/schema.prisma")
  post_merge: "pnpm db:generate"
  description: Regenerate Prisma client after schema changes

- id: install-deps
  trigger: change-modifies("package.json")
  post_merge: "pnpm install"
  description: Install dependencies after package.json changes
```

#### Scenario: Schema change triggers db:generate
- **WHEN** a change that modifies `prisma/schema.prisma` is merged
- **THEN** the orchestrator runs `pnpm db:generate` after merge
- **AND** if the command fails, it is reported as a post-merge error

#### Scenario: No schema change skips db:generate
- **WHEN** a change does NOT modify `prisma/schema.prisma`
- **THEN** the `db:generate` post-merge command is NOT triggered

### Requirement: Smoke test configuration template

The system SHALL provide a template for smoke test orchestration configuration:

```yaml
smoke:
  command: "pnpm test:smoke"
  timeout: 120
  env:
    SMOKE_BASE_URL: "http://localhost:3002"
  fix_timeout: 300  # max seconds to spend fixing a failed smoke test
  retry: 1          # retries before escalating
```

#### Scenario: Smoke test runs after merge
- **WHEN** a change is merged and smoke tests are configured
- **THEN** the orchestrator runs the smoke command with the specified environment
- **AND** applies the configured timeout

#### Scenario: Smoke fix timeout prevents infinite loops
- **WHEN** a smoke test fails and the agent attempts to fix it
- **AND** the fix attempt exceeds `fix_timeout` seconds
- **THEN** the orchestrator escalates instead of retrying

### Requirement: Cross-cutting change detection directive

The system SHALL provide a directive that flags changes touching cross-cutting files for extra review attention:

```yaml
- id: cross-cutting-review
  trigger: change-modifies-any(cross_cutting_files.sidebar, cross_cutting_files.i18n, cross_cutting_files.route_labels)
  action: flag-for-review
  description: Changes to cross-cutting files need careful review for consistency
```

#### Scenario: Sidebar change flagged for review
- **WHEN** a change modifies a file listed in `cross_cutting_files.sidebar`
- **THEN** the change is flagged with a "cross-cutting" label for review
- **AND** verification runs cross-cutting consistency checks

### Requirement: Context efficiency directive

The system SHALL provide a directive for managing Claude context window efficiency in consumer projects:

```yaml
- id: rules-not-claude-md
  description: Domain conventions go in .claude/rules/ with path-scoped activation, NOT in CLAUDE.md
  guidance:
    - CLAUDE.md contains only critical rules that apply to EVERY task
    - Domain-specific rules use .claude/rules/*.md with paths: frontmatter
    - Never use @ imports in CLAUDE.md (loads full file every turn)
    - Rules files reference full docs, not copy them
```

#### Scenario: New convention added correctly
- **WHEN** a developer adds a new email-related convention
- **THEN** it goes into `.claude/rules/email-conventions.md` with `paths:` matching email-related source files
- **AND** CLAUDE.md is NOT modified

#### Scenario: CLAUDE.md stays lean
- **WHEN** a project follows this directive
- **THEN** CLAUDE.md contains fewer than 3000 tokens of rule content
- **AND** domain-specific conventions are loaded on-demand via path matching
