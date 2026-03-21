import { NextResponse } from "next/server";
import { z } from "zod";
import { requireCounselor, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { redis, CACHE_KEYS, CACHE_TTL, rateLimiters } from "@/lib/redis";
import { Client } from "@upstash/qstash";

function getQStash() {
  return new Client({ token: process.env.QSTASH_TOKEN! });
}

const createOpportunitySchema = z.object({
  title: z.string().min(1).max(200),
  description: z.string().min(50, "Describe the opportunity in detail (min 50 chars) for better student matching").max(2000),
  category: z.enum(["COMPETITION", "RESEARCH", "EVENT", "HACKATHON", "PROGRAM", "CLUB", "VOLUNTEER", "PUBLICATION"]),
  status: z.enum(["DRAFT", "PUBLISHED"]).default("PUBLISHED"),
  url: z.string().url().optional().or(z.literal("")),
  location: z.string().max(200).optional(),
  organizerName: z.string().max(200).optional(),
  gradeLevels: z.array(z.number().int().min(9).max(12)).default([9, 10, 11, 12]),
  deadline: z.string().datetime().optional(),
  startDate: z.string().datetime().optional(),
  endDate: z.string().datetime().optional(),
  tags: z.array(z.string().max(50)).max(10).default([]),
});

export async function GET() {
  try {
    const counselor = await requireCounselor();

    const cached = await redis.get(CACHE_KEYS.counselorOpportunities(counselor.schoolId));
    if (cached) {
      return NextResponse.json(cached);
    }

    const opportunities = await prisma.opportunity.findMany({
      where: {
        schoolId: counselor.schoolId,
        status: { not: "ARCHIVED" },
      },
      orderBy: { createdAt: "desc" },
      select: {
        id: true,
        scope: true,
        status: true,
        category: true,
        title: true,
        description: true,
        url: true,
        location: true,
        organizerName: true,
        gradeLevels: true,
        deadline: true,
        startDate: true,
        endDate: true,
        tags: true,
        counselorId: true,
        embeddedAt: true,
        createdAt: true,
        updatedAt: true,
        _count: { select: { interactions: true } },
      },
    });

    const result = opportunities.map((opp) => ({
      ...opp,
      interactionCount: opp._count.interactions,
      isEmbedded: opp.embeddedAt !== null,
    }));

    await redis.set(
      CACHE_KEYS.counselorOpportunities(counselor.schoolId),
      result,
      { ex: CACHE_TTL.counselorOpportunities }
    );

    return NextResponse.json(result);
  } catch (error) {
    return apiError(error);
  }
}

export async function POST(req: Request) {
  try {
    const counselor = await requireCounselor();

    const { success } = await rateLimiters.counselorOpportunityCreate.limit(counselor.id);
    if (!success) {
      return NextResponse.json({ error: "Too many requests" }, { status: 429 });
    }

    const body = await req.json();
    const parsed = createOpportunitySchema.safeParse(body);
    if (!parsed.success) {
      return NextResponse.json(
        { error: "Validation failed", details: parsed.error.flatten() },
        { status: 400 }
      );
    }

    const data = parsed.data;

    const opportunity = await prisma.opportunity.create({
      data: {
        scope: "SCHOOL",
        status: data.status,
        category: data.category,
        title: data.title,
        description: data.description,
        url: data.url || null,
        location: data.location || null,
        organizerName: data.organizerName || null,
        gradeLevels: data.gradeLevels,
        deadline: data.deadline ? new Date(data.deadline) : null,
        startDate: data.startDate ? new Date(data.startDate) : null,
        endDate: data.endDate ? new Date(data.endDate) : null,
        tags: data.tags,
        schoolId: counselor.schoolId,
        counselorId: counselor.id,
      },
    });

    // Queue background embedding
    const appUrl = process.env.NEXT_PUBLIC_APP_URL;
    if (appUrl) {
      try {
        await getQStash().publishJSON({
          url: `${appUrl}/api/webhooks/qstash`,
          body: {
            type: "EMBED_OPPORTUNITY",
            data: { opportunityId: opportunity.id },
            triggeredAt: new Date().toISOString(),
          },
        });
      } catch {
        // Non-fatal: batch job will retry embedding
      }
    }

    // Invalidate counselor list cache
    await redis.del(CACHE_KEYS.counselorOpportunities(counselor.schoolId));

    return NextResponse.json(
      { ...opportunity, embeddingStatus: "QUEUED" },
      { status: 201 }
    );
  } catch (error) {
    return apiError(error);
  }
}
