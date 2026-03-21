import { View, Text, StyleSheet, TouchableOpacity } from "react-native";

interface Activity {
  id: string;
  name: string;
  category: string;
  excitement: number | null;
  hoursPerWeek: number | null;
  isOngoing: boolean;
}

const excitementEmojis = ["", "😐", "🙂", "😊", "😄", "🤩"];

const categoryColors: Record<string, string> = {
  ACADEMIC: "#3B82F6",
  EXTRACURRICULAR: "#10B981",
  READING: "#8B5CF6",
  PROJECT: "#F59E0B",
  WORK: "#6B7280",
  VOLUNTEER: "#EC4899",
  HOBBY: "#EF4444",
};

export function ActivityCard({
  activity,
  onDelete,
}: {
  activity: Activity;
  onDelete?: () => void;
}) {
  const categoryColor = categoryColors[activity.category] ?? "#6B7280";

  return (
    <View style={styles.card}>
      <View style={styles.header}>
        <View style={[styles.categoryDot, { backgroundColor: categoryColor }]} />
        <Text style={styles.name}>{activity.name}</Text>
        {activity.excitement !== null && (
          <Text style={styles.excitement}>
            {excitementEmojis[activity.excitement]}
          </Text>
        )}
        {onDelete && (
          <TouchableOpacity onPress={onDelete} style={styles.deleteBtn}>
            <Text style={styles.deleteText}>✕</Text>
          </TouchableOpacity>
        )}
      </View>
      <View style={styles.meta}>
        <Text style={styles.category}>{activity.category}</Text>
        {activity.hoursPerWeek && (
          <Text style={styles.hours}>{activity.hoursPerWeek} hrs/wk</Text>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: "rgba(255,255,255,0.6)",
    borderRadius: 12,
    padding: 12,
    borderWidth: 1,
    borderColor: "rgba(229,231,235,0.6)",
    marginBottom: 8,
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginBottom: 4,
  },
  categoryDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  name: {
    flex: 1,
    fontSize: 14,
    fontWeight: "500",
    color: "#1A1A2E",
  },
  excitement: {
    fontSize: 16,
  },
  deleteBtn: {
    padding: 4,
  },
  deleteText: {
    fontSize: 12,
    color: "#9CA3AF",
  },
  meta: {
    flexDirection: "row",
    gap: 12,
    paddingLeft: 16,
  },
  category: {
    fontSize: 11,
    color: "#9CA3AF",
    textTransform: "uppercase",
    letterSpacing: 0.5,
  },
  hours: {
    fontSize: 11,
    color: "#9CA3AF",
  },
});
