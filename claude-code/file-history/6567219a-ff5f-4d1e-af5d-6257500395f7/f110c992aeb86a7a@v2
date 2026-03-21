"use client";

import { motion } from "framer-motion";

function getBreadthLabel(score: number): string {
  if (score <= 20) return "Very Focused";
  if (score <= 40) return "Developing";
  if (score <= 60) return "Balanced";
  if (score <= 80) return "Broad";
  return "Highly Interdisciplinary";
}

function getBreadthColor(score: number): string {
  if (score <= 20) return "#EF4444";
  if (score <= 40) return "#F59E0B";
  if (score <= 60) return "#3B82F6";
  if (score <= 80) return "#10B981";
  return "#8B5CF6";
}

export default function BreadthBar({ score }: { score: number }) {
  const label = getBreadthLabel(score);
  const color = getBreadthColor(score);

  return (
    <div className="glass-card p-5">
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-medium text-[#1A1A2E] text-sm">
          Exploration Breadth
        </h3>
        <span className="text-xs font-semibold" style={{ color }}>
          {label}
        </span>
      </div>

      <div className="h-2.5 bg-gray-200/60 rounded-full overflow-hidden">
        <motion.div
          className="h-full rounded-full"
          style={{ backgroundColor: color }}
          initial={{ width: 0 }}
          animate={{ width: `${score}%` }}
          transition={{ duration: 0.8, ease: "easeOut", delay: 0.2 }}
        />
      </div>

      <div className="flex justify-between mt-1.5">
        <span className="text-[10px] text-[#9CA3AF]">Focused</span>
        <span className="text-[10px] text-[#9CA3AF] font-medium">
          {Math.round(score)}/100
        </span>
        <span className="text-[10px] text-[#9CA3AF]">Interdisciplinary</span>
      </div>
    </div>
  );
}
