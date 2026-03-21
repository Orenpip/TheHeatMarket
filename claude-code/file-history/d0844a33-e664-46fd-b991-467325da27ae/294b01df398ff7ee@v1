import { Pool } from "pg";
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "../generated/client/wasm";

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

function createPrismaClient() {
  // Use DATABASE_URL (pgbouncer pooled) for runtime queries in serverless.
  // DIRECT_URL is only for migrations (prisma db push/migrate).
  const url = process.env.DATABASE_URL ?? process.env.DIRECT_URL ?? "";
  const pool = new Pool({
    connectionString: url,
    max: 1,
    min: 0,
    idleTimeoutMillis: 5000,         // release connections quickly — prevents stale connections on warm Lambda reuse
    connectionTimeoutMillis: 10000,  // fail fast if can't connect
    allowExitOnIdle: true,           // let Lambda exit cleanly
    ssl: { rejectUnauthorized: false },
  });
  const adapter = new PrismaPg(pool);
  return new PrismaClient({ adapter });
}

export const prisma = globalForPrisma.prisma ?? createPrismaClient();

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;

export * from "../generated/client/wasm";
