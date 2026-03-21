# Fix Prisma Runtime Error on Vercel — PERMANENT Solution

## Context

The COMPASS Next.js app builds successfully on Vercel (Prisma generates, webpack compiles, 33 pages generated), but crashes at runtime with:
```
PrismaClientInitializationError: Prisma Client could not locate the Query Engine for runtime "rhel-openssl-3.0.x"
```

We've tried 10+ approaches: binaryTargets, serverExternalPackages, outputFileTracingRoot, driver adapters, non-cacheable turbo, binary copying. None worked because they all still rely on the **native binary** (`libquery_engine-rhel-openssl-3.0.x.so.node`), which Vercel's Node File Tracing (nft) simply does not bundle.

## Root Cause

The generated Prisma client has TWO entry points:

| Entry point | Runtime | Engine | Native binary needed? |
|---|---|---|---|
| `index.js` (default) | `runtime/library.js` | Native `.node` binary | **YES** |
| `wasm.js` | `runtime/wasm-engine-edge.js` | `query_engine_bg.wasm` | **NO** |

Our code at `packages/db/src/index.ts` imports from `../generated/client` which resolves to `index.js` → **library engine** → needs native binary → Vercel can't find it → crash.

The driver adapter (`@prisma/adapter-pg`) we added only replaces the **database connection layer** — Prisma still needs a **query engine** (either native binary OR WASM) to parse queries and generate SQL.

## The Fix (2 files, minimal changes)

### 1. `packages/db/src/index.ts` — Switch to WASM client

Change both import lines from `../generated/client` to `../generated/client/wasm`:

```typescript
import { Pool } from "pg";
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "../generated/client/wasm";  // <-- CHANGED

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

function createPrismaClient() {
  const url =
    process.env.DATABASE_URL?.replace(/[?&]pgbouncer=true/, "") ?? "";
  const pool = new Pool({ connectionString: url, max: 3 });
  const adapter = new PrismaPg(pool);
  return new PrismaClient({ adapter });
}

export const prisma = globalForPrisma.prisma ?? createPrismaClient();

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;

export * from "../generated/client/wasm";  // <-- CHANGED
```

**Why this works**: `wasm.js` loads `runtime/wasm-engine-edge.js` which uses `query_engine_bg.wasm` (a pure JavaScript/WASM module). No native binary needed. No platform-specific files. Works on any runtime — macOS, Linux, Vercel, anywhere.

**Types are identical**: `wasm.d.ts` → `default.d.ts` → `index.d.ts`. Same `PrismaClient`, same enums, same types. All downstream `import { prisma } from "@compass/db"` continues working unchanged.

### 2. `apps/web/next.config.mjs` — Enable WASM support in webpack

The WASM client dynamically imports `query_engine_bg.wasm`. Since `@compass/db` is in `transpilePackages`, webpack processes it and needs `asyncWebAssembly` enabled:

```javascript
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  transpilePackages: ["@compass/ui", "@compass/types", "@compass/db"],
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "*.clerk.com",
      },
    ],
  },
  experimental: {
    optimizePackageImports: ["@compass/ui"],
    outputFileTracingRoot: path.join(__dirname, "../../"),
  },
  webpack: (config, { isServer }) => {
    if (isServer) {
      config.experiments = {
        ...config.experiments,
        asyncWebAssembly: true,
      };
      // Fix webpack WASM output for serverless
      config.output.webassemblyModuleFilename = "./../server/chunks/[id].wasm";
    }
    return config;
  },
};

export default nextConfig;
```

### No other file changes needed

- **`schema.prisma`**: No changes. `driverAdapters` is GA in Prisma 6 (no preview feature needed). The generator output stays as-is.
- **`turbo.json`**: No changes needed.
- **`vercel.json`**: Keep `--force` in buildCommand for this deploy. Can remove it after confirming success.
- **All consumer files** (`auth.ts`, API routes, pages): Import from `@compass/db` — unchanged.

## Why This Is Permanent

1. **No native binary dependency** — WASM runs identically on macOS (dev), Linux (Vercel), any platform
2. **No nft tracing issues** — WASM is bundled by webpack, not traced by nft
3. **No monorepo path issues** — webpack resolves the WASM module as part of the bundle
4. **Driver adapter + WASM is Prisma's recommended serverless stack** — not a workaround
5. **Survives `prisma generate` re-runs** — the `/wasm` export is a stable Prisma API

## Verification

After pushing:
1. Vercel builds as before (turbo → prisma generate → next build → 33 pages)
2. No "Query Engine" errors at runtime
3. Visiting the URL shows the Clerk sign-in page
4. Signing up / logging in triggers Prisma DB queries that succeed
