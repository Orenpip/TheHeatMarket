import { NextResponse } from "next/server";
import { requireStudent, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { z } from "zod";

const updateSchema = z.object({
  pulseScore: z.number().min(1).max(10).optional(),
  pulseNote: z.string().max(500).optional(),
});

export async function GET(
  _req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const student = await requireStudent();
    const { id } = await params;

    const session = await prisma.reflectionSession.findFirst({
      where: { id, studentId: student.id },
      include: {
        activities: { orderBy: { createdAt: "asc" } },
        reflections: { orderBy: { createdAt: "asc" } },
      },
    });

    if (!session) {
      return NextResponse.json({ error: "Not found" }, { status: 404 });
    }

    return NextResponse.json(session);
  } catch (error) {
    return apiError(error);
  }
}

export async function PATCH(
  req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const student = await requireStudent();
    const { id } = await params;
    const body = await req.json();
    const data = updateSchema.parse(body);

    const session = await prisma.reflectionSession.updateMany({
      where: { id, studentId: student.id },
      data,
    });

    if (session.count === 0) {
      return NextResponse.json({ error: "Not found" }, { status: 404 });
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    return apiError(error);
  }
}
