import { NextResponse } from "next/server";
import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";

export async function GET() {
  try {
    const student = await requireStudent();

    const [sessions, activities, reflections, signalProfile, privacySettings] =
      await Promise.all([
        prisma.reflectionSession.findMany({
          where: { studentId: student.id },
          orderBy: { createdAt: "asc" },
        }),
        prisma.activity.findMany({
          where: { studentId: student.id },
          orderBy: { createdAt: "asc" },
        }),
        prisma.reflection.findMany({
          where: { studentId: student.id },
          orderBy: { createdAt: "asc" },
        }),
        prisma.signalProfile.findFirst({
          where: { studentId: student.id },
          orderBy: { createdAt: "desc" },
        }),
        prisma.studentPrivacySettings.findUnique({
          where: { studentId: student.id },
        }),
      ]);

    const exportData = {
      exportedAt: new Date().toISOString(),
      student: {
        id: student.id,
        email: student.email,
        firstName: student.firstName,
        lastName: student.lastName,
        gradeLevel: student.gradeLevel,
        createdAt: student.createdAt,
      },
      sessions,
      activities,
      reflections,
      signalProfile,
      privacySettings,
    };

    return new NextResponse(JSON.stringify(exportData, null, 2), {
      headers: {
        "Content-Type": "application/json",
        "Content-Disposition": `attachment; filename="compass-export-${student.id}.json"`,
      },
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
