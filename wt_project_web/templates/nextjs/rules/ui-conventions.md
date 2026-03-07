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
- Page layout: `<PageHeader>` + content area
- Use responsive containers — never hardcode pixel widths
- Sidebar items use `titleKey` for i18n — never hardcode labels

## Button Variant Policy
- `variant="ghost"` → icon-only, NO text content
- `variant="outline"` → secondary actions with text
- `variant="default"` → primary actions
- `variant="destructive"` → delete/remove actions, always with confirmation dialog

## Table Conventions
- Use `@tanstack/react-table` via shadcn DataTable
- Column headers must be translatable (i18n keys)
- Include loading skeleton states
- Pagination server-side for datasets > 50 rows

## Dialog Patterns
- Use shadcn `Dialog` component
- Forms inside dialogs follow Pattern A (see functional-conventions)
- Dialogs close on successful submit, stay open on error
- Confirmation dialogs for destructive actions

## i18n Rules
- Every user-visible string MUST use `useTranslations()` or `getTranslations()`
- Never hardcode Hungarian or English strings in components
- Key naming: `section.subsection.label` (dot-separated, lowercase)
- All keys must exist in ALL locale files (enforced by i18n-completeness rule)

## File Size
- Components should stay under 400 lines
- Split large components: extract hooks, sub-components, or utilities

Full reference: `docs/design/ui-patterns.md`
