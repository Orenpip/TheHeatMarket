import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";
import Link from "next/link";

export default async function ReflectionsPage() {
  const student = await requireStudent();

  const sessions = await prisma.reflectionSession.findMany({
    where: { studentId: student.id },
    orderBy: { createdAt: "desc" },
    include: {
      template: { select: { title: true, orderNum: true } },
      activities: { select: { id: true, name: true } },
      reflections: {
        select: {
          id: true,
          promptType: true,
          wordCount: true,
          isSharedWithCounselor: true,
        },
      },
    },
  });

  const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
  ];

  function formatMonthKey(key: string): string {
    const [year, month] = key.split("-");
    if (!year || !month) return key;
    return `${monthNames[parseInt(month) - 1]} ${year}`;
  }

  return (
    <div className="space-y-5">
      <div className="pt-2">
        <h1 className="text-2xl font-bold text-[#1A1A2E]">
          Your Reflections
        </h1>
        <p className="text-sm text-[#6B7280] mt-1">
          {sessions.length} reflection session{sessions.length !== 1 ? "s" : ""}
        </p>
      </div>

      {sessions.length === 0 ? (
        <div className="glass-card p-8 text-center">
          <div className="text-4xl mb-3">📓</div>
          <h3 className="font-semibold text-[#1A1A2E] mb-1">
            No reflections yet
          </h3>
          <p className="text-sm text-[#6B7280] mb-4">
            Start your first monthly reflection to begin building your signal
            profile.
          </p>
          <Link href="/reflect" className="btn-primary">
            Start Reflecting
          </Link>
        </div>
      ) : (
        <div className="space-y-3">
          {sessions.map((session) => (
            <div key={session.id} className="glass-card p-5">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <h3 className="font-semibold text-[#1A1A2E]">
                    {session.template
                      ? `Reflection ${session.template.orderNum}: ${session.template.title}`
                      : session.monthKey
                      ? formatMonthKey(session.monthKey)
                      : "Reflection"}
                  </h3>
                  {session.completedAt ? (
                    <span className="text-xs text-emerald-600 font-medium">
                      ✓ Completed{" "}
                      {new Date(session.completedAt).toLocaleDateString(
                        "en-US",
                        { month: "short", day: "numeric" }
                      )}
                    </span>
                  ) : (
                    <span className="text-xs text-amber-600 font-medium">
                      In progress
                    </span>
                  )}
                </div>
                {!session.completedAt && (
                  <Link
                    href={`/reflect/${session.id}`}
                    className="text-sm text-[#3B82F6] font-medium hover:underline"
                  >
                    Continue →
                  </Link>
                )}
              </div>

              <div className="flex gap-4 text-xs text-[#6B7280]">
                <span>
                  {session.activities.length} activit
                  {session.activities.length !== 1 ? "ies" : "y"}
                </span>
                <span>
                  {session.reflections.length} reflection
                  {session.reflections.length !== 1 ? "s" : ""}
                </span>
                {session.durationSeconds && (
                  <span>
                    {Math.round(session.durationSeconds / 60)} min
                  </span>
                )}
              </div>

              {session.activities.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-1">
                  {session.activities.slice(0, 4).map((a) => (
                    <span
                      key={a.id}
                      className="text-[10px] px-2 py-0.5 bg-blue-50 text-blue-700 rounded-full"
                    >
                      {a.name}
                    </span>
                  ))}
                  {session.activities.length > 4 && (
                    <span className="text-[10px] text-[#9CA3AF]">
                      +{session.activities.length - 4} more
                    </span>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
