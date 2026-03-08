---
paths:
  - "tests/**"
  - "**/*.test.*"
  - "**/*.spec.*"
  - "playwright.config.*"
---
# Testing Conventions

## Two-Level Testing Strategy
- **Unit tests** (Jest/Vitest): test pure logic, utilities, validation schemas. Run pre-merge via `test_command`.
- **Functional tests** (Playwright): test real user flows against a running dev server. Run post-merge via `smoke_command`.

## Unit Tests — What to Mock, What Not To
- DO mock: external APIs, email services, payment gateways
- DO NOT mock: Next.js runtime APIs (cookies(), headers(), redirect(), revalidatePath())
- DO NOT mock: database queries — use a test database or in-memory SQLite
- If a function calls cookies() or headers(), test it via Playwright, not Jest

## Playwright Functional Tests
- Each user-facing feature change MUST include Playwright test specs
- Test specs describe real user flows: navigate to page → interact with UI → verify outcome
- Tests run against `localhost` with a real dev server (not mocked)
- Use page object pattern for reusable selectors
- Test both happy path AND error states (invalid form data, unauthorized access)
- Auth-protected routes: test that unauthenticated users are redirected to login
- Form submissions: test with real data, verify server-side effects (DB records, redirects)

## Test File Organization
- Unit tests: co-located with source (`src/**/*.test.ts`) or `__tests__/`
- Playwright tests: `tests/e2e/*.spec.ts` (one file per feature area)
- Shared fixtures: `tests/e2e/fixtures/`

## What the Planner Must Specify
For each feature change, the planner scope MUST include a "Functional tests:" section listing:
- Pages to visit and expected initial state
- User interactions (click, fill, select, navigate)
- Test data (form values, credentials)
- Expected outcomes (visible text, URL changes, DB effects)
- Error scenarios to cover
