import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";
import { redirect } from "next/navigation";
import Link from "next/link";
import StartSessionButton from "@/components/session/StartSessionButton";

const COOLDOWN_DAYS = 21;

export default async function ReflectPage() {
  const student = await requireStudent();
  const now = new Date();

  // Resume in-progress session if any
  const inProgress = await prisma.reflectionSession.findFirst({
    where: { studentId: student.id, completedAt: null },
    orderBy: { createdAt: "desc" },
  });
  if (inProgress) {
    redirect(`/reflect/${inProgress.id}`);
  }

  // Get last completed session for cooldown check
  const lastCompleted = await prisma.reflectionSession.findFirst({
    where: { studentId: student.id, completedAt: { not: null } },
    orderBy: { completedAt: "desc" },
    include: { template: { select: { title: true, orderNum: true } } },
  });

  // Check cooldown
  let daysLeft = 0;
  if (lastCompleted?.completedAt) {
    const unlockDate = new Date(lastCompleted.completedAt);
    unlockDate.setDate(unlockDate.getDate() + COOLDOWN_DAYS);
    daysLeft = Math.max(0, Math.ceil((unlockDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24)));
  }

  // Find next available template
  const currentYear = String(now.getFullYear());
  const startedTemplateIds = (
    await prisma.reflectionSession.findMany({
      where: { studentId: student.id, templateId: { not: null } },
      select: { templateId: true },
    })
  ).map((s) => s.templateId!);

  const nextTemplate = await prisma.reflectionTemplate.findFirst({
    where: { yearKey: currentYear, isActive: true, id: { notIn: startedTemplateIds } },
    orderBy: { orderNum: "asc" },
  });

  const totalTemplates = await prisma.reflectionTemplate.count({
    where: { yearKey: currentYear, isActive: true },
  });

  const completedCount = startedTemplateIds.length;

  // All done for the year
  if (!nextTemplate) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="glass-card p-8 text-center max-w-sm">
          <div className="text-5xl mb-4">🎉</div>
          <h2 className="text-xl font-bold text-[#1A1A2E] mb-2">
            All reflections complete for {currentYear}
          </h2>
          <p className="text-[#6B7280] text-sm mb-6">
            You&apos;ve finished all {totalTemplates} reflections this year. Check back next year.
          </p>
          <Link href="/" className="btn-primary">Back to Home</Link>
        </div>
      </div>
    );
  }

  // In cooldown
  if (daysLeft > 0) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="glass-card p-8 text-center max-w-sm">
          <div className="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center text-2xl font-bold text-[#3B82F6] mx-auto mb-4">
            {daysLeft}
          </div>
          <h2 className="text-xl font-bold text-[#1A1A2E] mb-2">
            Next reflection opens in {daysLeft} day{daysLeft !== 1 ? "s" : ""}
          </h2>
          <p className="text-[#6B7280] text-sm mb-2">
            Up next: <span className="font-medium text-[#1A1A2E]">Reflection {nextTemplate.orderNum}: {nextTemplate.title}</span>
          </p>
          <p className="text-xs text-[#9CA3AF] mb-6">
            {completedCount} of {totalTemplates} reflections done this year
          </p>
          <Link href="/" className="btn-primary">Back to Home</Link>
        </div>
      </div>
    );
  }

  // Ready to start next reflection
  return (
    <div className="min-h-[60vh] flex items-center justify-center">
      <div className="glass-card p-8 text-center max-w-sm">
        <div className="text-5xl mb-4">🧭</div>
        <p className="text-xs text-[#9CA3AF] mb-1 uppercase tracking-wide font-medium">
          Reflection {nextTemplate.orderNum} of {totalTemplates}
        </p>
        <h2 className="text-xl font-bold text-[#1A1A2E] mb-2">
          {nextTemplate.title}
        </h2>
        {nextTemplate.description && (
          <p className="text-[#6B7280] text-sm mb-6">{nextTemplate.description}</p>
        )}
        {!nextTemplate.description && (
          <p className="text-[#6B7280] text-sm mb-6">
            10–15 minutes to capture what&apos;s been on your mind.
          </p>
        )}
        <StartSessionButton />
      </div>
    </div>
  );
}
