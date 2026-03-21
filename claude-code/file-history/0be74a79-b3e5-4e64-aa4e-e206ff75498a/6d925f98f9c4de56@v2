import { NextResponse } from "next/server";
import { requireStudent, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { z } from "zod";

const bodySchema = z.object({
  sessionId: z.string(),
});

export async function POST(req: Request) {
  try {
    const student = await requireStudent();
    const body = await req.json();
    const { sessionId } = bodySchema.parse(body);

    const session = await prisma.reflectionSession.findFirst({
      where: { id: sessionId, studentId: student.id },
      include: { template: true },
    });

    if (!session) {
      return NextResponse.json({ error: "Session not found" }, { status: 404 });
    }

    if (session.template?.prompts) {
      return NextResponse.json({ prompts: session.template.prompts });
    }

    // Fallback for legacy sessions without a template
    return NextResponse.json({
      prompts: [
        {
          text: "What activity from the past few weeks felt most engaging or alive to you?",
          type: "PATTERN",
        },
        {
          text: "What's something you've been curious about lately but haven't had time to explore?",
          type: "EXPLORATION",
        },
      ],
    });
  } catch (error) {
    return apiError(error);
  }
}
