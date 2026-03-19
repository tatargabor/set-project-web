## Context

`wt-project init --project-type web` currently:
1. Registers the project in the set-core registry
2. Deploys set-core hooks/MCP/skills
3. Saves the project type to `set/plugins/project-type.yaml`

But the template files bundled in the project type package (e.g., `set_project_web/templates/nextjs/project-knowledge.yaml` and `rules/*.md`) are never copied to the target project. Users get the type registered but none of the domain knowledge deployed.

The system has two repos involved:
- **set-project-base** (Python): owns the `ProjectType` ABC, resolver, and CLI — this is where template deploy logic belongs
- **wt-project** (bash, in set-core): the user-facing CLI that orchestrates init — calls Python for type resolution

## Goals / Non-Goals

**Goals:**
- Deploy template files from project type packages into target projects during `wt-project init`
- Support template variant selection (`--template nextjs` vs `--template spa`)
- Additive-only by default (never overwrite existing files without `--force`)
- Make `init-knowledge` project-type-aware (use type's template instead of generic)
- Work for both new projects and existing projects adding a type

**Non-Goals:**
- Template customization/interpolation (variable substitution in templates) — templates are static files copied as-is
- Auto-detection of which template variant fits (user picks explicitly)
- Syncing templates after initial deploy (one-time copy, user owns the files after)
- Changes to the WebProjectType class itself (templates already exist)

## Decisions

### D1: Template deploy lives in set-project-base Python CLI

The Python package has native access to installed package resources via `importlib.resources` or `ProjectType.get_template_dir()`. The bash script already delegates to Python for `_resolve_project_type` and `_list_project_types`.

New subcommand: `set-project-base deploy-templates --project-dir . --type web --template nextjs [--force]`

Alternative considered: Pure bash implementation — rejected because locating Python package resource directories from bash is fragile and duplicates the entry_points resolution.

### D2: Bash calls Python for template deploy (same pattern as type resolution)

Add `_deploy_project_templates()` bash function that calls `set-project-base deploy-templates`. Called from `cmd_init` after `_save_project_type`, and from `cmd_init_knowledge` when a project type is configured.

### D3: Additive-only deploy with --force override

Default behavior:
- Skip files that already exist in target
- Print what was skipped for transparency
- `--force` flag overwrites existing files

This matches `deploy_wt_tools` behavior and is safe for existing projects.

### D4: Template file targets

Template files map to target locations:
```
templates/<variant>/project-knowledge.yaml  →  wt/knowledge/project-knowledge.yaml (or project root)
templates/<variant>/rules/*.md              →  .claude/rules/*.md
```

The Python function reads the template directory from `ProjectType.get_template_dir()` and walks it, preserving relative paths.

### D5: Default template selection

If `--template` is not specified but the project type has exactly one template, use it. If multiple templates exist, list them and ask the user to pick (or error with guidance).

### D6: Package data inclusion

`set-project-web/pyproject.toml` needs to include template files and other data files in the package distribution. Use `[tool.hatch.build.targets.wheel]` with `packages` or include patterns for the `templates/`, `directives/`, and `verification-rules/` directories.

## Risks / Trade-offs

- [Package data not included in wheel] → Ensure pyproject.toml has correct include patterns; add a test that verifies template files are accessible
- [User confusion about template vs project-type] → Clear help text: project-type = set of rules, template = starting files for a specific stack
- [Existing init-knowledge users] → Backward compatible: without a project type, init-knowledge behaves exactly as before
