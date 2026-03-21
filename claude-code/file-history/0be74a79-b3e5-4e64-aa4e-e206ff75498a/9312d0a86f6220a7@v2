import { NextResponse } from "next/server";
import { requireStudent, apiError } from "@/lib/auth";
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
    // Return only fields the client needs — not clerkId or full relations
    return NextResponse.json({
      id: student.id,
      email: student.email,
      firstName: student.firstName,
      lastName: student.lastName,
      gradeLevel: student.gradeLevel,
      schoolId: student.schoolId,
      onboardingCompleted: student.onboardingCompleted,
    });
  } catch (error) {
    return apiError(error);
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

    return NextResponse.json({
      id: updated.id,
      firstName: updated.firstName,
      lastName: updated.lastName,
      gradeLevel: updated.gradeLevel,
    });
  } catch (error) {
    return apiError(error);
  }
}
