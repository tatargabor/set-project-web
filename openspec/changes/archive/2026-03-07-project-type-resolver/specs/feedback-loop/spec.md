## ADDED Requirements

### Requirement: Structured lesson format
Feedback lessons SHALL use a fixed YAML schema with fields: `rule_id`, `issue` (enum: false_positive, too_aggressive, missing_exclude, missing_rule, config_improvement), `context` (free text describing the issue without project/company names), `suggested_fix` (type + value), and `timestamp`.

#### Scenario: Valid lesson entry
- **WHEN** a lesson is recorded with rule_id "migration-safety", issue "false_positive", and context "Seed file changes trigger migration check"
- **THEN** the lesson is stored in `wt/knowledge/lessons/rule-feedback.yaml` with all required fields

#### Scenario: Lesson without project-specific information
- **WHEN** a lesson is created
- **THEN** the schema SHALL NOT include fields for project name, company name, or absolute file paths

### Requirement: Feedback record CLI
`set-project-base feedback record` SHALL interactively prompt for rule_id (with autocomplete from resolved rules), issue type, context, and suggested fix, then append to `wt/knowledge/lessons/rule-feedback.yaml`.

#### Scenario: Interactive recording
- **WHEN** user runs `set-project-base feedback record --project-dir /path/to/project`
- **THEN** CLI lists available rule IDs from the resolved set, prompts for issue type from the enum, asks for context and suggested fix, then appends the lesson

#### Scenario: Non-interactive recording
- **WHEN** user runs `set-project-base feedback record --rule-id migration-safety --issue false_positive --context "Seed changes trigger check" --fix-type add_exclude --fix-value "**/seed.*"`
- **THEN** CLI appends the lesson without prompting

### Requirement: Feedback export
`set-project-base feedback export` SHALL read all lessons from `wt/knowledge/lessons/rule-feedback.yaml`, validate they contain no project-specific information, and output anonymized YAML suitable for sharing as upstream PR or issue.

#### Scenario: Export produces clean YAML
- **WHEN** user runs `set-project-base feedback export --project-dir /path/to/project`
- **THEN** CLI outputs YAML with header comment explaining the format, each lesson entry, and no project-identifying information

#### Scenario: Export warns on potentially identifying content
- **WHEN** a lesson's context field contains a path-like string (e.g., `/home/user/project/src/`)
- **THEN** CLI emits a warning: "Lesson for rule X may contain project-specific path — review before sharing"

### Requirement: Feedback validation
The feedback system SHALL validate lesson entries against the schema on both record and export.

#### Scenario: Invalid issue type
- **WHEN** a lesson has issue type "bad_rule" which is not in the enum
- **THEN** CLI rejects with error listing valid issue types

#### Scenario: Missing required field
- **WHEN** a lesson is missing rule_id
- **THEN** CLI rejects with error "rule_id is required"
