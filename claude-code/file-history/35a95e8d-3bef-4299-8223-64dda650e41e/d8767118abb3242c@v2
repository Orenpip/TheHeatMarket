import { NextResponse } from "next/server";
import { z } from "zod";
import { requireStudent, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { redis, CACHE_KEYS, rateLimiters } from "@/lib/redis";

const interactSchema = z.object({
  type: z.enum(["VIEW", "SAVE", "UNSAVE", "CLICK", "DISMISS", "APPLY"]),
});

export async function POST(
  req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const student = await requireStudent();
    const { id: opportunityId } = await params;

    const { success } = await rateLimiters.exploreInteract.limit(student.id);
    if (!success) {
      return NextResponse.json({ error: "Too many requests" }, { status: 429 });
    }

    const body = await req.json();
    const parsed = interactSchema.safeParse(body);
    if (!parsed.success) {
      return NextResponse.json({ error: "Invalid interaction type" }, { status: 400 });
    }

    const { type } = parsed.data;
    const now = new Date();

    // Map interaction type to update fields
    type UpdateFields = {
      viewedAt?: Date | null;
      savedAt?: Date | null;
      clickedAt?: Date | null;
      dismissedAt?: Date | null;
      appliedAt?: Date | null;
    };
    const fieldMap: Record<string, UpdateFields> = {
      VIEW:    { viewedAt: now },
      SAVE:    { savedAt: now },
      UNSAVE:  { savedAt: null },
      CLICK:   { clickedAt: now },
      DISMISS: { dismissedAt: now },
      APPLY:   { appliedAt: now },
    };

    const fields = fieldMap[type] ?? {};

    await prisma.studentOpportunityInteraction.upsert({
      where: { studentId_opportunityId: { studentId: student.id, opportunityId } },
      create: { studentId: student.id, opportunityId, ...fields },
      update: fields,
    });

    // Invalidate explore feed cache so interaction is reflected
    await redis.del(CACHE_KEYS.exploreFeed(student.id));

    return NextResponse.json({ success: true });
  } catch (error) {
    return apiError(error);
  }
}
