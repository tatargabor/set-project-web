---
paths:
  - "src/lib/auth*"
  - "src/middleware*"
  - "src/app/**/login/**"
  - "src/app/**/register/**"
  - "src/app/api/auth/**"
---
# Auth Conventions

## Auth Library
- Use NextAuth.js v5 (Auth.js) — `next-auth@5`
- Use `auth()` for server-side session, NOT `getServerSession()`
- Use `useSession()` for client-side session access

## Role Checking
- Define project roles in auth config (e.g., USER, ADMIN)
- Use centralized role check helpers — never compare role strings inline
- Protected server actions: check auth/role at the top, before any logic
- Protected pages: use middleware or layout-level auth checks

## Middleware
- Protect routes selectively — specify exact matcher patterns
- Public routes (storefront, landing) must remain accessible
- Auth pages (login, register) must be accessible without auth

## Password & Credentials
- Passwords hashed with `bcrypt` (bcryptjs)
- Never log or expose password hashes
- JWT session strategy for stateless auth
