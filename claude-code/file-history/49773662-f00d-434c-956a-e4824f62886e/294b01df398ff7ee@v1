import { Pool } from "pg";
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "../generated/client/wasm";

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

function createPrismaClient() {
  // Use DIRECT_URL (bypasses pgbouncer) for the pg Pool, since the driver
  // adapter manages its own connections.  Fall back to DATABASE_URL if unset.
  const url = process.env.DIRECT_URL ?? process.env.DATABASE_URL ?? "";
  const pool = new Pool({ connectionString: url, max: 3 });
  const adapter = new PrismaPg(pool);
  return new PrismaClient({ adapter });
}

export const prisma = globalForPrisma.prisma ?? createPrismaClient();

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;

export * from "../generated/client/wasm";
