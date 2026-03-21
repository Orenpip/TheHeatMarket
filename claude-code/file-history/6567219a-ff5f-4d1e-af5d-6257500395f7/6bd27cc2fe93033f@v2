import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  Platform,
} from "react-native";
import { useEffect, useState } from "react";
import { Link, useRouter } from "expo-router";
import { api } from "@/lib/api";
import { GlassCard } from "@/components/GlassCard";

interface Session {
  id: string;
  monthKey: string;
  completedAt: string | null;
  durationSeconds: number | null;
  activities: Array<{ id: string; name: string }>;
  reflections: Array<{ id: string; promptType: string }>;
}

const MONTH_NAMES = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
];

function formatMonthKey(key: string): string {
  const [year, month] = key.split("-");
  if (!year || !month) return key;
  return `${MONTH_NAMES[parseInt(month) - 1]} ${year}`;
}

export default function ReflectionsScreen() {
  const router = useRouter();
  const [sessions, setSessions] = useState<Session[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getSessions()
      .then((data) => setSessions(data as Session[]))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const now = new Date();
  const currentMonthKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`;
  const currentSession = sessions.find((s) => s.monthKey === currentMonthKey);
  const hasCurrentSession = !!currentSession;
  const sessionComplete = hasCurrentSession && !!currentSession?.completedAt;

  async function startNewSession() {
    try {
      const session = await api.createSession(currentMonthKey);
      router.push(`/reflect/${(session as { id: string }).id}`);
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      showsVerticalScrollIndicator={false}
    >
      <View style={styles.header}>
        <Text style={styles.title}>Reflections</Text>
        {!loading && (
          <Text style={styles.subtitle}>
            {sessions.length} session{sessions.length !== 1 ? "s" : ""}
          </Text>
        )}
      </View>

      {/* Start / Continue CTA */}
      {!loading && (
        <GlassCard style={styles.ctaCard}>
          {sessionComplete ? (
            <Text style={styles.doneText}>
              ✓ {formatMonthKey(currentMonthKey)} complete
            </Text>
          ) : hasCurrentSession ? (
            <Link href={`/reflect/${currentSession!.id}`} asChild>
              <TouchableOpacity style={styles.ctaButton}>
                <Text style={styles.ctaButtonText}>
                  Continue {formatMonthKey(currentMonthKey)} Reflection →
                </Text>
              </TouchableOpacity>
            </Link>
          ) : (
            <TouchableOpacity style={styles.ctaButton} onPress={startNewSession}>
              <Text style={styles.ctaButtonText}>
                Start {formatMonthKey(currentMonthKey)} Reflection →
              </Text>
            </TouchableOpacity>
          )}
        </GlassCard>
      )}

      {loading && <ActivityIndicator color="#3B82F6" style={{ marginTop: 20 }} />}

      {/* Past Sessions */}
      {!loading && sessions.length === 0 && (
        <View style={styles.empty}>
          <Text style={styles.emptyIcon}>📓</Text>
          <Text style={styles.emptyTitle}>No reflections yet</Text>
          <Text style={styles.emptyText}>
            Start your first reflection above to begin building your signal profile.
          </Text>
        </View>
      )}

      {!loading &&
        sessions
          .filter((s) => s.monthKey !== currentMonthKey || sessionComplete)
          .map((session) => (
            <GlassCard key={session.id} style={styles.sessionCard}>
              <View style={styles.sessionHeader}>
                <Text style={styles.sessionMonth}>
                  {formatMonthKey(session.monthKey)}
                </Text>
                {session.completedAt ? (
                  <Text style={styles.completedBadge}>✓ Complete</Text>
                ) : (
                  <Link href={`/reflect/${session.id}`} asChild>
                    <TouchableOpacity>
                      <Text style={styles.continueBadge}>In Progress →</Text>
                    </TouchableOpacity>
                  </Link>
                )}
              </View>

              <View style={styles.sessionMeta}>
                <Text style={styles.metaText}>
                  {session.activities?.length ?? 0} activities
                </Text>
                <Text style={styles.metaDot}>·</Text>
                <Text style={styles.metaText}>
                  {session.reflections?.length ?? 0} reflections
                </Text>
                {session.durationSeconds && (
                  <>
                    <Text style={styles.metaDot}>·</Text>
                    <Text style={styles.metaText}>
                      {Math.round(session.durationSeconds / 60)} min
                    </Text>
                  </>
                )}
              </View>

              {session.activities?.length > 0 && (
                <View style={styles.activityTags}>
                  {session.activities.slice(0, 3).map((a) => (
                    <View key={a.id} style={styles.tag}>
                      <Text style={styles.tagText}>{a.name}</Text>
                    </View>
                  ))}
                  {session.activities.length > 3 && (
                    <Text style={styles.tagMore}>
                      +{session.activities.length - 3}
                    </Text>
                  )}
                </View>
              )}
            </GlassCard>
          ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F2F4F7" },
  content: { padding: 20, paddingBottom: 40, gap: 12 },
  header: {
    paddingTop: Platform.OS === "ios" ? 16 : 8,
    gap: 2,
    marginBottom: 4,
  },
  title: { fontSize: 24, fontWeight: "700", color: "#1A1A2E" },
  subtitle: { fontSize: 13, color: "#6B7280" },
  ctaCard: {},
  ctaButton: {
    backgroundColor: "#3B82F6",
    borderRadius: 12,
    padding: 14,
    alignItems: "center",
  },
  ctaButtonText: { color: "white", fontSize: 14, fontWeight: "600" },
  doneText: { fontSize: 14, color: "#10B981", fontWeight: "600", textAlign: "center" },
  empty: { alignItems: "center", paddingVertical: 40, gap: 8 },
  emptyIcon: { fontSize: 40 },
  emptyTitle: { fontSize: 16, fontWeight: "600", color: "#1A1A2E" },
  emptyText: { fontSize: 13, color: "#6B7280", textAlign: "center", lineHeight: 19 },
  sessionCard: { gap: 8 },
  sessionHeader: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  sessionMonth: { fontSize: 14, fontWeight: "600", color: "#1A1A2E" },
  completedBadge: { fontSize: 12, color: "#10B981", fontWeight: "500" },
  continueBadge: { fontSize: 12, color: "#F59E0B", fontWeight: "500" },
  sessionMeta: { flexDirection: "row", alignItems: "center", gap: 6 },
  metaText: { fontSize: 12, color: "#9CA3AF" },
  metaDot: { fontSize: 12, color: "#D1D5DB" },
  activityTags: { flexDirection: "row", flexWrap: "wrap", gap: 6 },
  tag: {
    backgroundColor: "rgba(239,246,255,0.8)",
    borderRadius: 20,
    paddingHorizontal: 10,
    paddingVertical: 3,
    borderWidth: 1,
    borderColor: "#BFDBFE",
  },
  tagText: { fontSize: 11, color: "#1D4ED8" },
  tagMore: { fontSize: 11, color: "#9CA3AF", alignSelf: "center" },
});
