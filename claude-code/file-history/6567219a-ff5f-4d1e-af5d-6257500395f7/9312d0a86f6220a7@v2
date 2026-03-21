import { NextResponse } from "next/server";
import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";
import { z } from "zod";

const updateProfileSchema = z.object({
  firstName: z.string().min(1).max(100).optional(),
  lastName: z.string().min(1).max(100).optional(),
  gradeLevel: z.number().min(9).max(12).optional(),
});

export async function GET() {
  try {
    const student = await requireStudent();
    return NextResponse.json(student);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}

export async function PUT(req: Request) {
  try {
    const student = await requireStudent();
    const body = await req.json();
    const data = updateProfileSchema.parse(body);

    const updated = await prisma.student.update({
      where: { id: student.id },
      data,
    });

    return NextResponse.json(updated);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
