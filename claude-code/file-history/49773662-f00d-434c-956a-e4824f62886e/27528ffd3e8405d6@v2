import { requireAdmin } from "@/lib/auth";
import { prisma } from "@compass/db";
import TemplateManager from "@/components/admin/TemplateManager";

export default async function TemplatesAdminPage() {
  await requireAdmin();

  const templates = await prisma.reflectionTemplate.findMany({
    orderBy: [{ yearKey: "desc" }, { orderNum: "asc" }],
    include: {
      _count: { select: { sessions: true } },
    },
  });

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-[#1A1A2E]">Reflection Templates</h1>
        <p className="text-sm text-[#6B7280] mt-1">
          Write and manage the reflection prompts students receive throughout the year.
        </p>
      </div>
      <TemplateManager templates={templates} />
    </div>
  );
}
