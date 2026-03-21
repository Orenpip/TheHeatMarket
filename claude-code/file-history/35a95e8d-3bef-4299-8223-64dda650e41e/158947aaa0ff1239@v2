import { NextRequest, NextResponse } from "next/server";
import { requireStudent, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { redis, CACHE_KEYS, CACHE_TTL, rateLimiters } from "@/lib/redis";
import { aiService } from "@/lib/ai-service";

const EXPLORE_RANKING_WEIGHTS = {
  cosine: 0.70,
  recency: 0.15,
  deadline: 0.15,
} as const;

function recencyBoost(createdAt: Date): number {
  const daysSince = (Date.now() - createdAt.getTime()) / (1000 * 60 * 60 * 24);
  return Math.max(0, 1 - daysSince / 90);
}

function deadlineUrgency(deadline: Date | null): number {
  if (!deadline) return 0;
  const daysUntil = (deadline.getTime() - Date.now()) / (1000 * 60 * 60 * 24);
  if (daysUntil < 0) return -0.5;
  if (daysUntil <= 14) return 1.0;
  if (daysUntil <= 30) return 0.7;
  if (daysUntil <= 60) return 0.3;
  return 0;
}

export async function GET(req: NextRequest) {
  try {
    const student = await requireStudent();

    const { success } = await rateLimiters.exploreFeed.limit(student.id);
    if (!success) {
      return NextResponse.json({ error: "Too many requests" }, { status: 429 });
    }

    const { searchParams } = new URL(req.url);
    const category = searchParams.get("category");
    const page = Math.max(1, parseInt(searchParams.get("page") ?? "1", 10));
    const limit = Math.min(50, Math.max(1, parseInt(searchParams.get("limit") ?? "20", 10)));
    const offset = (page - 1) * limit;

    // Cache only for page 1 with no filters
    const useCache = page === 1 && !category;
    if (useCache) {
      const cached = await redis.get(CACHE_KEYS.exploreFeed(student.id));
      if (cached) {
        return NextResponse.json(cached);
      }
    }

    // Get student's latest signal profile
    const signalProfile = await prisma.signalProfile.findFirst({
      where: { studentId: student.id },
      orderBy: { createdAt: "desc" },
    });

    // Get student's interactions to mark saved/dismissed
    const interactions = await prisma.studentOpportunityInteraction.findMany({
      where: { studentId: student.id },
      select: { opportunityId: true, savedAt: true, dismissedAt: true },
    });
    const interactionMap = new Map(
      interactions.map((i) => [
        i.opportunityId,
        { isSaved: i.savedAt !== null, isDismissed: i.dismissedAt !== null },
      ])
    );

    // Build where clause
    const whereBase = {
      status: "PUBLISHED" as const,
      OR: [
        { scope: "GLOBAL" as const },
        { scope: "SCHOOL" as const, schoolId: student.schoolId ?? "" },
      ],
      ...(category && { category: category as never }),
    };

    let opportunities: Array<{
      id: string;
      scope: string;
      category: string;
      title: string;
      description: string;
      url: string | null;
      location: string | null;
      organizerName: string | null;
      deadline: Date | null;
      startDate: Date | null;
      tags: string[];
      createdAt: Date;
      matchScore: number;
      matchReason: string;
    }> = [];

    const hasStudentEmbedding = !!(signalProfile?.compressedSummary && signalProfile.compressedSummary.length > 0);

    if (hasStudentEmbedding) {
      try {
        const aiServiceUrl = process.env.AI_SERVICE_URL;
        const aiServiceKey = process.env.AI_SERVICE_SECRET_KEY;

        const embeddingResponse = await fetch(`${aiServiceUrl}/embed`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-Service-Key": aiServiceKey!,
          },
          body: JSON.stringify({ text: signalProfile!.compressedSummary }),
        });

        if (embeddingResponse.ok) {
          const embeddingData = (await embeddingResponse.json()) as { embedding: unknown };
          const rawEmbedding = embeddingData.embedding;

          if (
            Array.isArray(rawEmbedding) &&
            rawEmbedding.length === 1024 &&
            rawEmbedding.every((v): v is number => typeof v === "number" && isFinite(v))
          ) {
            const embeddingStr = `[${rawEmbedding.join(",")}]`;

            type RawRow = {
              id: string;
              scope: string;
              category: string;
              title: string;
              description: string;
              url: string | null;
              location: string | null;
              organizerName: string | null;
              deadline: Date | null;
              startDate: Date | null;
              tags: string[];
              createdAt: Date;
              cosine_similarity: number;
            };

            // Fetch top 100 by cosine similarity (category filter applied in JS)
            const rows = await prisma.$queryRaw<RawRow[]>`
              SELECT
                id, scope, category, title, description, url, location, "organizerName",
                deadline, "startDate", tags, "createdAt",
                1 - (embedding <-> ${embeddingStr}::vector) AS cosine_similarity
              FROM "Opportunity"
              WHERE embedding IS NOT NULL
                AND status = 'PUBLISHED'
                AND (scope = 'GLOBAL' OR "schoolId" = ${student.schoolId ?? ""})
              ORDER BY embedding <-> ${embeddingStr}::vector
              LIMIT 100
            `;

            // Apply category filter in JS
            const filteredRows = category ? rows.filter((r) => r.category === category) : rows;

            // Hybrid score re-ranking
            const ranked = filteredRows
              .map((row) => ({
                ...row,
                matchScore:
                  EXPLORE_RANKING_WEIGHTS.cosine * row.cosine_similarity +
                  EXPLORE_RANKING_WEIGHTS.recency * recencyBoost(new Date(row.createdAt)) +
                  EXPLORE_RANKING_WEIGHTS.deadline * deadlineUrgency(row.deadline ? new Date(row.deadline) : null),
                matchReason: "",
              }))
              .sort((a, b) => b.matchScore - a.matchScore);

            opportunities = ranked;
          }
        }
      } catch {
        // Fall through to non-personalized
      }
    }

    // Fallback: non-personalized
    if (opportunities.length === 0) {
      const fallback = await prisma.opportunity.findMany({
        where: whereBase,
        orderBy: [{ deadline: "asc" }, { createdAt: "desc" }],
        take: 100,
        select: {
          id: true, scope: true, category: true, title: true, description: true,
          url: true, location: true, organizerName: true, deadline: true,
          startDate: true, tags: true, createdAt: true,
        },
      });
      opportunities = fallback.map((opp) => ({
        ...opp,
        matchScore: 0,
        matchReason: "",
      }));
    }

    const total = opportunities.length;
    const page_items = opportunities.slice(offset, offset + limit);

    // Fetch match explanations for page items if personalized
    if (hasStudentEmbedding && signalProfile?.compressedSummary && page_items.length > 0) {
      try {
        const { explanations } = await aiService.explainMatch({
          studentSummary: signalProfile.compressedSummary,
          opportunities: page_items.map((opp) => ({
            id: opp.id,
            title: opp.title,
            description: opp.description.slice(0, 300),
            category: opp.category,
          })),
        });

        const explanationMap = new Map(explanations.map((e) => [e.id, e.reason]));
        for (const opp of page_items) {
          opp.matchReason = explanationMap.get(opp.id) ?? "";
        }
      } catch {
        // Non-fatal: explanations are an enhancement
      }
    }

    const result = {
      opportunities: page_items.map((opp) => ({
        ...opp,
        deadline: opp.deadline?.toISOString() ?? null,
        startDate: opp.startDate?.toISOString() ?? null,
        createdAt: opp.createdAt.toISOString(),
        matchScore: Math.max(0, Math.min(1, opp.matchScore)),
        isSaved: interactionMap.get(opp.id)?.isSaved ?? false,
        isDismissed: interactionMap.get(opp.id)?.isDismissed ?? false,
        isPersonalized: hasStudentEmbedding,
      })),
      pagination: { page, limit, total, hasMore: offset + limit < total },
    };

    if (useCache) {
      await redis.set(CACHE_KEYS.exploreFeed(student.id), result, {
        ex: CACHE_TTL.exploreFeed,
      });
    }

    return NextResponse.json(result);
  } catch (error) {
    return apiError(error);
  }
}
