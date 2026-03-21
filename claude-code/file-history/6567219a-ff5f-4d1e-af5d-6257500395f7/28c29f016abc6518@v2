"use client";
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  Switch,
  Alert,
  ActivityIndicator,
  Platform,
} from "react-native";
import { useEffect, useState } from "react";
import { useAuth } from "@clerk/clerk-expo";
import { api } from "@/lib/api";
import { GlassCard } from "@/components/GlassCard";

interface SignalProfile {
  breadthScore: number;
  interestClusters: Array<{ id: string; label: string; strength: string; trend: string }>;
  characterSignals: Array<{ trait: string; description: string; confidence: string }>;
  lastSynthesizedAt: string | null;
}

interface PrivacySettings {
  shareInterestClusters: boolean;
  shareBreadthScore: boolean;
  shareTrajectoryShifts: boolean;
  shareCharacterSignals: boolean;
}

const STRENGTH_COLORS: Record<string, string> = {
  strong: "#10B981",
  moderate: "#F59E0B",
  emerging: "#8B5CF6",
};

const TREND_ICONS: Record<string, string> = {
  rising: "↑",
  stable: "→",
  declining: "↓",
};

export default function ProfileScreen() {
  const { signOut } = useAuth();
  const [profile, setProfile] = useState<SignalProfile | null>(null);
  const [privacy, setPrivacy] = useState<PrivacySettings | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.getSignalProfile().catch(() => null),
      api.getPrivacySettings().catch(() => null),
    ]).then(([p, pv]) => {
      if (p) setProfile(p as SignalProfile);
      if (pv) setPrivacy(pv as PrivacySettings);
    }).finally(() => setLoading(false));
  }, []);

  async function updatePrivacy(key: keyof PrivacySettings, value: boolean) {
    if (!privacy) return;
    const updated = { ...privacy, [key]: value };
    setPrivacy(updated);
    try {
      await api.updatePrivacySettings(updated);
    } catch {
      setPrivacy(privacy); // rollback
    }
  }

  async function handleSignOut() {
    Alert.alert(
      "Sign Out",
      "Are you sure you want to sign out?",
      [
        { text: "Cancel", style: "cancel" },
        {
          text: "Sign Out",
          style: "destructive",
          onPress: () => signOut(),
        },
      ]
    );
  }

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator color="#3B82F6" />
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      showsVerticalScrollIndicator={false}
    >
      <View style={styles.header}>
        <Text style={styles.title}>Profile</Text>
      </View>

      {/* Signal Profile */}
      {profile ? (
        <>
          <GlassCard style={styles.card}>
            <Text style={styles.sectionTitle}>Exploration Breadth</Text>
            <View style={styles.breadthRow}>
              <View style={styles.breadthBar}>
                <View
                  style={[
                    styles.breadthFill,
                    { width: `${Math.min(profile.breadthScore, 100)}%` as any },
                  ]}
                />
              </View>
              <Text style={styles.breadthScore}>
                {Math.round(profile.breadthScore)}/100
              </Text>
            </View>
            {profile.lastSynthesizedAt && (
              <Text style={styles.metaText}>
                Last updated{" "}
                {new Date(profile.lastSynthesizedAt).toLocaleDateString()}
              </Text>
            )}
          </GlassCard>

          {profile.interestClusters.length > 0 && (
            <GlassCard style={styles.card}>
              <Text style={styles.sectionTitle}>Interest Signals</Text>
              <View style={styles.clusterList}>
                {profile.interestClusters.slice(0, 6).map((cluster) => (
                  <View key={cluster.id} style={styles.clusterRow}>
                    <View
                      style={[
                        styles.clusterDot,
                        {
                          backgroundColor:
                            STRENGTH_COLORS[cluster.strength] ?? "#9CA3AF",
                        },
                      ]}
                    />
                    <Text style={styles.clusterLabel}>{cluster.label}</Text>
                    <Text style={styles.trendIcon}>
                      {TREND_ICONS[cluster.trend] ?? "→"}
                    </Text>
                  </View>
                ))}
              </View>
            </GlassCard>
          )}

          {profile.characterSignals.length > 0 && (
            <GlassCard style={styles.card}>
              <Text style={styles.sectionTitle}>Character Signals</Text>
              {profile.characterSignals.slice(0, 4).map((signal, i) => (
                <View key={i} style={styles.signalRow}>
                  <View
                    style={[
                      styles.signalDot,
                      {
                        backgroundColor:
                          signal.confidence === "high"
                            ? "#10B981"
                            : signal.confidence === "medium"
                            ? "#F59E0B"
                            : "#D1D5DB",
                      },
                    ]}
                  />
                  <View style={styles.signalText}>
                    <Text style={styles.signalTrait}>{signal.trait}</Text>
                    <Text style={styles.signalDesc}>{signal.description}</Text>
                  </View>
                </View>
              ))}
            </GlassCard>
          )}
        </>
      ) : (
        <GlassCard style={styles.card}>
          <View style={styles.emptyProfile}>
            <Text style={styles.emptyIcon}>🧭</Text>
            <Text style={styles.emptyTitle}>No signal profile yet</Text>
            <Text style={styles.emptyText}>
              Complete your first monthly reflection to start building your
              signal profile.
            </Text>
          </View>
        </GlassCard>
      )}

      {/* Privacy Settings */}
      {privacy && (
        <GlassCard style={styles.card}>
          <Text style={styles.sectionTitle}>Counselor Sharing</Text>
          <Text style={styles.sectionSubtitle}>
            Control what your counselor can see
          </Text>

          {[
            {
              key: "shareInterestClusters" as const,
              label: "Interest Signals",
              desc: "Your interest areas and trends",
            },
            {
              key: "shareBreadthScore" as const,
              label: "Exploration Breadth",
              desc: "Your interest diversity score",
            },
            {
              key: "shareTrajectoryShifts" as const,
              label: "Interest Shifts",
              desc: "How your interests have changed",
            },
            {
              key: "shareCharacterSignals" as const,
              label: "Character Signals",
              desc: "Patterns in how you engage",
            },
          ].map(({ key, label, desc }) => (
            <View key={key} style={styles.privacyRow}>
              <View style={styles.privacyText}>
                <Text style={styles.privacyLabel}>{label}</Text>
                <Text style={styles.privacyDesc}>{desc}</Text>
              </View>
              <Switch
                value={privacy[key]}
                onValueChange={(v) => updatePrivacy(key, v)}
                trackColor={{ false: "#D1D5DB", true: "#93C5FD" }}
                thumbColor={privacy[key] ? "#3B82F6" : "#F9FAFB"}
              />
            </View>
          ))}
        </GlassCard>
      )}

      {/* Account */}
      <GlassCard style={styles.card}>
        <Text style={styles.sectionTitle}>Account</Text>
        <TouchableOpacity
          style={styles.signOutButton}
          onPress={handleSignOut}
        >
          <Text style={styles.signOutText}>Sign Out</Text>
        </TouchableOpacity>
      </GlassCard>

      <View style={styles.footer}>
        <Text style={styles.footerText}>COMPASS v1.0</Text>
        <Text style={styles.footerText}>Your data belongs to you.</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F2F4F7" },
  content: { padding: 20, paddingBottom: 40, gap: 12 },
  centered: { flex: 1, justifyContent: "center", alignItems: "center" },
  header: {
    paddingTop: Platform.OS === "ios" ? 16 : 8,
    marginBottom: 4,
  },
  title: { fontSize: 24, fontWeight: "700", color: "#1A1A2E" },
  card: { gap: 8 },
  sectionTitle: { fontSize: 14, fontWeight: "600", color: "#1A1A2E", marginBottom: 2 },
  sectionSubtitle: { fontSize: 12, color: "#6B7280", marginBottom: 10 },
  breadthRow: { flexDirection: "row", alignItems: "center", gap: 10 },
  breadthBar: {
    flex: 1,
    height: 6,
    backgroundColor: "rgba(209,213,219,0.6)",
    borderRadius: 3,
    overflow: "hidden",
  },
  breadthFill: { height: "100%", backgroundColor: "#3B82F6", borderRadius: 3 },
  breadthScore: { fontSize: 13, fontWeight: "700", color: "#3B82F6", minWidth: 50 },
  metaText: { fontSize: 11, color: "#9CA3AF", marginTop: 2 },
  clusterList: { gap: 8 },
  clusterRow: { flexDirection: "row", alignItems: "center", gap: 8 },
  clusterDot: { width: 8, height: 8, borderRadius: 4 },
  clusterLabel: { flex: 1, fontSize: 13, color: "#1A1A2E" },
  trendIcon: { fontSize: 13, color: "#6B7280" },
  signalRow: { flexDirection: "row", alignItems: "flex-start", gap: 10, marginBottom: 8 },
  signalDot: { width: 8, height: 8, borderRadius: 4, marginTop: 4 },
  signalText: { flex: 1 },
  signalTrait: { fontSize: 13, fontWeight: "600", color: "#1A1A2E" },
  signalDesc: { fontSize: 12, color: "#6B7280", marginTop: 2 },
  emptyProfile: { alignItems: "center", paddingVertical: 20, gap: 8 },
  emptyIcon: { fontSize: 36 },
  emptyTitle: { fontSize: 15, fontWeight: "600", color: "#1A1A2E" },
  emptyText: { fontSize: 12, color: "#6B7280", textAlign: "center", lineHeight: 18 },
  privacyRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(209,213,219,0.3)",
  },
  privacyText: { flex: 1, marginRight: 12 },
  privacyLabel: { fontSize: 13, fontWeight: "500", color: "#1A1A2E" },
  privacyDesc: { fontSize: 11, color: "#9CA3AF", marginTop: 1 },
  signOutButton: {
    backgroundColor: "rgba(239,68,68,0.08)",
    borderRadius: 10,
    padding: 12,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "rgba(239,68,68,0.2)",
  },
  signOutText: { fontSize: 14, fontWeight: "600", color: "#EF4444" },
  footer: { alignItems: "center", gap: 2, paddingTop: 8 },
  footerText: { fontSize: 11, color: "#9CA3AF" },
});
