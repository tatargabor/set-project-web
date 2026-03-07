## ADDED Requirements

### Requirement: Resolve rules from package and YAML overlay
The ProjectTypeResolver SHALL load verification rules from the installed ProjectType package and merge them with customizations from `wt/plugins/project-type.yaml`. The final resolved set SHALL be: package rules + custom_rules - disabled_rules, with rule_overrides applied.

#### Scenario: Package rules only (no overlay)
- **WHEN** a project has `type: web` in project-type.yaml with no custom sections
- **THEN** resolver returns all rules from WebProjectType (inherited base + web rules)

#### Scenario: Custom rules added
- **WHEN** project-type.yaml contains `custom_rules` with a valid rule entry
- **THEN** resolver returns package rules plus the custom rules appended at the end

#### Scenario: Rules disabled
- **WHEN** project-type.yaml contains `disabled_rules: ["ghost-button-text"]`
- **THEN** resolver returns all package rules except `ghost-button-text`

#### Scenario: Rule config overridden
- **WHEN** project-type.yaml contains `rule_overrides: { file-size-limit: { config: { max_lines: 600 } } }`
- **THEN** resolver returns `file-size-limit` rule with `max_lines: 600` instead of the package default (400)

#### Scenario: Unknown rule in disabled_rules
- **WHEN** project-type.yaml contains `disabled_rules: ["nonexistent-rule"]`
- **THEN** resolver SHALL emit a warning and proceed without error

### Requirement: Resolve orchestration directives from package and YAML overlay
The ProjectTypeResolver SHALL apply the same merge logic to orchestration directives: package directives + custom_directives - disabled_directives.

#### Scenario: Custom directive added
- **WHEN** project-type.yaml contains `custom_directives` with a valid directive entry
- **THEN** resolver returns package directives plus the custom directive

#### Scenario: Directive disabled
- **WHEN** project-type.yaml contains `disabled_directives: ["install-deps-python"]`
- **THEN** resolver returns all package directives except `install-deps-python`

### Requirement: Local overrides file
The resolver SHALL check for `wt/plugins/.local-overrides.yaml` and apply it as a final layer after project-type.yaml. This file uses the same format (custom_rules, disabled_rules, rule_overrides, custom_directives, disabled_directives).

#### Scenario: Local override disables a rule
- **WHEN** `.local-overrides.yaml` contains `disabled_rules: ["todo-tracking"]`
- **THEN** resolver excludes `todo-tracking` from the final set, even if project-type.yaml does not disable it

#### Scenario: No local overrides file
- **WHEN** `.local-overrides.yaml` does not exist
- **THEN** resolver proceeds with project-type.yaml overlay only, no error

### Requirement: Resolver summary
The resolver SHALL provide a `summary()` method returning counts: total rules, from_package, custom, disabled, overridden — for both rules and directives.

#### Scenario: Summary output
- **WHEN** resolver has 8 package rules, 2 custom, 1 disabled, 1 overridden
- **THEN** summary returns `{ total: 9, from_package: 8, custom: 2, disabled: 1, overridden: 1 }`

### Requirement: CLI resolve command
`wt-project-base resolve` SHALL accept a `--project-dir` argument, load the project type and overlay, and print the final resolved rules and directives.

#### Scenario: Resolve with project dir
- **WHEN** user runs `wt-project-base resolve --project-dir /path/to/project`
- **THEN** CLI prints each resolved rule and directive with source annotation (package/custom/overridden)

### Requirement: Backward compatibility
Existing `project-type.yaml` files without custom sections SHALL work unchanged. The resolver SHALL treat missing custom sections as empty.

#### Scenario: Legacy YAML without custom sections
- **WHEN** project-type.yaml contains only `type`, `version`, `description`
- **THEN** resolver returns package rules and directives unmodified
