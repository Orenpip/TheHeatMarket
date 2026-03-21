import { NextResponse } from "next/server";
import { requireStudent, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { rateLimiters } from "@/lib/redis";
import { z } from "zod";
import { PromptType } from "@compass/db";

const createReflectionSchema = z.object({
  sessionId: z.string(),
  promptText: z.string().min(1).max(2000),
  responseText: z.string().max(10000).optional(),
  promptType: z.nativeEnum(PromptType),
  isSharedWithCounselor: z.boolean().default(false),
});

export async function POST(req: Request) {
  try {
    const student = await requireStudent();

    const { success } = await rateLimiters.reflectionsCreate.limit(student.id);
    if (!success) {
      return NextResponse.json({ error: "Too many requests" }, { status: 429 });
    }

    const body = await req.json();
    const data = createReflectionSchema.parse(body);

    // Validate session belongs to student
    const session = await prisma.reflectionSession.findFirst({
      where: { id: data.sessionId, studentId: student.id },
    });
    if (!session) {
      return NextResponse.json({ error: "Session not found" }, { status: 404 });
    }

    const wordCount = data.responseText
      ? data.responseText.trim().split(/\s+/).filter(Boolean).length
      : 0;

    const reflection = await prisma.reflection.create({
      data: {
        studentId: student.id,
        sessionId: data.sessionId,
        promptText: data.promptText,
        responseText: data.responseText,
        promptType: data.promptType,
        isSharedWithCounselor: data.isSharedWithCounselor,
        wordCount,
      },
    });

    return NextResponse.json(reflection, { status: 201 });
  } catch (error) {
    return apiError(error);
  }
}
