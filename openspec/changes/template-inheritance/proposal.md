## Why

When `wt-project init --project-type web --template nextjs` runs, only the web/nextjs template files are deployed. The base project type's template (universal rules like data-privacy) is ignored because `deploy_templates()` only processes a single project type — it has no awareness of the parent chain. This means base-level rules that should apply to every project are not inherited, and users must manually opt into them. As the base template grows with more "modern Claude" rules (code quality, testing, git conventions), every derived project type would need to duplicate them.

Additionally, there's no safe update mechanism — re-running init skips existing files (additive-only), so template improvements never reach existing projects. We need a managed-file convention so templates can be updated while respecting user customizations.

## What Changes

- `deploy_templates()` walks the parent chain (web → base) and deploys templates in parent-first order, with child templates overriding parent files when names collide
- Optional modules from all ancestors are merged and presented together during init
- Template-deployed files get a `<!-- wt-managed -->` header — re-init updates managed files, skips user-owned files (header removed)
- The base/default template gains new core rules for universal Claude best practices
- `_deploy_project_templates()` in the bash script calls deploy for each ancestor in the chain

## Capabilities

### New Capabilities
- `template-inheritance`: Parent chain resolution and multi-layer template deployment with file-level override semantics
- `managed-file-updates`: Header-based ownership tracking so re-init can safely update template files without destroying user customizations

### Modified Capabilities
- `template-deploy`: Deploy logic extended to support parent chain traversal and managed-file headers

## Impact

- **set-project-base**: `deploy.py` — new `deploy_templates_with_inheritance()` function or extension of existing `deploy_templates()`, managed-file header detection logic
- **set-project-base**: `cli.py` — `deploy-templates` command gains `--update` mode that respects managed headers
- **set-project-base**: `base.py` — parent chain resolution helper (load parent type via entry points)
- **set-project-base**: `templates/default/` — new core rule files for base conventions
- **set-core**: `bin/wt-project` — `_deploy_project_templates()` updated to pass parent chain or let Python handle it
- **set-project-web**: No code changes needed (inherits automatically via `parent: base` in ProjectTypeInfo)
