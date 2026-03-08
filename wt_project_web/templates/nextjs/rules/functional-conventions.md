---
paths:
  - "src/app/**"
  - "src/lib/**"
  - "src/actions/**"
---
# Functional Conventions

## Server Actions
- Return `{ success, error? }` — never throw from actions
- Call `revalidatePath()` after mutations
- Protected actions: check auth at the top before any logic
- Place in `src/actions/` or co-locate in feature directories

## Database Patterns (Prisma)
- Use singleton PrismaClient — import from `src/lib/prisma.ts`
- globalThis pattern for dev hot reload (prevent connection exhaustion)
- Use transactions (`prisma.$transaction`) for multi-table mutations
- Never use `deleteMany` without a WHERE clause

## Form Patterns
- **Pattern A (Dialog)**: Form in dialog → server action → close dialog → revalidate
- **Pattern B (Inline)**: Inline form/toggle → server action → revalidate
- Use `react-hook-form` + `zod` for validation
- Share validation schemas between client and server

## Error Handling
- Server actions return `{ success: false, error: string }` — never throw
- API routes return proper HTTP status codes with JSON error bodies
- Use `try/catch` at the action boundary, not inside utility functions
