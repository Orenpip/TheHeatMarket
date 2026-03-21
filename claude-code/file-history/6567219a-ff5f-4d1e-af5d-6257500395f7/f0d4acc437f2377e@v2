import { View, Text, StyleSheet } from "react-native";

type Strength = "strong" | "moderate" | "emerging" | "new";

interface SignalBadgeProps {
  label: string;
  strength?: Strength;
}

const strengthColors: Record<
  Strength,
  { dot: string; bg: string; text: string; border: string }
> = {
  strong: { dot: "#10B981", bg: "#ECFDF5", text: "#065F46", border: "#A7F3D0" },
  moderate: { dot: "#F59E0B", bg: "#FFFBEB", text: "#92400E", border: "#FDE68A" },
  emerging: { dot: "#8B5CF6", bg: "#F5F3FF", text: "#4C1D95", border: "#DDD6FE" },
  new: { dot: "#3B82F6", bg: "#EFF6FF", text: "#1E3A8A", border: "#BFDBFE" },
};

export function SignalBadge({ label, strength = "moderate" }: SignalBadgeProps) {
  const colors = strengthColors[strength];

  return (
    <View
      style={[
        styles.container,
        {
          backgroundColor: colors.bg,
          borderColor: colors.border,
        },
      ]}
    >
      <View style={[styles.dot, { backgroundColor: colors.dot }]} />
      <Text style={[styles.label, { color: colors.text }]}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 100,
    borderWidth: 1,
    gap: 6,
    alignSelf: "flex-start",
  },
  dot: {
    width: 6,
    height: 6,
    borderRadius: 3,
  },
  label: {
    fontSize: 12,
    fontWeight: "500",
  },
});
