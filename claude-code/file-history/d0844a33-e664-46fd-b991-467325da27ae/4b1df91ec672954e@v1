import { NextResponse } from "next/server";
import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";
import { z } from "zod";
import { PromptType } from "@compass/db";

const createReflectionSchema = z.object({
  sessionId: z.string(),
  promptText: z.string().min(1),
  responseText: z.string().optional(),
  promptType: z.nativeEnum(PromptType),
  isSharedWithCounselor: z.boolean().default(false),
});

export async function POST(req: Request) {
  try {
    const student = await requireStudent();
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
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
