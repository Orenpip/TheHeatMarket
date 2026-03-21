import { NextResponse } from "next/server";
import { requireStudent, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { redis, CACHE_KEYS } from "@/lib/redis";

export const maxDuration = 30;

export async function DELETE() {
  try {
    const student = await requireStudent();

    // Delete all student data (cascades via DB)
    await prisma.student.delete({
      where: { id: student.id },
    });

    // Clear all caches
    await Promise.all([
      redis.del(CACHE_KEYS.signalProfile(student.id)),
      redis.del(CACHE_KEYS.personalizedMap(student.id)),
    ]);

    return NextResponse.json({ success: true, message: "Account deleted" });
  } catch (error) {
    return apiError(error);
  }
}
