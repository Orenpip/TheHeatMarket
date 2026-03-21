import { NextResponse } from "next/server";
import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";
import { z } from "zod";

const createSessionSchema = z.object({
  monthKey: z.string().optional(),
});

export async function POST(req: Request) {
  try {
    const student = await requireStudent();
    const body = await req.json();
    const { monthKey } = createSessionSchema.parse(body);

    const now = new Date();
    const key =
      monthKey ??
      `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`;

    const session = await prisma.reflectionSession.upsert({
      where: {
        studentId_monthKey: {
          studentId: student.id,
          monthKey: key,
        },
      },
      update: {},
      create: {
        studentId: student.id,
        monthKey: key,
      },
      include: {
        activities: true,
        reflections: true,
      },
    });

    return NextResponse.json(session);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}

export async function GET() {
  try {
    const student = await requireStudent();

    const sessions = await prisma.reflectionSession.findMany({
      where: { studentId: student.id },
      orderBy: { createdAt: "desc" },
      include: {
        activities: true,
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
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
