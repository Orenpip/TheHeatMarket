import { View, StyleSheet, Text, Platform } from "react-native";
import { WebView } from "react-native-webview";
import { useUser } from "@clerk/clerk-expo";

const API_BASE = process.env.EXPO_PUBLIC_API_URL ?? "http://localhost:3000";

export default function MapScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Career & Education Map</Text>
        <Text style={styles.subtitle}>Tap any node to explore</Text>
      </View>

      {/* Embed the web map — full D3 experience */}
      <WebView
        source={{ uri: `${API_BASE}/map-embed` }}
        style={styles.webview}
        scrollEnabled={false}
        bounces={false}
        showsHorizontalScrollIndicator={false}
        showsVerticalScrollIndicator={false}
        javaScriptEnabled
        domStorageEnabled
        startInLoadingState
        renderLoading={() => (
          <View style={styles.loading}>
            <Text style={styles.loadingText}>Loading map...</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F2F4F7" },
  header: {
    paddingHorizontal: 20,
    paddingTop: Platform.OS === "ios" ? 60 : 20,
    paddingBottom: 12,
    gap: 2,
  },
  title: { fontSize: 20, fontWeight: "700", color: "#1A1A2E" },
  subtitle: { fontSize: 13, color: "#6B7280" },
  webview: { flex: 1 },
  loading: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#F2F4F7",
  },
  loadingText: { color: "#6B7280", fontSize: 14 },
});
