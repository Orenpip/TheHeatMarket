import { NextResponse } from "next/server";
import { requireStudent, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { redis, CACHE_KEYS, CACHE_TTL } from "@/lib/redis";

export async function GET() {
  try {
    const student = await requireStudent();

    // Check cache first
    const cached = await redis.get(CACHE_KEYS.signalProfile(student.id));
    if (cached) {
      return NextResponse.json(cached);
    }

    const profile = await prisma.signalProfile.findFirst({
      where: { studentId: student.id },
      orderBy: { createdAt: "desc" },
    });

    if (!profile) {
      return NextResponse.json(null);
    }

    // Cache it
    await redis.setex(
      CACHE_KEYS.signalProfile(student.id),
      CACHE_TTL.signalProfile,
      profile
    );

    return NextResponse.json(profile);
  } catch (error) {
    return apiError(error);
  }
}
