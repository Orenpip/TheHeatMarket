import { NextResponse } from "next/server";
import { requireStudent, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { z } from "zod";

const updateSchema = z.object({
  responseText: z.string().optional(),
  isSharedWithCounselor: z.boolean().optional(),
});

export async function PATCH(
  req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const student = await requireStudent();
    const { id } = await params;
    const body = await req.json();
    const data = updateSchema.parse(body);

    const wordCount =
      data.responseText !== undefined
        ? data.responseText.trim().split(/\s+/).filter(Boolean).length
        : undefined;

    const result = await prisma.reflection.updateMany({
      where: { id, studentId: student.id },
      data: {
        ...data,
        ...(wordCount !== undefined ? { wordCount } : {}),
      },
    });

    if (result.count === 0) {
      return NextResponse.json({ error: "Not found" }, { status: 404 });
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    return apiError(error);
  }
}
