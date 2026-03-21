import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";
import { notFound, redirect } from "next/navigation";
import SessionWizard from "@/components/session/SessionWizard";

export default async function SessionPage({
  params,
}: {
  params: Promise<{ sessionId: string }>;
}) {
  const student = await requireStudent();
  const { sessionId } = await params;

  const session = await prisma.reflectionSession.findFirst({
    where: { id: sessionId, studentId: student.id },
    include: {
      activities: { orderBy: { createdAt: "asc" } },
      reflections: { orderBy: { createdAt: "asc" } },
    },
  });

  if (!session) notFound();

  // Redirect if already completed
  if (session.completedAt) {
    redirect(`/reflect/${sessionId}/complete`);
  }

  // Get existing student activities (for suggestions)
  const allActivities = await prisma.activity.findMany({
    where: { studentId: student.id, isOngoing: true },
    orderBy: { createdAt: "desc" },
    take: 20,
  });

  return (
    <SessionWizard
      session={session}
      student={student}
      allActivities={allActivities}
    />
  );
}
