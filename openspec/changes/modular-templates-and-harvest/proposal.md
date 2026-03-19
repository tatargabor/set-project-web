## Why

Template deploy (`wt-project init --project-type web --template nextjs`) currently deploys ALL template files to every project. When rules are harvested from production projects back into templates, they get pushed to every future (and re-inited) project — even projects that don't need them. There's no way to selectively opt into subsets of a template's knowledge, and no tooling to generalize production rules back into templates.

## What Changes

- Add `manifest.yaml` to templates defining **core** (always deployed) and **optional modules** (deployed on request)
- Update `deploy_templates()` to read the manifest and support module selection
- Add `--modules` flag to `wt-project init` for CLI-based module selection
- Track selected modules in `set/plugins/project-type.yaml` so re-init deploys the same set
- Add a `harvest` skill that compares a source project's rules against the template, classifies candidates (base/web/skip), generalizes them, and writes them as optional modules

## Capabilities

### New Capabilities
- `modular-templates`: Template manifest with core/optional module structure, module selection during deploy, module tracking per project
- `template-harvest`: Diff-based comparison of project rules vs template, AI-driven classification and generalization, writing harvested rules as optional template modules

### Modified Capabilities
- `template-deploy`: Deploy now reads manifest.yaml, supports `--modules` flag, only deploys core + selected modules instead of all files

## Impact

- `set-project-base`: `deploy.py` updated to read manifest, new `harvest.py` module
- `set-project-web`: `manifest.yaml` added to nextjs and spa templates, existing rules categorized as core vs optional
- `wt-project` bash script: `--modules` flag on init, module tracking in project-type.yaml
- `set-core`: new `/wt:harvest` skill definition
