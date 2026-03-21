import { View, Text, ScrollView, StyleSheet, TouchableOpacity, ActivityIndicator } from "react-native";
import { useEffect, useState } from "react";
import { Link } from "expo-router";
import { useUser } from "@clerk/clerk-expo";
import { api } from "@/lib/api";
import { GlassCard } from "@/components/GlassCard";
import { SignalBadge } from "@/components/SignalBadge";
import { NotificationCard } from "@/components/NotificationCard";

interface InterestCluster {
  id: string;
  label: string;
  strength: "strong" | "moderate" | "emerging";
  trend: "rising" | "stable" | "declining";
}

interface SignalProfile {
  breadthScore: number;
  interestClusters: InterestCluster[];
  compressedSummary: string | null;
}

interface Notification {
  id: string;
  type: string;
  title: string;
  body: string;
  readAt: string | null;
  createdAt: string;
}

interface Session {
  id: string;
  monthKey: string;
  completedAt: string | null;
}

export default function HomeScreen() {
  const { user } = useUser();
  const [signalProfile, setSignalProfile] = useState<SignalProfile | null>(null);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [currentSession, setCurrentSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [profileRes, notifRes, sessionsRes] = await Promise.allSettled([
          api.getSignalProfile(),
          api.getNotifications(1),
          api.getSessions(),
        ]);

        if (profileRes.status === "fulfilled") {
          setSignalProfile(profileRes.value as SignalProfile);
        }
        if (notifRes.status === "fulfilled") {
          const data = notifRes.value as { notifications: Notification[] };
          setNotifications(data.notifications?.slice(0, 2) ?? []);
        }
        if (sessionsRes.status === "fulfilled") {
          const sessions = sessionsRes.value as Session[];
          const now = new Date();
          const monthKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`;
          const current = sessions.find((s) => s.monthKey === monthKey) ?? null;
          setCurrentSession(current);
        }
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const firstName = user?.firstName ?? "there";
  const now = new Date();
  const monthKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`;
  const hasCurrentSession = currentSession?.monthKey === monthKey;
  const sessionComplete = hasCurrentSession && !!currentSession?.completedAt;

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      showsVerticalScrollIndicator={false}
    >
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.greeting}>Hey, {firstName} 👋</Text>
        <Text style={styles.subtitle}>
          {signalProfile
            ? "Here's what COMPASS sees in you"
            : "Start reflecting to see your signals"}
        </Text>
      </View>

      {/* Session CTA */}
      <GlassCard style={styles.sessionCard}>
        {sessionComplete ? (
          <View style={styles.sessionRow}>
            <View>
              <Text style={styles.sessionTitle}>This month is done ✓</Text>
              <Text style={styles.sessionSub}>Next reflection opens in ~30 days</Text>
            </View>
          </View>
        ) : hasCurrentSession ? (
          <View style={styles.sessionRow}>
            <View style={{ flex: 1 }}>
              <Text style={styles.sessionTitle}>Reflection in progress</Text>
              <Text style={styles.sessionSub}>Pick up where you left off</Text>
            </View>
            <Link href={`/reflect/${currentSession!.id}`} asChild>
              <TouchableOpacity style={styles.ctaButton}>
                <Text style={styles.ctaText}>Continue</Text>
              </TouchableOpacity>
            </Link>
          </View>
        ) : (
          <View style={styles.sessionRow}>
            <View style={{ flex: 1 }}>
              <Text style={styles.sessionTitle}>Monthly Reflection</Text>
              <Text style={styles.sessionSub}>10–15 minutes</Text>
            </View>
            <Link href="/reflect/new" asChild>
              <TouchableOpacity style={styles.ctaButton}>
                <Text style={styles.ctaText}>Start</Text>
              </TouchableOpacity>
            </Link>
          </View>
        )}
      </GlassCard>

      {loading && <ActivityIndicator color="#3B82F6" style={{ marginTop: 20 }} />}

      {/* Signal Profile */}
      {signalProfile && !loading && (
        <GlassCard style={styles.card}>
          <Text style={styles.cardTitle}>Interest Signals</Text>
          <View style={styles.badges}>
            {(signalProfile.interestClusters ?? []).slice(0, 4).map((c) => (
              <SignalBadge key={c.id} label={c.label} strength={c.strength} />
            ))}
          </View>
        </GlassCard>
      )}

      {/* Breadth Score */}
      {signalProfile && !loading && (
        <GlassCard style={styles.card}>
          <View style={styles.breadthRow}>
            <Text style={styles.cardTitle}>Exploration Breadth</Text>
            <Text style={styles.breadthScore}>
              {Math.round(signalProfile.breadthScore)}/100
            </Text>
          </View>
          <View style={styles.progressTrack}>
            <View
              style={[
                styles.progressFill,
                { width: `${signalProfile.breadthScore}%` as `${number}%` },
              ]}
            />
          </View>
        </GlassCard>
      )}

      {/* Map CTA */}
      <Link href="/tabs/map" asChild>
        <TouchableOpacity activeOpacity={0.8}>
          <GlassCard style={[styles.card, styles.mapCard]}>
            <View style={styles.mapRow}>
              <View>
                <Text style={styles.mapTitle}>Explore the Career Map</Text>
                <Text style={styles.mapSub}>Discover paths that match you</Text>
              </View>
              <Text style={styles.mapArrow}>→</Text>
            </View>
          </GlassCard>
        </TouchableOpacity>
      </Link>

      {/* Notifications */}
      {notifications.length > 0 && !loading && (
        <View>
          <Text style={styles.sectionLabel}>New for you</Text>
          {notifications.map((n) => (
            <NotificationCard
              key={n.id}
              notification={n}
              onPress={() => api.markRead(n.id)}
            />
          ))}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F2F4F7" },
  content: { padding: 20, paddingBottom: 40, gap: 14 },
  header: { paddingTop: 16, gap: 4, marginBottom: 4 },
  greeting: { fontSize: 24, fontWeight: "700", color: "#1A1A2E" },
  subtitle: { fontSize: 14, color: "#6B7280" },
  sessionCard: { marginBottom: 4 },
  sessionRow: { flexDirection: "row", alignItems: "center", justifyContent: "space-between" },
  sessionTitle: { fontSize: 14, fontWeight: "600", color: "#1A1A2E" },
  sessionSub: { fontSize: 12, color: "#6B7280", marginTop: 2 },
  ctaButton: { backgroundColor: "#3B82F6", borderRadius: 10, paddingHorizontal: 16, paddingVertical: 8 },
  ctaText: { color: "white", fontSize: 13, fontWeight: "600" },
  card: { gap: 10 },
  cardTitle: { fontSize: 14, fontWeight: "600", color: "#1A1A2E" },
  badges: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  breadthRow: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  breadthScore: { fontSize: 14, fontWeight: "700", color: "#3B82F6" },
  progressTrack: { height: 6, backgroundColor: "rgba(229,231,235,0.8)", borderRadius: 3, overflow: "hidden" },
  progressFill: { height: 6, backgroundColor: "#3B82F6", borderRadius: 3 },
  mapCard: { backgroundColor: "rgba(239,246,255,0.8)", borderColor: "rgba(191,219,254,0.4)" },
  mapRow: { flexDirection: "row", alignItems: "center", justifyContent: "space-between" },
  mapTitle: { fontSize: 14, fontWeight: "600", color: "#1A1A2E" },
  mapSub: { fontSize: 12, color: "#6B7280", marginTop: 2 },
  mapArrow: { fontSize: 18, color: "#3B82F6" },
  sectionLabel: { fontSize: 12, fontWeight: "600", color: "#6B7280", marginBottom: 6, textTransform: "uppercase", letterSpacing: 0.5 },
});
