## ADDED Requirements

### Requirement: Interactive design tool prompt during init

The `init` command SHALL prompt the user: "Do you have a Figma design file? (y/n)". If the user answers yes, the system SHALL prompt for the Figma file URL.

#### Scenario: User provides Figma URL
- **WHEN** user runs `wt-project-web init --type nextjs` and answers "yes" to the Figma prompt
- **AND** provides a URL like `https://www.figma.com/file/ABC123/MyProject`
- **THEN** the system registers the Figma MCP server
- **AND** writes `design_file: <url>` to `.claude/orchestration.yaml` in the target directory

#### Scenario: User declines design setup
- **WHEN** user runs `wt-project-web init --type nextjs` and answers "no" to the Figma prompt
- **THEN** no MCP registration occurs
- **AND** no `orchestration.yaml` is created or modified
- **AND** init proceeds normally with all other template files

#### Scenario: Non-interactive mode
- **WHEN** user runs init with `--no-design` flag
- **THEN** the design prompt is skipped entirely
- **AND** init proceeds without design setup

### Requirement: MCP server registration via Claude CLI

The system SHALL register the Figma MCP server by invoking `claude mcp add figma https://mcp.figma.com/mcp` as a subprocess targeting the project's `.claude/settings.json`.

#### Scenario: Successful MCP registration
- **WHEN** the Claude CLI is available on PATH
- **AND** the user provided a Figma URL
- **THEN** the system runs `claude mcp add figma https://mcp.figma.com/mcp`
- **AND** `.claude/settings.json` contains a `figma` entry under `mcpServers`

#### Scenario: Claude CLI not found
- **WHEN** the Claude CLI is not available on PATH
- **THEN** the system prints a warning: "Claude CLI not found — skipping MCP registration. Run manually: claude mcp add figma https://mcp.figma.com/mcp"
- **AND** init continues without error

### Requirement: Orchestration YAML design file reference

The system SHALL write the design file reference to `.claude/orchestration.yaml` in the target directory. If the file already exists, the system SHALL merge the `design_file` key without overwriting other content.

#### Scenario: New orchestration.yaml
- **WHEN** no `.claude/orchestration.yaml` exists in the target directory
- **THEN** the system creates it with `design_file: <url>`

#### Scenario: Existing orchestration.yaml
- **WHEN** `.claude/orchestration.yaml` already exists with other keys
- **THEN** the system adds or updates `design_file: <url>` without removing existing keys

### Requirement: Design integration rule template — nextjs

The nextjs template SHALL include a `rules/design-integration.md` file with path-scoped activation for UI-related source files. The rule SHALL instruct agents to:
- Query the design MCP for component specs and design tokens before implementing UI
- Map design tokens to Tailwind CSS configuration (`tailwind.config.ts` theme section)
- Map design components to shadcn/ui component variants
- Use CSS custom properties (`--var-name`) for design tokens not covered by Tailwind defaults
- Flag missing design frames as `design_gap` ambiguities

#### Scenario: Rule activates for UI files
- **WHEN** an agent edits a file matching `src/components/**` or `src/app/**/*.tsx`
- **THEN** the design-integration rule is loaded alongside ui-conventions

#### Scenario: Rule is inert without design MCP
- **WHEN** no design MCP is registered in `.claude/settings.json`
- **THEN** the rule content is loaded but agents self-gate (no design tool to query)
- **AND** no errors or warnings are produced

### Requirement: Design integration rule template — spa

The spa template SHALL include a `rules/design-integration.md` with generic guidance (no Next.js or shadcn/ui specifics). It SHALL cover:
- Query design tool for layout and component specifications
- Map design tokens to CSS custom properties or framework-specific token system
- Maintain component naming consistency with design file naming

#### Scenario: SPA rule is framework-agnostic
- **WHEN** a project uses the spa template
- **THEN** the design-integration rule does not reference Next.js, Tailwind, or shadcn/ui
- **AND** uses generic terms like "token system" and "component library"
