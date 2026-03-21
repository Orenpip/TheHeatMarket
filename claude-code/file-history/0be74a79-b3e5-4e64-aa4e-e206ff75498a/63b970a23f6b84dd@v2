import { NextResponse } from "next/server";
import { requireStudent, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { z } from "zod";

const updatePrefsSchema = z.object({
  maxPerWeek: z.number().min(0).max(21).optional(),
  reflectionNudges: z.boolean().optional(),
  opportunityAlerts: z.boolean().optional(),
  mapExpansions: z.boolean().optional(),
  peerPrompts: z.boolean().optional(),
  quietHoursStart: z.string().regex(/^\d{2}:\d{2}$/).optional(),
  quietHoursEnd: z.string().regex(/^\d{2}:\d{2}$/).optional(),
});

export async function GET() {
  try {
    const student = await requireStudent();

    const prefs = await prisma.notificationPreferences.findUnique({
      where: { studentId: student.id },
    });

    return NextResponse.json(
      prefs ?? {
        studentId: student.id,
        maxPerWeek: 3,
        reflectionNudges: true,
        opportunityAlerts: true,
        mapExpansions: true,
        peerPrompts: true,
        quietHoursStart: "21:00",
        quietHoursEnd: "08:00",
      }
    );
  } catch (error) {
    return apiError(error);
  }
}

export async function PUT(req: Request) {
  try {
    const student = await requireStudent();
    const body = await req.json();
    const data = updatePrefsSchema.parse(body);

    const prefs = await prisma.notificationPreferences.upsert({
      where: { studentId: student.id },
      update: data,
      create: {
        studentId: student.id,
        ...data,
      },
    });

    return NextResponse.json(prefs);
  } catch (error) {
    return apiError(error);
  }
}
