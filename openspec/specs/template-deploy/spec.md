## ADDED Requirements

### Requirement: Python deploy-templates command
The `set-project-base` CLI SHALL provide a `deploy-templates` subcommand that copies template files from a project type package into a target project directory.

Arguments:
- `--project-dir` (required): target project directory
- `--type` (required): project type name (resolved via entry points)
- `--template` (required unless type has exactly one variant): template variant ID
- `--force` (optional): overwrite existing files
- `--dry-run` (optional): show what would be deployed without writing

The command SHALL exit 0 on success and print a summary of deployed/skipped files.

#### Scenario: Deploy to new project
- **WHEN** `set-project-base deploy-templates --project-dir /tmp/myapp --type web --template nextjs` is run and no target files exist
- **THEN** all template files are copied to the target, preserving relative paths (project-knowledge.yaml → wt/knowledge/project-knowledge.yaml, rules/*.md → .claude/rules/*.md)

#### Scenario: Deploy to existing project (additive)
- **WHEN** deploy-templates is run and `.claude/rules/ui-conventions.md` already exists in the target
- **THEN** that file is skipped, a message is printed ("Skipped (exists): .claude/rules/ui-conventions.md"), and other missing files are still deployed

#### Scenario: Deploy with --force
- **WHEN** deploy-templates is run with `--force` and files already exist
- **THEN** existing files are overwritten and a message is printed ("Overwritten: .claude/rules/ui-conventions.md")

#### Scenario: Single template auto-selection
- **WHEN** `--template` is not specified and the project type has exactly one template variant
- **THEN** that variant is used automatically

#### Scenario: Multiple templates without selection
- **WHEN** `--template` is not specified and the project type has multiple variants
- **THEN** the command exits with error listing available variants

#### Scenario: Unknown template variant
- **WHEN** `--template foo` is specified but the project type has no variant named "foo"
- **THEN** the command exits with error listing available variants

### Requirement: Bash init integration
The `wt-project init` bash script SHALL call the Python deploy-templates command after saving the project type, when `--project-type` is specified.

A new `--template` flag SHALL be added to `wt-project init`.

#### Scenario: Init with project type and template
- **WHEN** `wt-project init --project-type web --template nextjs` is run
- **THEN** the project is registered, set-core deployed, project type saved, AND template files deployed to the project

#### Scenario: Init with project type only
- **WHEN** `wt-project init --project-type web` is run and web has multiple templates
- **THEN** the project type is saved but template deploy is skipped with a message: "Multiple templates available for 'web': nextjs, spa. Use --template <name> to deploy one."

### Requirement: init-knowledge project-type awareness
`wt-project init-knowledge` SHALL check for a configured project type in `set/plugins/project-type.yaml`. When a project type is configured and has templates, it SHALL use the project type's template instead of the generic set-core template.

#### Scenario: init-knowledge with project type configured
- **WHEN** `wt-project init-knowledge` is run and `set/plugins/project-type.yaml` specifies `type: web`
- **THEN** the project-knowledge.yaml from the web project type's template is used (with variant selection if needed)

#### Scenario: init-knowledge without project type
- **WHEN** `wt-project init-knowledge` is run and no project-type.yaml exists
- **THEN** behavior is unchanged — uses the generic set-core template with auto-scan

### Requirement: Package data inclusion
`set-project-web` pyproject.toml SHALL include template files, directives, and verification-rules in the built package so they are accessible at runtime via `importlib.resources` or `ProjectType.get_template_dir()`.

#### Scenario: Templates accessible after pip install
- **WHEN** `set-project-web` is installed via pip
- **THEN** `WebProjectType().get_template_dir("nextjs")` returns a valid path containing `project-knowledge.yaml` and `rules/*.md`
