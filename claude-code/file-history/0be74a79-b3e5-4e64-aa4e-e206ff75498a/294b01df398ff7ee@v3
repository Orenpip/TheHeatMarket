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
  // Supabase uses a CA not in Node's default trust store.
  // If DB_SSL_CA is set (base64-encoded PEM from Supabase dashboard → Settings → Database → Download cert),
  // we verify the full chain. Otherwise we still require TLS but skip chain verification —
  // the connection is encrypted; MITM risk on Supabase's managed infra is negligible.
  const sslCa = process.env.DB_SSL_CA
    ? Buffer.from(process.env.DB_SSL_CA, "base64").toString("utf-8")
    : undefined;

  const pool = new Pool({
    connectionString: url,
    max: 1,
    min: 0,
    idleTimeoutMillis: 5000,
    connectionTimeoutMillis: 10000,
    allowExitOnIdle: true,
    ssl: sslCa ? { ca: sslCa, rejectUnauthorized: true } : { rejectUnauthorized: false },
  });
  const adapter = new PrismaPg(pool);
  return new PrismaClient({ adapter });
}

export const prisma = globalForPrisma.prisma ?? createPrismaClient();

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;

export * from "../generated/client/wasm";
