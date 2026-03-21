/**
 * embed-map-nodes.ts
 *
 * Batch-embeds all MapNode records that don't yet have a vector embedding.
 * Uses Voyage AI `voyage-3` (1024-dim) via the AI service /embed endpoint.
 *
 * Run after seeding: `pnpm tsx scripts/embed-map-nodes.ts`
 *
 * The script:
 * 1. Fetches all MapNodes without embeddings
 * 2. Calls the AI service /embed endpoint in batches of 50
 * 3. Writes the 1024-dim vectors back via raw Prisma SQL
 */

import { prisma } from "@compass/db";

const AI_SERVICE_URL =
  process.env.AI_SERVICE_URL ?? "http://localhost:8000";
const AI_SERVICE_SECRET_KEY = process.env.AI_SERVICE_SECRET_KEY ?? "";
const BATCH_SIZE = 50;

interface MapNode {
  id: string;
  label: string;
  description: string | null;
  type: string;
}

interface EmbedResponse {
  embedding: number[];
}

async function embedText(text: string): Promise<number[]> {
  const res = await fetch(`${AI_SERVICE_URL}/embed`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Service-Key": AI_SERVICE_SECRET_KEY,
    },
    body: JSON.stringify({ text }),
  });

  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Embed API error ${res.status}: ${body}`);
  }

  const data = (await res.json()) as EmbedResponse;
  return data.embedding;
}

async function run() {
  console.log("Fetching map nodes without embeddings...");

  // Raw query because Prisma doesn't expose the vector column
  const nodes = (await prisma.$queryRaw`
    SELECT id, label, description, type
    FROM "MapNode"
    WHERE embedding IS NULL
    ORDER BY "createdAt" ASC
  `) as MapNode[];

  console.log(`Found ${nodes.length} nodes to embed.`);

  if (nodes.length === 0) {
    console.log("Nothing to do.");
    return;
  }

  let processed = 0;
  let errors = 0;

  for (let i = 0; i < nodes.length; i += BATCH_SIZE) {
    const batch = nodes.slice(i, i + BATCH_SIZE);

    await Promise.allSettled(
      batch.map(async (node) => {
        // Build a rich text representation for embedding
        const text = [
          `${node.type}: ${node.label}`,
          node.description ?? "",
        ]
          .filter(Boolean)
          .join(". ");

        try {
          const embedding = await embedText(text);

          // Write back using raw SQL — pgvector expects a string like '[0.1,0.2,...]'
          const vectorStr = `[${embedding.join(",")}]`;
          await prisma.$executeRaw`
            UPDATE "MapNode"
            SET embedding = ${vectorStr}::vector
            WHERE id = ${node.id}
          `;

          processed++;
          if (processed % 10 === 0 || processed === nodes.length) {
            console.log(
              `  Progress: ${processed}/${nodes.length} (${errors} errors)`
            );
          }
        } catch (err) {
          errors++;
          console.error(`  ✗ Failed to embed node ${node.id} (${node.label}):`, err);
        }
      })
    );

    // Small delay between batches to respect rate limits
    if (i + BATCH_SIZE < nodes.length) {
      await new Promise((r) => setTimeout(r, 500));
    }
  }

  console.log(`\nDone. ${processed} embedded, ${errors} failed.`);
}

run()
  .catch((err) => {
    console.error("Fatal error:", err);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
