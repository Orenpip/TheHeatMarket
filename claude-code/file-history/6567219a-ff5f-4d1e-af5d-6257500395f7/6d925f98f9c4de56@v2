import { NextResponse } from "next/server";
import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";
import { aiService } from "@/lib/ai-service";
import { z } from "zod";

const bodySchema = z.object({
  sessionId: z.string(),
});

export async function POST(req: Request) {
  try {
    const student = await requireStudent();
    const body = await req.json();
    const { sessionId } = bodySchema.parse(body);

    // Verify session belongs to student
    const session = await prisma.reflectionSession.findFirst({
      where: { id: sessionId, studentId: student.id },
    });

    if (!session) {
      return NextResponse.json({ error: "Session not found" }, { status: 404 });
    }

    // Get data needed for prompt generation
    const [signalProfile, recentActivities, recentReflections] =
      await Promise.all([
        prisma.signalProfile.findFirst({
          where: { studentId: student.id },
          orderBy: { createdAt: "desc" },
          select: { compressedSummary: true },
        }),
        prisma.activity.findMany({
          where: { studentId: student.id },
          orderBy: { createdAt: "desc" },
          take: 15,
        }),
        prisma.reflection.findMany({
          where: { studentId: student.id },
          orderBy: { createdAt: "desc" },
          take: 10,
          select: {
            promptText: true,
            responseText: true,
            promptType: true,
          },
        }),
      ]);

    const previousPrompts = recentReflections.map((r) => r.promptText);

    const result = await aiService.getReflectionPrompts({
      studentId: student.id,
      compressedSummary: signalProfile?.compressedSummary ?? undefined,
      recentActivities,
      recentReflections,
      previousPrompts,
    });

    return NextResponse.json(result);
  } catch (error) {
    console.error("Prompt generation error:", error);
    // Return fallback prompts on error
    return NextResponse.json({
      prompts: [
        {
          promptText:
            "What activity from the past month felt most engaging or alive to you?",
          promptType: "PATTERN",
        },
        {
          promptText:
            "What's something you've been curious about lately but haven't had time to explore?",
          promptType: "EXPLORATION",
        },
      ],
    });
  }
}
