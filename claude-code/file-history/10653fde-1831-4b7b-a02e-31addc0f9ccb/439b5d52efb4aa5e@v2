import { NextResponse } from "next/server";
import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";
import { Client } from "@upstash/qstash";

export const maxDuration = 30;

function getQStash() {
  return new Client({ token: process.env.QSTASH_TOKEN! });
}

export async function POST(
  _req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const student = await requireStudent();
    const { id } = await params;

    const session = await prisma.reflectionSession.findFirst({
      where: { id, studentId: student.id },
    });

    if (!session) {
      return NextResponse.json({ error: "Not found" }, { status: 404 });
    }

    if (session.completedAt) {
      return NextResponse.json({ error: "Session already submitted" }, { status: 400 });
    }

    // Mark session as complete
    const now = new Date();
    const durationSeconds = Math.floor(
      (now.getTime() - session.createdAt.getTime()) / 1000
    );

    await prisma.reflectionSession.update({
      where: { id },
      data: {
        completedAt: now,
        durationSeconds,
      },
    });

    // Enqueue synthesis job via QStash
    const appUrl = process.env.NEXT_PUBLIC_APP_URL ?? "http://localhost:3000";
    await getQStash().publishJSON({
      url: `${appUrl}/api/webhooks/qstash`,
      body: {
        type: "POST_SESSION_SYNTHESIS",
        data: {
          studentId: student.id,
          sessionId: id,
        },
        triggeredAt: now.toISOString(),
      },
      // 30 second delay to let any last writes settle
      delay: 30,
    });

    return NextResponse.json({ success: true, completedAt: now });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
