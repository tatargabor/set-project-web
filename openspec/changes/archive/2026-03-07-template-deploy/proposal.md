## Why

`wt-project init --project-type web` saves the project type to `set/plugins/project-type.yaml` and the resolver can merge rules/directives, but the template files (project-knowledge.yaml, .claude/rules/*.md) bundled in the project type package are never deployed to the target project. Users must manually copy these files or use `init-knowledge` which only knows about the generic template. This is the missing bridge between "project type registered" and "project actually configured with domain knowledge."

## What Changes

- Add a `deploy_templates` command to `set-project-base` Python CLI that copies template files from a project type package into the target project directory (additive — skip existing files by default, `--force` to overwrite)
- Add a `--template` flag to `wt-project init` to select which template variant to deploy (e.g., `nextjs`, `spa`)
- Update `wt-project init` bash script to call the Python template deploy after saving the project type
- Update `wt-project init-knowledge` to prefer the project-type-aware template when a project type is configured (fall back to generic template when no type is set)

## Capabilities

### New Capabilities
- `template-deploy`: Deploy project-knowledge.yaml and .claude/rules/*.md from a project type's template into the target project, with additive-only safety and variant selection

### Modified Capabilities

## Impact

- `set-project-base`: new `deploy-templates` CLI subcommand + Python helper
- `wt-project` bash script: new `--template` flag on init, updated `init-knowledge` to be type-aware
- `set-project-web`: no code changes needed (templates already exist in package), but `pyproject.toml` must include template files in package data
