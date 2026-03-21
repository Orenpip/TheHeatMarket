# Vercel Deployment - COMPASS

## Setup (working as of March 2026)
- **Root Directory**: blank (empty) in Vercel UI
- **All Override toggles**: OFF
- **Node.js**: 20.x
- **Config**: Single `vercel.json` at monorepo root (not in apps/web)

## Root vercel.json contains
- `"framework": "nextjs"`
- `"buildCommand": "turbo run build --filter=@compass/web"`
- `"outputDirectory": "apps/web/.next"`
- `"installCommand": "pnpm install"`
- `"ignoreCommand": "npx turbo-ignore @compass/web"`

## Prisma on Vercel (solved)
- **Problem**: Native binary engine (`libquery_engine-rhel-openssl-3.0.x.so.node`) not traced by nft; WASM engine can't be parsed by Next.js 14's webpack (`parseVec could not cast the value`)
- **Solution**: Custom webpack loader (`apps/web/prisma-wasm-loader.js`) that inlines the 2.2MB WASM as base64, compiles it via `new WebAssembly.Module(buffer)`, bypassing the broken parser entirely
- `packages/db/src/index.ts` imports from `../generated/client/wasm` (not the default `index.js`)
- Uses `@prisma/adapter-pg` driver adapter with `pg` Pool
- **DIRECT_URL** (not DATABASE_URL) must be used for the pg Pool — DATABASE_URL points to pgbouncer which has different auth
- `next.config.mjs` webpack rule: `{ test: /query_engine_bg\.wasm$/, loader: "prisma-wasm-loader.js", type: "javascript/auto" }`
- Do NOT enable `asyncWebAssembly` experiment — that's what triggers the broken parser

## Auth / student record resilience
- `(student)/layout.tsx` auto-creates student record from Clerk user data if the webhook missed it (e.g. DB was unreachable when webhook fired)
- Without this, missing student record causes redirect loop: `/` → `/sign-in` → `/` …

## Key lessons
- With Root Directory blank, Vercel reads `/vercel.json` (root), NOT `apps/web/vercel.json`
- `next` must be in root `package.json` devDependencies for Vercel to detect the Next.js version
- After adding deps to root package.json, must run `pnpm install` to update lockfile
- The `functions` config (maxDuration) was deferred — add back after confirming deploy works
