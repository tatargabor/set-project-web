---
paths:
  - "src/lib/auth*"
  - "src/middleware*"
  - "src/app/login/**"
  - "src/app/register/**"
  - "src/app/api/auth/**"
---
# Auth Conventions

## Role Hierarchy
- Roles: `user` < `admin` < `superadmin` < `platform_admin`
- Higher roles inherit all permissions of lower roles
- `platform_admin` is a separate axis — cross-tenant access

## Role Checking
- Use centralized role helpers: `hasRole()`, `requireRole()`, `canAccess()`
- Never check roles with string comparison directly
- Server actions: call `requireRole()` at the top, before any logic
- API routes: use middleware or `requireRole()` in handler

## Session Patterns
- Use `auth()` from NextAuth for server-side session access
- Use `useSession()` for client-side session access
- Never pass session tokens in URL parameters
- Session includes: `userId`, `tenantId`, `role`, `email`

## Impersonation
- Platform admins can impersonate tenant users
- Impersonation adds `impersonatedBy` to session
- All actions during impersonation are audit-logged with impersonator ID
- Impersonation banner must be visible in UI

## Password & Credentials
- Passwords hashed with `bcrypt` (cost factor 12+)
- Never log or expose password hashes
- Rate-limit login attempts per IP and per account

Full reference: `docs/design/auth-system.md`
