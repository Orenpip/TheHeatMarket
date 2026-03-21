import { View, Text, StyleSheet, TouchableOpacity } from "react-native";

interface Notification {
  id: string;
  type: string;
  title: string;
  body: string;
  readAt: string | null;
  createdAt: string;
}

const typeIcons: Record<string, string> = {
  REFLECTION_NUDGE: "✍️",
  OPPORTUNITY: "🌟",
  MAP_EXPANSION: "🗺️",
  PEER_PROMPT: "👥",
};

export function NotificationCard({
  notification,
  onPress,
}: {
  notification: Notification;
  onPress?: () => void;
}) {
  const isUnread = !notification.readAt;

  return (
    <TouchableOpacity
      style={[styles.card, isUnread && styles.unread]}
      onPress={onPress}
      activeOpacity={0.7}
    >
      <Text style={styles.icon}>
        {typeIcons[notification.type] ?? "📬"}
      </Text>
      <View style={styles.content}>
        <Text style={styles.title}>{notification.title}</Text>
        <Text style={styles.body} numberOfLines={2}>
          {notification.body}
        </Text>
        <Text style={styles.time}>
          {new Date(notification.createdAt).toLocaleDateString("en-US", {
            month: "short",
            day: "numeric",
          })}
        </Text>
      </View>
      {isUnread && <View style={styles.unreadDot} />}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: "row",
    alignItems: "flex-start",
    gap: 12,
    padding: 14,
    backgroundColor: "rgba(255,255,255,0.7)",
    borderRadius: 14,
    borderWidth: 1,
    borderColor: "rgba(229,231,235,0.5)",
    marginBottom: 8,
  },
  unread: {
    backgroundColor: "rgba(239,246,255,0.8)",
    borderColor: "rgba(191,219,254,0.6)",
  },
  icon: {
    fontSize: 20,
    marginTop: 2,
  },
  content: {
    flex: 1,
    gap: 2,
  },
  title: {
    fontSize: 14,
    fontWeight: "600",
    color: "#1A1A2E",
  },
  body: {
    fontSize: 12,
    color: "#6B7280",
    lineHeight: 17,
  },
  time: {
    fontSize: 11,
    color: "#9CA3AF",
    marginTop: 2,
  },
  unreadDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: "#3B82F6",
    marginTop: 4,
  },
});
