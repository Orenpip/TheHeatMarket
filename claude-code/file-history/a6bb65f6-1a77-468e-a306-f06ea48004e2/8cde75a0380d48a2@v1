"use client";

import { motion } from "framer-motion";

interface MapNode {
  id: string;
  type: string;
  label: string;
  description: string | null;
  metadata: Record<string, unknown>;
  similarity?: number;
}

const NODE_TYPE_LABELS: Record<string, string> = {
  CAREER: "Career",
  MAJOR: "College Major",
  INDUSTRY: "Industry",
  PROGRAM: "Program / Opportunity",
  SKILL: "Skill",
  VALUE: "Value",
};

const NODE_COLORS: Record<string, string> = {
  CAREER: "blue",
  MAJOR: "violet",
  INDUSTRY: "emerald",
  PROGRAM: "amber",
  SKILL: "red",
  VALUE: "pink",
};

export default function MapNodeDetail({
  node,
  onClose,
}: {
  node: MapNode;
  onClose: () => void;
}) {
  const meta = node.metadata;
  const color = NODE_COLORS[node.type] ?? "gray";

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 20 }}
      className="absolute top-20 right-4 z-30 w-80 glass-card p-5 max-h-[70vh] overflow-y-auto"
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div>
          <span
            className={`text-[10px] font-semibold px-2 py-0.5 rounded-full uppercase tracking-wide bg-${color}-100 text-${color}-800`}
          >
            {NODE_TYPE_LABELS[node.type] ?? node.type}
          </span>
          {node.similarity !== undefined && (
            <span className="ml-2 text-[10px] text-emerald-600 font-medium">
              {Math.round(node.similarity * 100)}% match
            </span>
          )}
        </div>
        <button
          onClick={onClose}
          className="text-[#6B7280] hover:text-[#1A1A2E] transition-colors"
        >
          ✕
        </button>
      </div>

      <h2 className="text-lg font-bold text-[#1A1A2E] mb-2">{node.label}</h2>

      {node.description && (
        <p className="text-sm text-[#6B7280] mb-4">{node.description}</p>
      )}

      {/* Metadata */}
      <div className="space-y-2.5">
        {meta.medianSalary != null && (
          <div className="flex items-center gap-2">
            <span className="text-xs text-[#9CA3AF] w-28 flex-shrink-0">
              Median Salary
            </span>
            <span className="text-xs font-medium text-[#1A1A2E]">
              {String(meta.medianSalary)}
            </span>
          </div>
        )}
        {meta.growthRate != null && (
          <div className="flex items-center gap-2">
            <span className="text-xs text-[#9CA3AF] w-28 flex-shrink-0">
              Job Growth
            </span>
            <span className="text-xs font-medium text-[#1A1A2E]">
              {String(meta.growthRate)}
            </span>
          </div>
        )}
        {meta.educationRequired != null && (
          <div className="flex items-center gap-2">
            <span className="text-xs text-[#9CA3AF] w-28 flex-shrink-0">
              Education
            </span>
            <span className="text-xs font-medium text-[#1A1A2E]">
              {String(meta.educationRequired)}
            </span>
          </div>
        )}
        {Array.isArray(meta.skills) && meta.skills.length > 0 && (
          <div>
            <span className="text-xs text-[#9CA3AF] block mb-1">
              Key Skills
            </span>
            <div className="flex flex-wrap gap-1">
              {(meta.skills as string[]).map((skill) => (
                <span
                  key={skill}
                  className="text-[10px] px-2 py-0.5 bg-gray-100 rounded-full text-[#6B7280]"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}
        {Array.isArray(meta.entryPaths) && meta.entryPaths.length > 0 && (
          <div>
            <span className="text-xs text-[#9CA3AF] block mb-1">
              Entry Paths
            </span>
            <ul className="space-y-0.5">
              {(meta.entryPaths as string[]).map((path) => (
                <li
                  key={path}
                  className="text-xs text-[#6B7280] flex items-center gap-1"
                >
                  <span className="text-[#3B82F6]">→</span> {path}
                </li>
              ))}
            </ul>
          </div>
        )}
        {meta.dayInTheLife != null && (
          <div>
            <span className="text-xs text-[#9CA3AF] block mb-1">
              Day in the Life
            </span>
            <p className="text-xs text-[#6B7280]">
              {String(meta.dayInTheLife)}
            </p>
          </div>
        )}
        {meta.deadline != null && (
          <div className="flex items-center gap-2">
            <span className="text-xs text-[#9CA3AF] w-28 flex-shrink-0">
              Deadline
            </span>
            <span className="text-xs font-medium text-amber-600">
              {String(meta.deadline)}
            </span>
          </div>
        )}
      </div>
    </motion.div>
  );
}
