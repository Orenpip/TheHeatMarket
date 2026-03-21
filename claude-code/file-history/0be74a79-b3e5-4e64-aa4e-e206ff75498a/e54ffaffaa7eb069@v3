import { NextResponse } from "next/server";
import { requireStudent, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { rateLimiters } from "@/lib/redis";
import { COOLDOWN_DAYS } from "@/lib/constants";

export async function POST() {
  try {
    const student = await requireStudent();

    const { success } = await rateLimiters.sessionCreate.limit(student.id);
    if (!success) {
      return NextResponse.json({ error: "Too many requests" }, { status: 429 });
    }

    const now = new Date();

    // Check for existing in-progress session
    const inProgress = await prisma.reflectionSession.findFirst({
      where: { studentId: student.id, completedAt: null },
      orderBy: { createdAt: "desc" },
    });
    if (inProgress) {
      return NextResponse.json(inProgress);
    }

    // Enforce 3-week cooldown from last completed session
    const lastCompleted = await prisma.reflectionSession.findFirst({
      where: { studentId: student.id, completedAt: { not: null } },
      orderBy: { completedAt: "desc" },
    });

    if (lastCompleted?.completedAt) {
      const unlockDate = new Date(lastCompleted.completedAt);
      unlockDate.setDate(unlockDate.getDate() + COOLDOWN_DAYS);
      if (unlockDate > now) {
        const daysLeft = Math.ceil((unlockDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
        return NextResponse.json(
          { error: "cooldown", daysLeft },
          { status: 403 }
        );
      }
    }

    // Find next available template for current year
    const currentYear = String(now.getFullYear());
    const startedTemplateIds = (
      await prisma.reflectionSession.findMany({
        where: { studentId: student.id, templateId: { not: null } },
        select: { templateId: true },
      })
    ).map((s) => s.templateId!);

    const nextTemplate = await prisma.reflectionTemplate.findFirst({
      where: {
        yearKey: currentYear,
        isActive: true,
        id: { notIn: startedTemplateIds },
      },
      orderBy: { orderNum: "asc" },
    });

    if (!nextTemplate) {
      return NextResponse.json(
        { error: "all_complete" },
        { status: 403 }
      );
    }

    // Count sessions to assign session number
    const sessionCount = await prisma.reflectionSession.count({
      where: { studentId: student.id },
    });

    const session = await prisma.reflectionSession.create({
      data: {
        studentId: student.id,
        templateId: nextTemplate.id,
        sessionNumber: sessionCount + 1,
      },
      include: {
        activities: true,
        reflections: true,
        template: true,
      },
    });

    return NextResponse.json(session);
  } catch (error) {
    return apiError(error);
  }
}

export async function GET() {
  try {
    const student = await requireStudent();

    const sessions = await prisma.reflectionSession.findMany({
      where: { studentId: student.id },
      orderBy: { createdAt: "desc" },
      include: {
        template: { select: { title: true, orderNum: true } },
        activities: { select: { id: true, name: true } },
        reflections: {
          select: {
            id: true,
            promptType: true,
            wordCount: true,
            createdAt: true,
            isSharedWithCounselor: true,
          },
        },
      },
    });

    return NextResponse.json(sessions);
  } catch (error) {
    return apiError(error);
  }
}
