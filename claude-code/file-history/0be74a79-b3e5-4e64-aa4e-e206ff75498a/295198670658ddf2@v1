import { NextResponse } from "next/server";
import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";
import { z } from "zod";

const updatePrivacySchema = z.object({
  shareInterestClusters: z.boolean().optional(),
  shareBreadthScore: z.boolean().optional(),
  shareTrajectoryShifts: z.boolean().optional(),
  shareCharacterSignals: z.boolean().optional(),
});

export async function GET() {
  try {
    const student = await requireStudent();

    const settings = await prisma.studentPrivacySettings.findUnique({
      where: { studentId: student.id },
    });

    return NextResponse.json(
      settings ?? {
        studentId: student.id,
        shareInterestClusters: true,
        shareBreadthScore: true,
        shareTrajectoryShifts: true,
        shareCharacterSignals: true,
      }
    );
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}

export async function PUT(req: Request) {
  try {
    const student = await requireStudent();
    const body = await req.json();
    const data = updatePrivacySchema.parse(body);

    const settings = await prisma.studentPrivacySettings.upsert({
      where: { studentId: student.id },
      update: data,
      create: {
        studentId: student.id,
        ...data,
      },
    });

    return NextResponse.json(settings);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
