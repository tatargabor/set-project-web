## 1. Template rule files

- [x] 1.1 Create `templates/nextjs/rules/design-integration.md` with path-scoped activation (`src/components/**`, `src/app/**/*.tsx`) — Tailwind token mapping, shadcn/ui component mapping, CSS custom properties guidance, design_gap flagging
- [x] 1.2 Create `templates/spa/rules/design-integration.md` with generic guidance — no framework-specific references, generic "token system" and "component library" terminology
- [x] 1.3 Update `templates/nextjs/manifest.yaml` to include `rules/design-integration.md`
- [x] 1.4 Update `templates/spa/manifest.yaml` to include `rules/design-integration.md`

## 2. Project knowledge updates

- [x] 2.1 Add `design_tokens` entry to `cross_cutting_files` in `templates/nextjs/project-knowledge.yaml` (`tailwind.config.ts`, `src/styles/tokens.*`)
- [x] 2.2 Add `design_tokens` entry to `cross_cutting_files` in `templates/spa/project-knowledge.yaml` (generic token file patterns)

## 3. CLI design setup

- [x] 3.1 Add `--no-design` flag to the init argument parser
- [x] 3.2 Implement interactive design prompt function: ask y/n for Figma, prompt for URL if yes
- [x] 3.3 Implement MCP registration: run `claude mcp add figma https://mcp.figma.com/mcp` via subprocess, handle Claude CLI not found gracefully
- [x] 3.4 Implement orchestration.yaml write: create or merge `design_file` key into `.claude/orchestration.yaml` in target directory
- [x] 3.5 Wire design setup into `init_project()` flow — after template copy, before final summary

## 4. Verification

- [x] 4.1 Verify nextjs design-integration.md is under 100 lines and has correct path frontmatter
- [x] 4.2 Verify spa design-integration.md is framework-agnostic (no Next.js/Tailwind/shadcn references)
- [x] 4.3 Verify `--no-design` flag skips the interactive prompt
- [x] 4.4 Verify init with design setup creates correct settings.json and orchestration.yaml entries
- [x] 4.5 Verify init without Claude CLI prints warning and continues without error
