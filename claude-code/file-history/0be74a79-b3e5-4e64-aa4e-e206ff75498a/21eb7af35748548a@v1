import { NextResponse } from "next/server";
import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";

export async function PUT(
  _req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const student = await requireStudent();
    const { id } = await params;

    await prisma.notification.updateMany({
      where: { id, studentId: student.id },
      data: { actedOn: true, readAt: new Date() },
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
