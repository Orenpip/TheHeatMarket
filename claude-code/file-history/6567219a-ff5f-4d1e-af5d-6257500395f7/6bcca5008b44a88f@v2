import { BlurView } from "expo-blur";
import {
  StyleSheet,
  View,
  ViewStyle,
  Platform,
  StyleProp,
} from "react-native";

interface GlassCardProps {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  intensity?: number;
  padding?: number;
}

export function GlassCard({
  children,
  style,
  intensity = 60,
  padding = 20,
}: GlassCardProps) {
  if (Platform.OS === "ios") {
    return (
      <BlurView
        intensity={intensity}
        tint="light"
        style={[styles.card, { padding }, style]}
      >
        {children}
      </BlurView>
    );
  }

  // Android fallback — no blur, use white/semi-transparent
  return (
    <View style={[styles.card, styles.androidCard, { padding }, style]}>
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.18)",
    overflow: "hidden",
  },
  androidCard: {
    backgroundColor: "rgba(255,255,255,0.85)",
    shadowColor: "#1F2687",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 16,
    elevation: 4,
  },
});
