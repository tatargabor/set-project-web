## MODIFIED Requirements

### Requirement: Python deploy-templates command
The `set-project-base` CLI `deploy-templates` subcommand SHALL support an optional `--modules` parameter (comma-separated list of module IDs). When a `manifest.yaml` exists in the template, only core files and files from selected modules are deployed.

Arguments (updated):
- `--project-dir` (required): target project directory
- `--type` (required): project type name (resolved via entry points)
- `--template` (required unless type has exactly one variant): template variant ID
- `--modules` (optional): comma-separated module IDs to deploy
- `--force` (optional): overwrite existing files
- `--dry-run` (optional): show what would be deployed without writing

#### Scenario: Deploy with manifest and modules
- **WHEN** `deploy-templates --type web --template nextjs --modules gdpr` is run and `manifest.yaml` exists
- **THEN** core files plus the `gdpr` module files are deployed, other optional module files are not deployed

#### Scenario: Deploy with manifest and no modules specified
- **WHEN** `deploy-templates --type web --template nextjs` is run and `manifest.yaml` has optional modules
- **THEN** only core files are deployed, optional modules are listed as available

#### Scenario: Deploy without manifest (backward compat)
- **WHEN** `deploy-templates` is run and no `manifest.yaml` exists in the template
- **THEN** all files in the template directory are deployed (unchanged behavior)

#### Scenario: Deploy to new project
- **WHEN** `set-project-base deploy-templates --project-dir /tmp/myapp --type web --template nextjs` is run and no target files exist
- **THEN** all template files are copied to the target, preserving relative paths (project-knowledge.yaml → wt/knowledge/project-knowledge.yaml, rules/*.md → .claude/rules/*.md)

#### Scenario: Deploy to existing project (additive)
- **WHEN** deploy-templates is run and `.claude/rules/ui-conventions.md` already exists in the target
- **THEN** that file is skipped, a message is printed ("Skipped (exists): .claude/rules/ui-conventions.md"), and other missing files are still deployed

#### Scenario: Deploy with --force
- **WHEN** deploy-templates is run with `--force` and files already exist
- **THEN** existing files are overwritten and a message is printed ("Overwritten: .claude/rules/ui-conventions.md")
