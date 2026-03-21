"use client";

import { useState } from "react";

interface OpportunityFormData {
  title: string;
  description: string;
  category: string;
  status: "DRAFT" | "PUBLISHED";
  url: string;
  location: string;
  organizerName: string;
  deadline: string;
  tags: string;
}

const CATEGORIES = [
  "COMPETITION", "RESEARCH", "EVENT", "HACKATHON",
  "PROGRAM", "CLUB", "VOLUNTEER", "PUBLICATION",
];

const EMPTY: OpportunityFormData = {
  title: "", description: "", category: "COMPETITION",
  status: "PUBLISHED", url: "", location: "",
  organizerName: "", deadline: "", tags: "",
};

export default function OpportunityForm({
  initial,
  opportunityId,
  onSuccess,
  onCancel,
}: {
  initial?: Partial<OpportunityFormData>;
  opportunityId?: string;
  onSuccess: () => void;
  onCancel: () => void;
}) {
  const [form, setForm] = useState<OpportunityFormData>({ ...EMPTY, ...initial });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const set = (field: keyof OpportunityFormData, value: string) =>
    setForm((prev) => ({ ...prev, [field]: value }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);

    const payload = {
      title: form.title,
      description: form.description,
      category: form.category,
      status: form.status,
      url: form.url || undefined,
      location: form.location || undefined,
      organizerName: form.organizerName || undefined,
      deadline: form.deadline ? new Date(form.deadline).toISOString() : undefined,
      tags: form.tags
        ? form.tags.split(",").map((t) => t.trim()).filter(Boolean)
        : [],
    };

    try {
      const url = opportunityId
        ? `/api/counselor/opportunities/${opportunityId}`
        : "/api/counselor/opportunities";
      const method = opportunityId ? "PATCH" : "POST";

      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error ?? "Failed to save");
      }

      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setSaving(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="col-span-2">
          <label className="block text-sm font-medium text-[#1A1A2E] mb-1">Title *</label>
          <input
            required
            value={form.title}
            onChange={(e) => set("title", e.target.value)}
            maxLength={200}
            placeholder="e.g. DECA State Competition"
            className="w-full px-3 py-2 text-sm border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#3B82F6]/30"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-[#1A1A2E] mb-1">Category *</label>
          <select
            value={form.category}
            onChange={(e) => set("category", e.target.value)}
            className="w-full px-3 py-2 text-sm border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#3B82F6]/30"
          >
            {CATEGORIES.map((c) => (
              <option key={c} value={c}>{c.charAt(0) + c.slice(1).toLowerCase()}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-[#1A1A2E] mb-1">Status</label>
          <select
            value={form.status}
            onChange={(e) => set("status", e.target.value as "DRAFT" | "PUBLISHED")}
            className="w-full px-3 py-2 text-sm border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#3B82F6]/30"
          >
            <option value="PUBLISHED">Published</option>
            <option value="DRAFT">Draft</option>
          </select>
        </div>

        <div className="col-span-2">
          <label className="block text-sm font-medium text-[#1A1A2E] mb-1">
            Description * <span className="text-[#6B7280] font-normal">(min 50 chars — more detail = better matching)</span>
          </label>
          <textarea
            required
            minLength={50}
            maxLength={2000}
            value={form.description}
            onChange={(e) => set("description", e.target.value)}
            rows={4}
            placeholder="Describe the opportunity, who it's for, what students gain, how to apply..."
            className="w-full px-3 py-2 text-sm border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#3B82F6]/30 resize-none"
          />
          <p className="text-xs text-[#6B7280] mt-1">{form.description.length}/2000</p>
        </div>

        <div>
          <label className="block text-sm font-medium text-[#1A1A2E] mb-1">Organizer</label>
          <input
            value={form.organizerName}
            onChange={(e) => set("organizerName", e.target.value)}
            placeholder="e.g. DECA Inc."
            className="w-full px-3 py-2 text-sm border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#3B82F6]/30"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-[#1A1A2E] mb-1">Location</label>
          <input
            value={form.location}
            onChange={(e) => set("location", e.target.value)}
            placeholder="e.g. Online, Boston MA"
            className="w-full px-3 py-2 text-sm border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#3B82F6]/30"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-[#1A1A2E] mb-1">Deadline</label>
          <input
            type="date"
            value={form.deadline}
            onChange={(e) => set("deadline", e.target.value)}
            className="w-full px-3 py-2 text-sm border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#3B82F6]/30"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-[#1A1A2E] mb-1">URL</label>
          <input
            type="url"
            value={form.url}
            onChange={(e) => set("url", e.target.value)}
            placeholder="https://..."
            className="w-full px-3 py-2 text-sm border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#3B82F6]/30"
          />
        </div>

        <div className="col-span-2">
          <label className="block text-sm font-medium text-[#1A1A2E] mb-1">Tags <span className="text-[#6B7280] font-normal">(comma-separated)</span></label>
          <input
            value={form.tags}
            onChange={(e) => set("tags", e.target.value)}
            placeholder="e.g. business, leadership, state-level"
            className="w-full px-3 py-2 text-sm border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#3B82F6]/30"
          />
        </div>
      </div>

      {error && <p className="text-sm text-red-500">{error}</p>}

      <div className="flex gap-3 pt-2">
        <button
          type="submit"
          disabled={saving}
          className="btn-primary py-2 px-6 text-sm disabled:opacity-50"
        >
          {saving ? "Saving..." : opportunityId ? "Save changes" : "Add opportunity"}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="py-2 px-4 text-sm text-[#6B7280] hover:text-[#1A1A2E] transition-colors"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}
