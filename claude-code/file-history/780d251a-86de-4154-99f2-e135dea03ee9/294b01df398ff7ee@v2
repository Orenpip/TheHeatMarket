import { Pool } from "pg";
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "../generated/client/wasm";

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

function createPrismaClient() {
  // Strip Prisma-specific pgbouncer param — pg doesn't understand it
  const url =
    process.env.DATABASE_URL?.replace(/[?&]pgbouncer=true/, "") ?? "";
  const pool = new Pool({ connectionString: url, max: 3 });
  const adapter = new PrismaPg(pool);
  return new PrismaClient({ adapter });
}

export const prisma = globalForPrisma.prisma ?? createPrismaClient();

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;

export * from "../generated/client/wasm";
