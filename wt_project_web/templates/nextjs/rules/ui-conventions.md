---
paths:
  - "src/components/**"
  - "src/app/**/*.tsx"
---
# UI Conventions

## Component Stack
- Use shadcn/ui components as the base layer
- Import from `@/components/ui/` — never use raw Radix primitives directly
- Icons: use `lucide-react` exclusively

## Layout Patterns
- Page layout: consistent header/content structure
- Use responsive containers — never hardcode pixel widths
- Mobile-first: design for small screens, enhance for larger

## Button Variant Policy
- `variant="ghost"` → icon-only, NO text content
- `variant="outline"` → secondary actions with text
- `variant="default"` → primary actions
- `variant="destructive"` → delete/remove actions, always with confirmation dialog

## Table Conventions
- Use `@tanstack/react-table` via shadcn DataTable
- Include loading skeleton states
- Pagination server-side for datasets > 50 rows

## Dialog Patterns
- Use shadcn `Dialog` component
- Forms inside dialogs follow Pattern A (see functional-conventions)
- Dialogs close on successful submit, stay open on error
- Confirmation dialogs for destructive actions

## Components by Default
- All components are Server Components by default
- Add `"use client"` only when needed: event handlers, hooks, browser APIs
- Keep client components small — extract data fetching to server parents

## File Size
- Components should stay under 400 lines
- Split large components: extract hooks, sub-components, or utilities
