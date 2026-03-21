"use client";

import { cn } from "./utils";

interface PrivacyToggleProps {
  enabled: boolean;
  onChange: (enabled: boolean) => void;
  label?: string;
  description?: string;
  className?: string;
}

export function PrivacyToggle({
  enabled,
  onChange,
  label,
  description,
  className,
}: PrivacyToggleProps) {
  return (
    <div className={cn("flex items-center justify-between gap-4", className)}>
      {(label || description) && (
        <div className="flex-1">
          {label && (
            <p className="text-sm font-medium text-[#1A1A2E]">{label}</p>
          )}
          {description && (
            <p className="text-xs text-[#6B7280] mt-0.5">{description}</p>
          )}
        </div>
      )}
      <button
        role="switch"
        aria-checked={enabled}
        onClick={() => onChange(!enabled)}
        className={cn(
          "relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent",
          "transition-colors duration-200 ease-in-out",
          "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
          enabled ? "bg-[#3B82F6]" : "bg-gray-300"
        )}
      >
        <span
          className={cn(
            "pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0",
            "transition duration-200 ease-in-out",
            enabled ? "translate-x-5" : "translate-x-0"
          )}
        />
      </button>
    </div>
  );
}
