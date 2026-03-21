# COMPASS Project — Complete Summary
MAR 15 ~3:20 AM

## What COMPASS Is

Student career exploration platform for high schoolers. Students complete structured reflection sessions every 3 weeks → AI (Claude + Voyage AI) synthesizes responses into "signal profiles" (interest clusters, character signals, trajectory shifts, breadth score, compressed summary) → counselors see filtered dashboards → a pgvector map surfaces personalized career/major recommendations → an Explore tab shows AI-ranked opportunities.

---

## Architecture

Monorepo (Turborepo + pnpm workspaces):
```
compass/
├── apps/web/          — Next.js 15 App Router (student + counselor + admin UI) → Vercel
├── apps/ai-service/   — FastAPI Python (synthesis, embeddings, prompts, explain-match) → Railway
├── packages/db/       — Prisma 6 WASM + Supabase schema
├── packages/ui/       — Shared UI components
├── packages/types/    — Shared TypeScript types
├── packages/config/   — Shared tsconfig/eslint
├── turbo.json         — Turborepo task config (ANTHROPIC_API_KEY now listed)
└── CLAUDE.md          — Project-level Claude instructions
```

**Tech stack:** Next.js 15.5.12, TypeScript, Tailwind, Prisma 6 (WASM), Supabase (PostgreSQL + pgvector), Clerk (student/counselor/admin roles), Upstash Redis + QStash, Claude claude-sonnet-4-6 (synthesis, direct via ANTHROPIC_API_KEY in Vercel), Voyage AI (1024-dim embeddings via Railway AI service), Vercel (web), Railway (AI service).

---

## Database Schema (16 models)

Student, Counselor, School, ReflectionSession, ReflectionTemplate, Activity, Reflection,
SignalProfile, StudentPrivacySettings, MapNode (pgvector), MapEdge, Notification,
NotificationPreferences, PeerGroup, PeerGroupMember, **Opportunity**, **StudentOpportunityInteraction**.

**Key constraints:**
- `SignalProfile.@@unique([studentId, sessionId])` — idempotent QStash synthesis
- `MapEdge` uses `sourceId`/`targetId` — API maps to `source`/`target` for D3
- `StudentOpportunityInteraction.@@unique([studentId, opportunityId])` — upsert safe
- Opportunity scope: GLOBAL (admin) or SCHOOL (counselor) — `schoolId` NULL for GLOBAL

**4 migrations applied:**
1. `0_init`
2. `add-signal-profile-session-id-unique`
3. `signal-profile-not-null-add-share-summary`
4. `20260315070000_add-opportunities` ✅ applied via Supabase SQL editor + _prisma_migrations INSERT

**Migration workflow:**
```bash
cd packages/db
# Write SQL manually → place in prisma/migrations/<timestamp>_<name>/migration.sql
# Run SQL in Supabase SQL editor
# INSERT into _prisma_migrations to track it
# Never use: prisma migrate dev / prisma migrate reset
```

---

## Deployment

### Web (Vercel) — compass-sigma-two.vercel.app
- Root Directory blank; `vercel.json` at repo root
- Prisma WASM engine + custom webpack loader
- `pg Pool` with `DIRECT_URL`, `rejectUnauthorized: false`
- `force-dynamic` on root layout, `outputFileTracingRoot` at top-level of next.config
- **Synthesis runs directly via `lib/synthesize.ts` → Anthropic SDK → ANTHROPIC_API_KEY in Vercel**
- QStash fallback if direct synthesis fails

### AI Service (Railway)
- Root Dir: `apps/ai-service`, Watch Paths: `apps/ai-service/**`, Port: 8000
- Protected by `X-Service-Key` header
- Endpoints: /embed, /synthesize-profile, /reflection-prompts, /generate-notification, /meeting-prep, /explain-match

### Required Vercel Env Vars
DATABASE_URL, DIRECT_URL, NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY, CLERK_SECRET_KEY,
CLERK_WEBHOOK_SECRET, UPSTASH_REDIS_REST_URL, UPSTASH_REDIS_REST_TOKEN, QSTASH_TOKEN,
QSTASH_CURRENT_SIGNING_KEY, QSTASH_NEXT_SIGNING_KEY, AI_SERVICE_URL, AI_SERVICE_SECRET_KEY,
NEXT_PUBLIC_APP_URL, **ANTHROPIC_API_KEY**

### Required Railway Env Vars
ANTHROPIC_API_KEY, VOYAGE_API_KEY, DATABASE_URL (direct port 5432), AI_SERVICE_SECRET_KEY,
APP_URL (Vercel domain, for CORS)

---

## API Routes (40 routes)

**Student:** /api/sessions, /api/sessions/[id], /api/sessions/[id]/submit, /api/sessions/prompts,
/api/reflections, /api/reflections/[id], /api/activities, /api/activities/[id],
/api/students/onboarding, /api/students/profile, /api/students/signal-profile,
/api/notifications, /api/notifications/[id]/read, /api/notifications/[id]/acted,
/api/notifications/preferences, /api/privacy, /api/privacy/reset, /api/privacy/audit,
/api/export, /api/export/delete, /api/map/nodes, /api/map/nodes/[id],
/api/map/personalized, /api/map/search,
**/api/explore, /api/explore/[id]/interact**

**Counselor:** /api/counselor/students, /api/counselor/students/[id]/summary,
/api/counselor/students/[id]/meeting-prep, /api/counselor/flags,
**/api/counselor/opportunities, /api/counselor/opportunities/[id]**

**Admin:** /api/admin/templates, /api/admin/templates/[id],
**/api/admin/retrigger-synthesis** (student auth — any student can re-run their own synthesis)

**Webhooks:** /api/webhooks/clerk, /api/webhooks/qstash
QStash jobs: POST_SESSION_SYNTHESIS, WEEKLY_NUDGE_SWEEP, OPPORTUNITY_SWEEP, EMBED_PROFILE, **EMBED_OPPORTUNITY**

---

## Pages

**Student:** / (home), /map, /explore, /reflect, /reflect/[sessionId],
/reflect/[sessionId]/complete, /reflections, /profile, /onboarding

**Counselor:** /dashboard, /flags, /students/[id], /opportunities

**Admin:** /templates

**Auth:** /sign-in, /sign-up | **Other:** /map-embed

---

## Key Files
- `apps/web/lib/auth.ts` — AuthError + apiError + requireStudent/Counselor/Admin
- `apps/web/lib/redis.ts` — Redis client + rateLimiters + CACHE_KEYS/TTL (incl. explore)
- `apps/web/lib/synthesize.ts` — Direct Claude synthesis (ANTHROPIC_API_KEY)
- `apps/web/lib/ai-service.ts` — HTTP client for Railway (embed, meeting-prep, explain-match)
- `apps/web/lib/constants.ts` — COOLDOWN_DAYS = 21
- `apps/web/lib/utils.ts` — getISOWeekKey() UTC ISO 8601
- `apps/web/app/api/webhooks/qstash/route.ts` — all background jobs
- `packages/db/prisma/schema.prisma` — 16-model schema
- `apps/ai-service/app/main.py` — FastAPI entry

---

## What's Still Open

1. **Explore needs data** — no Opportunity records yet; counselors must add via /opportunities
2. **MapCanvas double-fetch** — personalized=false still fetches wrong endpoint for edges
3. **Map nodes need seeding** — no MapNode records; map shows empty state
4. **More tests** — 32 tests cover core logic; API routes + new explore code need coverage
5. **maxDuration on QStash webhook** — already set to 60s ✅
6. **APP_URL in Railway** — CORS needs correct Vercel domain set by user
7. **Clerk webhook URL** — verify matches compass-sigma-two.vercel.app in Clerk dashboard

## Agent Instructions
- Use **planner** agent before any new feature
- Use **architect** agent for schema/API design
- Use **code-reviewer** after writing code
- Use **tdd-guide** for every bug fix or new feature
- Project CLAUDE.md: `/Users/yahelraviv/compass/CLAUDE.md`
