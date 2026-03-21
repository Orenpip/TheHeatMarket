"use client";

interface Notification {
  id: string;
  type: string;
  title: string;
  body: string;
  createdAt: Date;
}

const typeIcons: Record<string, string> = {
  REFLECTION_NUDGE: "✍️",
  OPPORTUNITY: "🌟",
  MAP_EXPANSION: "🗺️",
  PEER_PROMPT: "👥",
};

export default function NotificationPreview({
  notifications,
}: {
  notifications: Notification[];
}) {
  return (
    <div className="space-y-2">
      <h3 className="text-sm font-semibold text-[#6B7280] px-1">New for you</h3>
      {notifications.map((notif) => (
        <div key={notif.id} className="glass-card p-4">
          <div className="flex items-start gap-3">
            <span className="text-xl flex-shrink-0">
              {typeIcons[notif.type] ?? "📬"}
            </span>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-[#1A1A2E] truncate">
                {notif.title}
              </p>
              <p className="text-xs text-[#6B7280] mt-0.5 line-clamp-2">
                {notif.body}
              </p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
