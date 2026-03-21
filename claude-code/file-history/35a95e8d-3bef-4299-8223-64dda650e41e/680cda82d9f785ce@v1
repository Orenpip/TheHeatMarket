"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { UserButton } from "@clerk/nextjs";

interface Counselor {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  school: {
    name: string;
  };
}

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: "🏠" },
  { href: "/flags", label: "Needs Attention", icon: "🚩" },
];

export default function CounselorSidebar({
  counselor,
}: {
  counselor: Counselor;
}) {
  const pathname = usePathname();

  return (
    <div className="fixed left-0 top-0 h-full w-64 bg-white/80 backdrop-blur-[20px] border-r border-gray-200/40 flex flex-col z-40">
      {/* Header */}
      <div className="p-6 border-b border-gray-200/40">
        <div className="text-xl font-bold text-[#1A1A2E] mb-1">🧭 COMPASS</div>
        <div className="text-xs text-[#6B7280]">{counselor.school.name}</div>
      </div>

      {/* Nav */}
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                isActive
                  ? "bg-[#3B82F6] text-white shadow-md"
                  : "text-[#6B7280] hover:bg-gray-100/60 hover:text-[#1A1A2E]"
              }`}
            >
              <span>{item.icon}</span>
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200/40">
        <div className="flex items-center gap-3">
          <UserButton afterSignOutUrl="/sign-in" />
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-[#1A1A2E] truncate">
              {counselor.firstName} {counselor.lastName}
            </p>
            <p className="text-xs text-[#6B7280] truncate">{counselor.email}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
