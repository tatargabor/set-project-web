---
paths:
  - "src/app/**"
  - "src/lib/**"
  - "src/actions/**"
---
# Functional Conventions

## Server Actions
- Every server action MUST start with `await auth()` guard
- Return `{ success, error? }` — never throw from actions
- Call `revalidatePath()` after mutations
- Call `logActivity()` for audit-relevant operations
- Place in `src/actions/` or co-locate in feature directories

## Database Patterns (Prisma)
- Use singleton PrismaClient — import from `src/lib/prisma.ts`
- Every query MUST scope by `tenantId` (except platform-admin queries)
- Use transactions for multi-table mutations
- Never use `deleteMany` without a WHERE clause

## Form Patterns
- **Pattern A (Dialog)**: Form in dialog → server action → close dialog → revalidate
- **Pattern B (Toggle)**: Inline toggle → server action → optimistic update → revalidate
- Use `react-hook-form` + `zod` for validation
- Share validation schemas between client and server

## Error Handling
- Server actions return `{ success: false, error: string }` — never throw
- API routes return proper HTTP status codes with JSON error bodies
- Use `try/catch` at the action boundary, not inside utility functions

Full reference: `docs/design/functional-patterns.md`
