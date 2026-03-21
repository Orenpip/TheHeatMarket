import type { Config } from "tailwindcss";

const compassTailwindConfig: Partial<Config> = {
  theme: {
    extend: {
      colors: {
        // Glass OS Design System
        "glass-white": "rgba(255,255,255,0.72)",
        "glass-border": "rgba(255,255,255,0.18)",
        "bg-primary": "#F2F4F7",
        "bg-secondary": "#E8EBF0",
        "bg-dark": "#0F1117",

        // Brand
        "accent-primary": "#3B82F6",
        "accent-secondary": "#6366F1",
        "accent-warm": "#F59E0B",

        // Signal Strengths
        "signal-strong": "#10B981",
        "signal-moderate": "#F59E0B",
        "signal-emerging": "#8B5CF6",
        "signal-new": "#3B82F6",

        // Text
        "text-primary": "#1A1A2E",
        "text-secondary": "#6B7280",
        "text-muted": "#9CA3AF",
        "text-inverse": "#FFFFFF",

        // Node Types (Map)
        "node-career": "#3B82F6",
        "node-major": "#8B5CF6",
        "node-industry": "#10B981",
        "node-program": "#F59E0B",
        "node-skill": "#EF4444",
        "node-value": "#EC4899",

        // Status
        "status-active": "#10B981",
        "status-warning": "#F59E0B",
        "status-inactive": "#EF4444",
      },
      fontFamily: {
        sans: ["Inter var", "Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      backdropBlur: {
        glass: "20px",
        "glass-heavy": "40px",
      },
      backdropSaturate: {
        glass: "180%",
      },
      boxShadow: {
        glass: "0 8px 32px 0 rgba(31,38,135,0.15)",
        "glass-hover": "0 12px 40px 0 rgba(31,38,135,0.25)",
        "glass-inset": "inset 0 1px 0 0 rgba(255,255,255,0.6)",
        "node-glow": "0 0 20px rgba(59,130,246,0.4)",
        "node-glow-strong": "0 0 30px rgba(59,130,246,0.6)",
      },
      borderRadius: {
        glass: "16px",
        "glass-lg": "24px",
        "glass-xl": "32px",
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "fade-up": "fadeUp 0.4s ease-out",
        "scale-in": "scaleIn 0.3s ease-out",
        "slide-in": "slideIn 0.3s ease-out",
        shimmer: "shimmer 2s linear infinite",
      },
      keyframes: {
        fadeUp: {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        scaleIn: {
          "0%": { opacity: "0", transform: "scale(0.95)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        slideIn: {
          "0%": { opacity: "0", transform: "translateX(-10px)" },
          "100%": { opacity: "1", transform: "translateX(0)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
    },
  },
  plugins: [],
};

export default compassTailwindConfig;
