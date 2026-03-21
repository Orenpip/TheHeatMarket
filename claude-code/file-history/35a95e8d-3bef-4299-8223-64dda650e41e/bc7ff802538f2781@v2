"use client";

import { useState, useEffect } from "react";
import OpportunityForm from "./OpportunityForm";

interface Opportunity {
  id: string;
  title: string;
  category: string;
  status: string;
  deadline: string | null;
  interactionCount: number;
  isEmbedded: boolean;
  counselorId: string | null;
}

const CATEGORY_COLORS: Record<string, string> = {
  COMPETITION: "bg-orange-100 text-orange-700",
  RESEARCH: "bg-purple-100 text-purple-700",
  EVENT: "bg-blue-100 text-blue-700",
  HACKATHON: "bg-green-100 text-green-700",
  PROGRAM: "bg-indigo-100 text-indigo-700",
  CLUB: "bg-yellow-100 text-yellow-700",
  VOLUNTEER: "bg-teal-100 text-teal-700",
  PUBLICATION: "bg-rose-100 text-rose-700",
};

export default function OpportunityTable() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<Opportunity | null>(null);
  const [archiving, setArchiving] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/counselor/opportunities");
      if (res.ok) setOpportunities(await res.json());
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleArchive = async (id: string) => {
    if (!confirm("Archive this opportunity? Students will no longer see it.")) return;
    setArchiving(id);
    try {
      await fetch(`/api/counselor/opportunities/${id}`, { method: "DELETE" });
      setOpportunities((prev) => prev.filter((o) => o.id !== id));
    } finally {
      setArchiving(null);
    }
  };

  if (showForm || editing) {
    return (
      <div className="bg-white rounded-2xl border border-gray-200/60 p-6">
        <h2 className="text-base font-semibold text-[#1A1A2E] mb-4">
          {editing ? "Edit opportunity" : "Add new opportunity"}
        </h2>
        <OpportunityForm
          opportunityId={editing?.id}
          initial={editing ? {
            title: editing.title,
            category: editing.category,
            status: editing.status as "DRAFT" | "PUBLISHED",
          } : undefined}
          onSuccess={() => {
            setShowForm(false);
            setEditing(null);
            load();
          }}
          onCancel={() => {
            setShowForm(false);
            setEditing(null);
          }}
        />
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <p className="text-sm text-[#6B7280]">{opportunities.length} opportunities</p>
        <button
          onClick={() => setShowForm(true)}
          className="btn-primary py-2 px-4 text-sm"
        >
          + Add opportunity
        </button>
      </div>

      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-16 bg-gray-100 rounded-xl animate-pulse" />
          ))}
        </div>
      ) : opportunities.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-4xl mb-3">🎯</div>
          <p className="text-sm font-medium text-[#1A1A2E] mb-1">No opportunities yet</p>
          <p className="text-xs text-[#6B7280] mb-4">
            Add clubs, competitions, and local events your students can explore
          </p>
          <button onClick={() => setShowForm(true)} className="btn-primary py-2 px-4 text-sm">
            Add first opportunity
          </button>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-gray-200/60 overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left text-xs font-medium text-[#6B7280] px-4 py-3">Opportunity</th>
                <th className="text-left text-xs font-medium text-[#6B7280] px-4 py-3">Category</th>
                <th className="text-left text-xs font-medium text-[#6B7280] px-4 py-3">Deadline</th>
                <th className="text-left text-xs font-medium text-[#6B7280] px-4 py-3">Status</th>
                <th className="text-left text-xs font-medium text-[#6B7280] px-4 py-3">Views</th>
                <th className="px-4 py-3" />
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {opportunities.map((opp) => (
                <tr key={opp.id} className="hover:bg-gray-50/60 transition-colors">
                  <td className="px-4 py-3">
                    <p className="text-sm font-medium text-[#1A1A2E] line-clamp-1">{opp.title}</p>
                    {!opp.isEmbedded && (
                      <p className="text-[10px] text-yellow-600 mt-0.5">Indexing...</p>
                    )}
                  </td>
                  <td className="px-4 py-3">
                    <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full uppercase ${CATEGORY_COLORS[opp.category] ?? "bg-gray-100 text-gray-700"}`}>
                      {opp.category}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-xs text-[#6B7280]">
                    {opp.deadline
                      ? new Date(opp.deadline).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })
                      : "—"}
                  </td>
                  <td className="px-4 py-3">
                    <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full ${
                      opp.status === "PUBLISHED" ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-600"
                    }`}>
                      {opp.status === "PUBLISHED" ? "Live" : "Draft"}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-xs text-[#6B7280]">{opp.interactionCount}</td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2 justify-end">
                      <button
                        onClick={() => setEditing(opp)}
                        className="text-xs text-[#3B82F6] hover:underline"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleArchive(opp.id)}
                        disabled={archiving === opp.id}
                        className="text-xs text-red-400 hover:underline disabled:opacity-50"
                      >
                        {archiving === opp.id ? "..." : "Archive"}
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
