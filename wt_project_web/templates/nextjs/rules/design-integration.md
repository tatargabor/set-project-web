---
paths:
  - "src/components/**"
  - "src/app/**/*.tsx"
---
# Design Integration

These rules apply when a design MCP (e.g., Figma) is registered. If no design tool is available, skip this file — agents self-gate.

## Before Implementing UI

- Query the design tool for the relevant frame/page before writing component code
- If the required frame is MISSING from the design, flag it as a `design_gap` ambiguity — do not guess layout or styling

## Design Token Mapping

- Map design colors → `tailwind.config.ts` `theme.extend.colors` using CSS custom properties
- Map design spacing/sizing → Tailwind spacing scale or custom values in config
- Map design typography → `tailwind.config.ts` `theme.extend.fontFamily` / `fontSize`
- Map design shadows → `tailwind.config.ts` `theme.extend.boxShadow`
- For tokens not covered by Tailwind defaults, use CSS custom properties: `var(--token-name)`
- Token source of truth: `tailwind.config.ts` and `src/styles/tokens.*` — never hardcode values

## Component Mapping

- Map design components → shadcn/ui variants where a match exists
- Use existing shadcn/ui components before creating custom ones
- Match design states (hover, focus, disabled, error) to component variant props
- If a design component has no shadcn/ui equivalent, create in `src/components/` following the same pattern (Radix + Tailwind + `cn()`)

## Responsive Behavior

- Check design for mobile/tablet/desktop breakpoint frames
- Map breakpoint-specific layouts to Tailwind responsive prefixes (`sm:`, `md:`, `lg:`)
- If only one breakpoint is designed, implement mobile-first and flag missing breakpoints
