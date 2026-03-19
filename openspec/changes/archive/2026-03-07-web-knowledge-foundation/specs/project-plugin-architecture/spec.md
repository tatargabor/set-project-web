## ADDED Requirements

### Requirement: Layered plugin hierarchy

The system SHALL support a three-layer project-knowledge plugin hierarchy:
1. **Base layer** (`set-project-base`) — universal software project rules (code hygiene, git workflow, file size limits, documentation patterns)
2. **Domain layer** (e.g., `set-project-web`) — domain-specific rules (i18n, routing, DB migrations, component conventions)
3. **Custom layer** (e.g., `wt-project-acme`) — organization-specific rules and overrides

Each layer SHALL inherit all rules from its parent layer and MAY override or extend them.

#### Scenario: Domain plugin inherits base rules
- **WHEN** a project uses `set-project-web`
- **THEN** all `set-project-base` rules are automatically active
- **AND** web-specific rules are added on top

#### Scenario: Custom plugin extends domain plugin
- **WHEN** an organization creates `wt-project-acme` extending `set-project-web`
- **THEN** base + web rules are active
- **AND** organization-specific overrides take precedence

### Requirement: Configuration-driven knowledge definition

Project knowledge SHALL be expressed as YAML configuration and Markdown files, NOT as executable code. The configuration files are:
- `project-knowledge.yaml` — cross-cutting file registry and feature registry
- `.claude/rules/*.md` — path-scoped convention files with YAML frontmatter
- `verification-rules.yaml` — declarative verification checks
- `orchestration-directives.yaml` — orchestration guardrails

#### Scenario: Plugin provides only configuration files
- **WHEN** a project-knowledge plugin is installed
- **THEN** it delivers YAML and Markdown files to the consumer project
- **AND** no Python code execution is required in the consumer project

### Requirement: Template inheritance via extends

Consumer projects SHALL be able to extend a plugin template using an `extends` field in `project-knowledge.yaml`:
```yaml
extends: set-project-web/nextjs
```

The system SHALL merge the parent template with the consumer's overrides, where consumer values take precedence for any conflicting keys.

#### Scenario: Consumer overrides a template value
- **WHEN** the parent template defines `sidebar_config: "src/components/sidebar.tsx"`
- **AND** the consumer's `project-knowledge.yaml` defines `sidebar_config: "src/ui/nav/sidebar.tsx"`
- **THEN** the consumer's value is used

#### Scenario: Consumer adds to a template list
- **WHEN** the parent template defines `locale_files: ["messages/*.json"]`
- **AND** the consumer adds `locale_files: ["messages/*.json", "content/*.json"]`
- **THEN** the merged result includes both patterns

### Requirement: Plugin discovery via Python entry points

Project-knowledge plugins SHALL be discoverable via Python entry points under the group `set_tools.project_types`. This extends the existing `wt_tools.plugins` mechanism.

```toml
[project.entry-points."set_tools.project_types"]
web = "set_project_web:WebProjectType"
```

#### Scenario: Plugin is discovered automatically
- **WHEN** `set-project-web` is installed as a Python package
- **THEN** `wt-project init --type web-nextjs` can find and use its templates
- **AND** no manual registration is needed

### Requirement: Init command scaffolds project knowledge

The `wt-project init --type <type>` command SHALL scaffold all project-knowledge files from the selected plugin template into the consumer project.

#### Scenario: Initialize a Next.js project
- **WHEN** user runs `wt-project init --type web-nextjs`
- **THEN** the following files are created from templates:
  - `project-knowledge.yaml`
  - `.claude/rules/*.md` (path-scoped convention files)
  - `verification-rules.yaml`
- **AND** `orchestration-directives.yaml` entries are merged into `orchestration.yaml` if it exists

#### Scenario: Init does not overwrite existing files
- **WHEN** user runs `wt-project init` and `project-knowledge.yaml` already exists
- **THEN** the system SHALL warn and skip existing files unless `--force` is provided
