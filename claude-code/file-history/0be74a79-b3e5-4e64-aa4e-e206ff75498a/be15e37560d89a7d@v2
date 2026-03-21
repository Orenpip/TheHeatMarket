import { NextResponse } from "next/server";
import { requireStudent, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { z } from "zod";
import { ActivityCategory } from "@compass/db";

const onboardingSchema = z.object({
  gradeLevel: z.number().min(9).max(12),
  initialActivities: z
    .array(
      z.object({
        category: z.nativeEnum(ActivityCategory),
        name: z.string().min(1).max(200),
        hoursPerWeek: z.number().optional(),
        excitement: z.number().min(1).max(5).optional(),
      })
    )
    .optional(),
});

export async function POST(req: Request) {
  try {
    const student = await requireStudent();
    const body = await req.json();
    const data = onboardingSchema.parse(body);

    // Update student grade + mark onboarding complete
    await prisma.student.update({
      where: { id: student.id },
      data: {
        gradeLevel: data.gradeLevel,
        onboardingCompleted: true,
      },
    });

    // Save initial activities if provided
    if (data.initialActivities && data.initialActivities.length > 0) {
      await prisma.activity.createMany({
        data: data.initialActivities.map((a) => ({
          studentId: student.id,
          category: a.category,
          name: a.name,
          hoursPerWeek: a.hoursPerWeek,
          excitement: a.excitement,
          isOngoing: true,
        })),
      });
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    return apiError(error);
  }
}
