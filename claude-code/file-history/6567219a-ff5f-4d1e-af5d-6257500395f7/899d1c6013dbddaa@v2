import { NextResponse } from "next/server";
import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";
import { redis, CACHE_KEYS } from "@/lib/redis";

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
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
