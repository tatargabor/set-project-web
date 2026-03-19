## ADDED Requirements

### Requirement: Template manifest format
Templates MAY contain a `manifest.yaml` file that defines core files and optional modules.

Core files are always deployed. Optional modules are deployed only when selected by the user.

```yaml
core:
  - project-knowledge.yaml
  - rules/ui-conventions.md

modules:
  gdpr:
    description: "GDPR retention, suppression, data export"
    files:
      - rules/data-privacy.md
```

#### Scenario: Template with manifest
- **WHEN** a template directory contains `manifest.yaml`
- **THEN** `deploy_templates()` SHALL deploy only core files plus selected modules

#### Scenario: Template without manifest (backward compat)
- **WHEN** a template directory does not contain `manifest.yaml`
- **THEN** `deploy_templates()` SHALL deploy all files in the directory (existing behavior)

#### Scenario: Manifest references non-existent file
- **WHEN** `manifest.yaml` lists a file that does not exist in the template directory
- **THEN** a warning is printed and the missing file is skipped

### Requirement: Module selection via CLI
`wt-project init` SHALL accept a `--modules` flag with a comma-separated list of module IDs.

#### Scenario: Explicit module selection
- **WHEN** `wt-project init --project-type web --template nextjs --modules gdpr,integrations` is run
- **THEN** core files plus the `gdpr` and `integrations` modules are deployed

#### Scenario: Interactive module selection
- **WHEN** `--modules` is not specified, optional modules exist, and no prior selection is tracked
- **THEN** available modules are listed and the user is prompted for comma-separated input

#### Scenario: Unknown module ID
- **WHEN** `--modules foo` is specified but no module named `foo` exists in manifest
- **THEN** a warning is printed listing available modules, and `foo` is skipped

### Requirement: Module tracking in project-type.yaml
Selected modules SHALL be persisted in `set/plugins/project-type.yaml` under a `modules` key.

#### Scenario: Modules saved on first init
- **WHEN** user selects modules during init
- **THEN** the module list is written to `project-type.yaml` alongside the type and template

#### Scenario: Re-init uses tracked modules
- **WHEN** `wt-project init` is re-run and `project-type.yaml` contains a `modules` list
- **THEN** the tracked modules are deployed without re-prompting

#### Scenario: Override tracked modules
- **WHEN** `wt-project init --modules gdpr` is re-run and `project-type.yaml` had `modules: [gdpr, integrations]`
- **THEN** the new selection (`gdpr` only) replaces the tracked modules
