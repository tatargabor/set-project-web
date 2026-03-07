---
paths:
  - "prisma/**"
  - "src/lib/prisma*"
  - "docs/design/data-model*"
---
# Data Model Conventions

## Prisma Schema
- IDs: use `cuid()` default — never auto-increment
- Table mapping: `@@map("snake_case_table")` for all models
- Field mapping: `@map("snake_case_field")` for camelCase fields
- Every model needs `createdAt` and `updatedAt` timestamps
- Soft delete: use `deletedAt DateTime?` — never hard delete user data

## Tenant Scoping
- Every business model MUST have `tenantId String` field
- Add `@@index([tenantId])` to all tenant-scoped models
- Queries MUST filter by `tenantId` — no cross-tenant data leaks
- Exceptions: platform-level models (Tenant, PlatformConfig)

## Migrations
- Run `prisma migrate dev --name descriptive-name` to create migrations
- Migration names: `add_user_roles`, `create_invoice_table` (snake_case, descriptive)
- Review generated SQL before committing
- Never edit deployed migrations — create new ones to fix issues
- Update `docs/design/data-model.md` when adding/modifying models

## State Machines
- Use enum fields for states: `status InvoiceStatus`
- Define valid transitions in code, not in schema
- Log state transitions with `logActivity()`

## Relations
- Use explicit relation names for self-referencing or ambiguous relations
- Cascade deletes only for true child entities (e.g., InvoiceItem → Invoice)
- Set `onDelete: SetNull` for optional references

Full reference: `docs/design/data-model.md`
