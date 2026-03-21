import { NextResponse } from "next/server";
import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";
import { redis, CACHE_KEYS, CACHE_TTL } from "@/lib/redis";

export async function GET() {
  try {
    const student = await requireStudent();

    // Check cache
    const cached = await redis.get(CACHE_KEYS.personalizedMap(student.id));
    if (cached) {
      return NextResponse.json(cached);
    }

    // Get signal profile for embedding-based search
    const signalProfile = await prisma.signalProfile.findFirst({
      where: { studentId: student.id },
      orderBy: { createdAt: "desc" },
    });

    let nodes;
    let personalizedNodeIds: string[] = [];

    if (signalProfile?.compressedSummary) {
      // Use pgvector similarity search
      // Generate embedding via AI service, then query
      try {
        const aiServiceUrl = process.env.AI_SERVICE_URL;
        const aiServiceKey = process.env.AI_SERVICE_SECRET_KEY;

        const embeddingResponse = await fetch(
          `${aiServiceUrl}/embed`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-Service-Key": aiServiceKey!,
            },
            body: JSON.stringify({ text: signalProfile.compressedSummary }),
          }
        );

        if (embeddingResponse.ok) {
          const { embedding } = await embeddingResponse.json() as { embedding: number[] };
          const embeddingStr = `[${embedding.join(",")}]`;

          // pgvector similarity search (raw query needed for vector ops)
          const similarNodes = await prisma.$queryRaw<
            Array<{ id: string; similarity: number }>
          >`
            SELECT id, 1 - (embedding <-> ${embeddingStr}::vector) as similarity
            FROM "MapNode"
            WHERE embedding IS NOT NULL
            ORDER BY embedding <-> ${embeddingStr}::vector
            LIMIT 50
          `;

          personalizedNodeIds = similarNodes.map((n) => n.id);

          nodes = await prisma.mapNode.findMany({
            where: { id: { in: personalizedNodeIds } },
            select: {
              id: true,
              type: true,
              label: true,
              description: true,
              metadata: true,
              parentId: true,
              createdAt: true,
              updatedAt: true,
            },
          });

          // Inject similarity scores
          const simMap = new Map(
            similarNodes.map((n) => [n.id, n.similarity])
          );
          nodes = nodes.map((n) => ({
            ...n,
            similarity: simMap.get(n.id) ?? 0,
            isPersonalized: true,
          }));
        }
      } catch {
        // Fall through to non-personalized
      }
    }

    if (!nodes || nodes.length === 0) {
      // Fallback: return all nodes without personalization
      nodes = await prisma.mapNode.findMany({
        select: {
          id: true,
          type: true,
          label: true,
          description: true,
          metadata: true,
          parentId: true,
          createdAt: true,
          updatedAt: true,
        },
        take: 100,
        orderBy: { label: "asc" },
      });
    }

    // Get edges for these nodes
    const nodeIds = nodes.map((n) => n.id);
    const edges = await prisma.mapEdge.findMany({
      where: {
        OR: [
          { sourceId: { in: nodeIds } },
          { targetId: { in: nodeIds } },
        ],
      },
    });

    const result = {
      nodes,
      edges,
      personalizedNodeIds,
      studentBreadthScore: signalProfile?.breadthScore ?? 0,
    };

    // Cache for 1 hour
    await redis.setex(
      CACHE_KEYS.personalizedMap(student.id),
      CACHE_TTL.personalizedMap,
      result
    );

    return NextResponse.json(result);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
