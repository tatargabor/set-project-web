## Context

The wt-tools design-bridge (`lib/design/bridge.sh`) provides generic infrastructure: detecting design MCP servers in `.claude/settings.json`, exporting config for `run_claude --mcp-config`, and generating design-aware prompt sections for the planner. This works for any project type — the detection patterns (figma, penpot, sketch, zeplin) are universal.

However, consumer web projects currently have no automated way to:
1. Register a design MCP server during project init
2. Get web-specific guidance on mapping design outputs to the web stack (Tailwind CSS tokens, shadcn/ui components)
3. Declare design-related cross-cutting files in their project knowledge

## Goals / Non-Goals

**Goals:**
- Automated design tool setup during `wt-project-web init` (interactive prompt → MCP registration + orchestration.yaml)
- Web-specific design integration rule templates for both nextjs and spa templates
- Design-related cross-cutting file entries in project-knowledge.yaml

**Non-Goals:**
- Modifying the wt-tools bridge.sh — the core infrastructure stays as-is
- Supporting non-MCP design integrations (e.g., direct Figma REST API)
- Auto-generating code from design files — agents query the design tool at runtime

## Decisions

### D1: Interactive design prompt in CLI init

The `init` command will ask "Do you have a Figma design file? (y/n)". If yes, it prompts for the URL, runs `claude mcp add figma https://mcp.figma.com/mcp` via subprocess, and writes `design_file: <url>` to `.claude/orchestration.yaml`.

**Why not auto-detect?** At init time there's nothing to detect — the MCP hasn't been registered yet. The init is the right moment to ask because the user is already in setup mode.

**Why subprocess for `claude mcp add`?** Writing settings.json directly is fragile — the `claude` CLI handles the correct format, merging with existing servers, and platform differences.

### D2: Separate design-integration.md rule per template

Each template gets its own `rules/design-integration.md` with path-scoped activation. The nextjs version references tailwind.config.ts, shadcn/ui conventions, and CSS variables. The spa version is lighter — just design tokens and component mapping without framework-specific details.

**Why not a single shared rule?** Path scoping differs between templates, and the web stack specifics (tailwind vs plain CSS, shadcn vs generic components) justify separate files. Keeps each under the 100-line target.

### D3: Design files as cross-cutting entries

`project-knowledge.yaml` gets a `design` entry under `cross_cutting_files` pointing to `tailwind.config.ts` and `src/styles/tokens.*` (or framework equivalent). This tells the orchestrator that design token changes are cross-cutting — multiple features may depend on them.

**Why these files?** Design tokens land in tailwind config (colors, spacing, fonts) and optionally in a CSS custom properties file. These are the files that bridge design ↔ code.

### D4: Optional — skip silently if user declines

If the user answers "no" to the Figma prompt, init proceeds normally with no design-related side effects. The rule template is still deployed (it's part of the template), but without an MCP server registered, the wt-tools bridge self-gates and agents ignore the design rule.

## Risks / Trade-offs

- **[Figma MCP URL may change]** → The URL `https://mcp.figma.com/mcp` is hardcoded. If Figma changes it, the init command needs updating. Mitigation: the URL is in one place (cli.py), easy to update.
- **[`claude` CLI must be on PATH]** → `claude mcp add` requires the Claude CLI to be installed. Mitigation: this is a wt-tools project — Claude CLI is a prerequisite. Fail gracefully with a helpful error message if not found.
- **[Penpot/Sketch/Zeplin not covered in init]** → Only Figma has a known public MCP endpoint. Mitigation: the prompt can be extended later for other tools. The rule template is tool-agnostic ("query the design tool"), only init is Figma-specific for now.
