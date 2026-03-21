import { requireCounselor } from "@/lib/auth";
import OpportunityTable from "@/components/counselor/OpportunityTable";

export default async function OpportunitiesPage() {
  await requireCounselor();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-[#1A1A2E]">Opportunity Management</h1>
        <p className="text-[#6B7280] text-sm mt-1">
          Add clubs, competitions, and events for your students. The AI will match them to students based on their interests.
        </p>
      </div>
      <OpportunityTable />
    </div>
  );
}
