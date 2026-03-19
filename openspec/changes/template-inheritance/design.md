## Context

Template deployment currently operates on a single project type — `deploy_templates()` receives one `ProjectType` instance and deploys its template files. The `ProjectType` ABC has a `parent` field (`ProjectTypeInfo.parent`) but it's purely informational — the deploy system ignores it. This means base-level rules (data-privacy, future code-quality conventions) are not inherited by derived project types like `web`.

Additionally, template files are deployed additive-only (skip if exists). Once deployed, they never update — even when the template packages are upgraded. There's no mechanism to distinguish "user customized this file" from "this file was deployed and never touched."

Three repos are involved: `set-project-base` (deploy logic + base templates), `set-project-web` (web templates), `set-core` (bash CLI).

## Goals / Non-Goals

**Goals:**
- Parent chain traversal: `web → base` template inheritance with parent-first deploy order
- Module merging: optional modules from all ancestors presented together
- Managed-file updates: template files can be safely updated on re-init without destroying user customizations
- Extensible: works for any future project type chain depth (e.g., `nextjs-saas → web → base`)

**Non-Goals:**
- Merging file contents (e.g., combining base and web project-knowledge.yaml sections) — child simply overrides parent for same-named files
- Auto-updating existing projects in the background — update requires explicit `wt-project init` re-run
- Versioned migrations (tracking which template version was last deployed) — managed header is sufficient

## Decisions

### 1. Parent chain resolution lives in Python (deploy.py), not bash

**Why:** The parent chain requires loading project type classes via entry points, which is already Python infrastructure. The bash script calls `deploy-templates` once — Python handles the chain internally.

**Alternative considered:** Bash script resolves chain and calls deploy-templates N times. Rejected because: duplicates entry point resolution logic, can't merge module lists across ancestors, and would need N subprocess calls instead of one.

### 2. Deploy order: parent-first, child overrides

When deploying `web/nextjs` with parent `base`:
1. Deploy `base/default` core files
2. Deploy `web/nextjs` core files (overwrite any collisions from step 1)

This means the child's `project-knowledge.yaml` (with real cross-cutting files) replaces the base's empty skeleton. Rules files don't collide (different names).

**Alternative considered:** Child-first (skip if exists). Rejected because base files would never deploy if child has same-named file.

### 3. Managed-file header for update safety

Template-deployed `.md` files get a comment header:
```
<!-- wt-managed: base/default -->
```

On re-init with `--force` or `--update`:
- File has `wt-managed` header → **update** (overwrite with latest template)
- File has no header (user removed it or wrote from scratch) → **skip** (user owns it)
- File doesn't exist → **deploy** (new file)

This is opt-out: users remove the header to take ownership. Default is managed.

Non-`.md` files (e.g., `project-knowledge.yaml`) use a YAML comment: `# wt-managed: web/nextjs`

**Alternative considered:** Git-based diffing (check if file was modified since deploy). Rejected because: requires tracking deploy timestamps, doesn't work across branches, and is fragile with reformatting.

### 4. Module merging across ancestors

When presenting optional modules during init, all ancestors' modules are shown with their source:
```
Optional modules available:
  data-privacy (base) — Data privacy & retention
  integrations (web)  — External API patterns
```

Module IDs are globally unique across the chain. If a collision occurs (same module ID in parent and child), child wins.

Selected modules are tracked in `project-type.yaml` with their source:
```yaml
modules:
  - data-privacy
  - integrations
```

The deploy system routes each module to its source template for file resolution.

### 5. The `deploy_templates()` function gains a `parent_chain` parameter

Rather than changing the function signature radically, add a new top-level function `deploy_with_inheritance()` that:
1. Resolves the parent chain via entry points
2. Calls `deploy_templates()` for each ancestor in order
3. Merges module availability across ancestors
4. Handles managed-file logic

The existing `deploy_templates()` remains unchanged for backward compatibility.

## Risks / Trade-offs

- **[Risk] Module ID collision across ancestors** → Mitigation: child wins, log warning. Convention: prefix module IDs if ambiguous.
- **[Risk] Managed header stripped accidentally by editor** → Mitigation: header is an HTML comment, invisible in rendered markdown. Editors don't strip these.
- **[Risk] Deep parent chains causing slow init** → Mitigation: realistic depth is 2-3 levels max. Each level is a fast file copy.
- **[Trade-off] Child completely overrides parent for same-named files** → No content merging. If base has a richer `project-knowledge.yaml` in the future, it won't merge with web's version. This is acceptable — the child should be the authoritative version.
