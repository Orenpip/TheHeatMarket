"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

interface Prompt {
  promptText: string;
  promptType: "PATTERN" | "EXPLORATION" | "IDENTITY" | "CHALLENGE";
}

interface Template {
  id: string;
  title: string;
  description: string | null;
  orderNum: number;
  yearKey: string;
  prompts: unknown;
  isActive: boolean;
  _count: { sessions: number };
}

const PROMPT_TYPES = ["PATTERN", "EXPLORATION", "IDENTITY", "CHALLENGE"] as const;

const CURRENT_YEAR = String(new Date().getFullYear());

function emptyPrompt(): Prompt {
  return { promptText: "", promptType: "PATTERN" };
}

function parsePrompts(raw: unknown): Prompt[] {
  if (!Array.isArray(raw)) return [emptyPrompt()];
  return raw.map((p) => ({
    promptText: (p as Prompt).promptText ?? "",
    promptType: (p as Prompt).promptType ?? "PATTERN",
  }));
}

function TemplateForm({
  initial,
  existingOrders,
  onSave,
  onCancel,
}: {
  initial?: Partial<Template>;
  existingOrders: number[];
  onSave: (data: object) => Promise<void>;
  onCancel: () => void;
}) {
  const [title, setTitle] = useState(initial?.title ?? "");
  const [description, setDescription] = useState(initial?.description ?? "");
  const [orderNum, setOrderNum] = useState(initial?.orderNum ?? (Math.max(0, ...existingOrders) + 1));
  const [yearKey, setYearKey] = useState(initial?.yearKey ?? CURRENT_YEAR);
  const [prompts, setPrompts] = useState<Prompt[]>(
    initial?.prompts ? parsePrompts(initial.prompts) : [emptyPrompt(), emptyPrompt()]
  );
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function updatePrompt(i: number, field: keyof Prompt, value: string) {
    setPrompts((prev) => prev.map((p, idx) => (idx === i ? { ...p, [field]: value } : p)));
  }

  function addPrompt() {
    setPrompts((prev) => [...prev, emptyPrompt()]);
  }

  function removePrompt(i: number) {
    setPrompts((prev) => prev.filter((_, idx) => idx !== i));
  }

  async function handleSave() {
    if (!title.trim() || prompts.some((p) => !p.promptText.trim())) {
      setError("Title and all prompt texts are required.");
      return;
    }
    setSaving(true);
    setError(null);
    try {
      await onSave({ title, description, orderNum, yearKey, prompts });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="border border-gray-200 rounded-2xl p-5 space-y-4 bg-white">
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="text-xs font-medium text-[#6B7280] block mb-1">Title</label>
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g. Finding Your Threads"
            className="w-full px-3 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40"
          />
        </div>
        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="text-xs font-medium text-[#6B7280] block mb-1">Order #</label>
            <input
              type="number"
              value={orderNum}
              onChange={(e) => setOrderNum(parseInt(e.target.value) || 1)}
              min={1}
              className="w-full px-3 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40"
            />
          </div>
          <div>
            <label className="text-xs font-medium text-[#6B7280] block mb-1">Year</label>
            <input
              value={yearKey}
              onChange={(e) => setYearKey(e.target.value)}
              placeholder="2026"
              className="w-full px-3 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40"
            />
          </div>
        </div>
      </div>

      <div>
        <label className="text-xs font-medium text-[#6B7280] block mb-1">Description (shown to student before starting)</label>
        <input
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Optional — what this reflection is about"
          className="w-full px-3 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40"
        />
      </div>

      <div className="space-y-3">
        <label className="text-xs font-medium text-[#6B7280] block">Prompts</label>
        {prompts.map((p, i) => (
          <div key={i} className="flex gap-2 items-start">
            <span className="flex-shrink-0 w-5 h-5 mt-2 bg-[#3B82F6] text-white text-[10px] rounded-full flex items-center justify-center font-medium">
              {i + 1}
            </span>
            <div className="flex-1 space-y-1.5">
              <textarea
                value={p.promptText}
                onChange={(e) => updatePrompt(i, "promptText", e.target.value)}
                placeholder="Write your reflection prompt here..."
                rows={2}
                className="w-full px-3 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 resize-none"
              />
              <select
                value={p.promptType}
                onChange={(e) => updatePrompt(i, "promptType", e.target.value)}
                className="px-2 py-1 border border-gray-200 rounded-lg text-xs text-[#6B7280] focus:outline-none"
              >
                {PROMPT_TYPES.map((t) => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>
            {prompts.length > 1 && (
              <button onClick={() => removePrompt(i)} className="mt-2 text-red-400 hover:text-red-600 text-sm">×</button>
            )}
          </div>
        ))}
        <button
          onClick={addPrompt}
          className="text-sm text-[#3B82F6] hover:underline"
        >
          + Add prompt
        </button>
      </div>

      {error && <p className="text-sm text-red-600">{error}</p>}

      <div className="flex gap-2 justify-end">
        <button onClick={onCancel} className="px-4 py-2 text-sm text-[#6B7280] hover:text-[#1A1A2E]">
          Cancel
        </button>
        <button
          onClick={handleSave}
          disabled={saving}
          className="px-4 py-2 text-sm bg-[#3B82F6] text-white rounded-xl hover:bg-[#2563EB] disabled:opacity-60"
        >
          {saving ? "Saving..." : "Save Template"}
        </button>
      </div>
    </div>
  );
}

export default function TemplateManager({ templates: initial }: { templates: Template[] }) {
  const router = useRouter();
  const [templates, setTemplates] = useState(initial);
  const [creating, setCreating] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  const existingOrders = templates.map((t) => t.orderNum);

  async function handleCreate(data: object) {
    const res = await fetch("/api/admin/templates", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json() as { error: string };
      throw new Error(err.error);
    }
    setCreating(false);
    router.refresh();
  }

  async function handleUpdate(id: string, data: object) {
    const res = await fetch(`/api/admin/templates/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json() as { error: string };
      throw new Error(err.error);
    }
    setEditingId(null);
    router.refresh();
  }

  async function handleDelete(id: string) {
    if (!confirm("Delete this template? Students who haven't started it will no longer see it.")) return;
    const res = await fetch(`/api/admin/templates/${id}`, { method: "DELETE" });
    if (!res.ok) {
      alert("Failed to delete template. Please try again.");
      return;
    }
    setTemplates((prev) => prev.filter((t) => t.id !== id));
  }

  async function handleToggleActive(t: Template) {
    const res = await fetch(`/api/admin/templates/${t.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ isActive: !t.isActive }),
    });
    if (!res.ok) {
      alert("Failed to update template. Please try again.");
      return;
    }
    router.refresh();
  }

  return (
    <div className="space-y-4">
      {templates.map((t) => {
        const parsedPrompts = parsePrompts(t.prompts);
        return (
          <div key={t.id} className={`border rounded-2xl p-4 ${t.isActive ? "border-gray-200 bg-white" : "border-gray-100 bg-gray-50 opacity-60"}`}>
            {editingId === t.id ? (
              <TemplateForm
                initial={t}
                existingOrders={existingOrders.filter((o) => o !== t.orderNum)}
                onSave={(data) => handleUpdate(t.id, data)}
                onCancel={() => setEditingId(null)}
              />
            ) : (
              <div>
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-medium text-[#9CA3AF]">{t.yearKey} · #{t.orderNum}</span>
                      {!t.isActive && <span className="text-[10px] px-2 py-0.5 bg-gray-200 text-gray-500 rounded-full">Inactive</span>}
                    </div>
                    <h3 className="font-semibold text-[#1A1A2E] mt-0.5">{t.title}</h3>
                    {t.description && <p className="text-sm text-[#6B7280] mt-0.5">{t.description}</p>}
                    <p className="text-xs text-[#9CA3AF] mt-1">
                      {parsedPrompts.length} prompt{parsedPrompts.length !== 1 ? "s" : ""} · {t._count.sessions} session{t._count.sessions !== 1 ? "s" : ""} started
                    </p>
                  </div>
                  <div className="flex items-center gap-2 flex-shrink-0">
                    <button onClick={() => handleToggleActive(t)} className="text-xs text-[#6B7280] hover:text-[#1A1A2E]">
                      {t.isActive ? "Deactivate" : "Activate"}
                    </button>
                    <button onClick={() => setEditingId(t.id)} className="text-xs text-[#3B82F6] hover:underline">
                      Edit
                    </button>
                    <button onClick={() => handleDelete(t.id)} className="text-xs text-red-400 hover:text-red-600">
                      Delete
                    </button>
                  </div>
                </div>
                <div className="mt-3 space-y-1.5">
                  {parsedPrompts.map((p, i) => (
                    <div key={i} className="flex items-start gap-2">
                      <span className="text-[10px] px-1.5 py-0.5 bg-blue-50 text-blue-600 rounded font-medium flex-shrink-0 mt-0.5">{p.promptType}</span>
                      <p className="text-sm text-[#374151]">{p.promptText}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        );
      })}

      {creating ? (
        <TemplateForm
          existingOrders={existingOrders}
          onSave={handleCreate}
          onCancel={() => setCreating(false)}
        />
      ) : (
        <button
          onClick={() => setCreating(true)}
          className="w-full py-3 border-2 border-dashed border-gray-200 rounded-2xl text-sm text-[#6B7280] hover:border-blue-300 hover:text-[#3B82F6] transition-colors"
        >
          + New Template
        </button>
      )}
    </div>
  );
}
