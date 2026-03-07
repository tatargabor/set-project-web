---
paths:
  - "Dockerfile"
  - "docker-compose*"
  - ".github/**"
  - "railway*"
  - "next.config*"
---
# Deployment Conventions

## Migration-First Deploy
- Migrations run BEFORE the new application version starts
- Deploy sequence: migrate → build → start
- Never rely on `prisma db push` in production — always use migrations

## Docker
- Multi-stage build: deps → build → runtime
- Use `.dockerignore` to exclude `node_modules/`, `.next/`, `.git/`
- Pin Node.js version in Dockerfile (match project's `.nvmrc`)
- Health check endpoint: `/api/health`

## Port Allocation
- Production: port from `PORT` env var
- Dev server: `3000` (default Next.js)
- Smoke tests: `3002` (separate instance)
- DB: `5432` (PostgreSQL)

## Environment Variables
- `.env.example` — all variables with placeholder values, committed
- `.env` — actual values, gitignored
- `.env.test` — test-specific overrides, committed
- Secrets MUST use platform secret management (Railway, Vercel, etc.)
- Never commit actual secrets — use placeholders in examples

## CI/CD
- Pre-merge: lint, type-check, unit tests
- Post-merge: build, migrate, deploy, smoke test
- Smoke test failure: auto-rollback or alert (configurable)

Full reference: `docs/design/deployment.md`
