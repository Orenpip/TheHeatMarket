import { NextResponse } from "next/server";
import { requireStudent, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";

export async function PUT(
  _req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const student = await requireStudent();
    const { id } = await params;

    await prisma.notification.updateMany({
      where: { id, studentId: student.id, readAt: null },
      data: { readAt: new Date(), deliveredAt: new Date() },
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    return apiError(error);
  }
}
