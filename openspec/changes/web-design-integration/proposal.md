## Why

The wt-tools design-bridge provides infrastructure for design tool integration (detection, MCP config export, prompt enrichment), but consumer web projects have no automated way to set it up. Users must manually run `claude mcp add`, edit `orchestration.yaml`, and agents lack web-specific guidance on mapping design tokens to Tailwind or Figma components to shadcn/ui.

## What Changes

- Add `rules/design-integration.md` to the nextjs template — path-scoped rule that guides agents to query design MCP for tokens/components and map them to the web stack (tailwind.config.ts, shadcn/ui)
- Add `rules/design-integration.md` to the spa template — lighter version without Next.js-specific guidance
- Extend `project-knowledge.yaml` in both templates with a `design` entry in `cross_cutting_files` (e.g., `tailwind.config.ts`, `src/styles/tokens.*`)
- Add init-time design setup to the CLI: prompt for Figma file URL, register MCP server via `claude mcp add`, and write `design_file` to `.claude/orchestration.yaml`

## Capabilities

### New Capabilities
- `web-design-setup`: Init-time design tool registration (interactive Figma prompt, MCP add, orchestration.yaml write) and web-specific design integration rule templates

### Modified Capabilities
- `web-knowledge-templates`: Adding design-related cross-cutting files and a new rule file to both nextjs and spa templates

## Impact

- `wt_project_web/cli.py` — new interactive design setup step during `init`
- `wt_project_web/templates/nextjs/rules/design-integration.md` — new file
- `wt_project_web/templates/nextjs/project-knowledge.yaml` — new `design` entry
- `wt_project_web/templates/spa/rules/design-integration.md` — new file
- `wt_project_web/templates/spa/project-knowledge.yaml` — new `design` entry
- No changes to wt-tools — the bridge.sh infrastructure stays as-is
