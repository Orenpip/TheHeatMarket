# COMPASS — Project Instructions for Claude

## Agent Usage (IMPORTANT)

Use the **planner** and **architect** subagents freely and proactively throughout this project:
- **planner** — for any new feature, before writing a single line of code
- **architect** — for any schema change, API design, or cross-cutting concern
- **code-reviewer** — immediately after writing or modifying code
- **tdd-guide** — for every new feature or bug fix (write tests first)
- **security-reviewer** — before any commit touching auth, input handling, or sensitive data

Do not wait to be asked. Spawn agents in parallel when tasks are independent.

## What This Project Is

COMPASS is a student career exploration platform for high schoolers. Students complete structured
reflection sessions every 3 weeks → AI synthesizes responses into signal profiles → counselors
see filtered dashboards → a pgvector map surfaces personalized career/major recommendations.

## Key Rules

- Next.js 15 App Router — all routes under `apps/web/app/`
- Prisma 6 WASM engine — never use `prisma migrate dev` or `prisma migrate reset`
- Migration workflow: `pnpm db:migrate-new <name>` → `pnpm db:migrate-deploy`
- Redis: use `redis.set(key, value, {ex: ttl})` NOT `redis.setex(key, ttl, value)`
- MapEdge API: return `source`/`target` for D3 forceLink (not `sourceId`/`targetId`)
- All API routes must use `apiError()` from `lib/auth.ts` for consistent error responses
- Rate limit every public-facing endpoint

## Architecture

```
compass/
├── apps/web/          — Next.js 15 App Router → Vercel
├── apps/ai-service/   — FastAPI Python → Railway
├── packages/db/       — Prisma 6 WASM + schema
├── packages/ui/       — Shared components
├── packages/types/    — Shared TypeScript types
└── packages/config/   — Shared tsconfig/eslint
```

## Current Roles

- Student — reflections, map, explore, profile, notifications
- Counselor — dashboard, student summaries, flags, meeting prep, opportunity management
- Admin — reflection templates
