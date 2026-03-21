import { NextResponse } from "next/server";
import { z } from "zod";
import { requireCounselor, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { redis, CACHE_KEYS } from "@/lib/redis";
import { Client } from "@upstash/qstash";

function getQStash() {
  return new Client({ token: process.env.QSTASH_TOKEN! });
}

const updateOpportunitySchema = z.object({
  title: z.string().min(1).max(200).optional(),
  description: z.string().min(50).max(2000).optional(),
  category: z.enum(["COMPETITION", "RESEARCH", "EVENT", "HACKATHON", "PROGRAM", "CLUB", "VOLUNTEER", "PUBLICATION"]).optional(),
  status: z.enum(["DRAFT", "PUBLISHED"]).optional(),
  url: z.string().url().optional().or(z.literal("")).optional(),
  location: z.string().max(200).optional(),
  organizerName: z.string().max(200).optional(),
  gradeLevels: z.array(z.number().int().min(9).max(12)).optional(),
  deadline: z.string().datetime().nullable().optional(),
  startDate: z.string().datetime().nullable().optional(),
  endDate: z.string().datetime().nullable().optional(),
  tags: z.array(z.string().max(50)).max(10).optional(),
});

export async function PATCH(
  req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const counselor = await requireCounselor();
    const { id } = await params;

    const opportunity = await prisma.opportunity.findFirst({
      where: { id, schoolId: counselor.schoolId, status: { not: "ARCHIVED" } },
    });

    if (!opportunity) {
      return NextResponse.json({ error: "Not found" }, { status: 404 });
    }

    const body = await req.json();
    const parsed = updateOpportunitySchema.safeParse(body);
    if (!parsed.success) {
      return NextResponse.json(
        { error: "Validation failed", details: parsed.error.flatten() },
        { status: 400 }
      );
    }

    const data = parsed.data;
    const descriptionChanged = data.description !== undefined && data.description !== opportunity.description;

    const updated = await prisma.opportunity.update({
      where: { id },
      data: {
        ...data,
        url: data.url === "" ? null : data.url,
        deadline: data.deadline === null ? null : data.deadline ? new Date(data.deadline) : undefined,
        startDate: data.startDate === null ? null : data.startDate ? new Date(data.startDate) : undefined,
        endDate: data.endDate === null ? null : data.endDate ? new Date(data.endDate) : undefined,
        // Mark embedding as stale if description changed
        ...(descriptionChanged && { embeddedAt: null }),
      },
    });

    // Re-embed if description or title changed
    if (descriptionChanged || (data.title !== undefined && data.title !== opportunity.title)) {
      const appUrl = process.env.NEXT_PUBLIC_APP_URL;
      if (appUrl) {
        try {
          await getQStash().publishJSON({
            url: `${appUrl}/api/webhooks/qstash`,
            body: {
              type: "EMBED_OPPORTUNITY",
              data: { opportunityId: id },
              triggeredAt: new Date().toISOString(),
            },
          });
        } catch {
          // Non-fatal
        }
      }
    }

    await redis.del(CACHE_KEYS.counselorOpportunities(counselor.schoolId));

    return NextResponse.json(updated);
  } catch (error) {
    return apiError(error);
  }
}

export async function DELETE(
  _req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const counselor = await requireCounselor();
    const { id } = await params;

    const opportunity = await prisma.opportunity.findFirst({
      where: { id, schoolId: counselor.schoolId },
    });

    if (!opportunity) {
      return NextResponse.json({ error: "Not found" }, { status: 404 });
    }

    // Soft-delete: set status to ARCHIVED
    await prisma.opportunity.update({
      where: { id },
      data: { status: "ARCHIVED" },
    });

    await redis.del(CACHE_KEYS.counselorOpportunities(counselor.schoolId));

    return NextResponse.json({ success: true });
  } catch (error) {
    return apiError(error);
  }
}
