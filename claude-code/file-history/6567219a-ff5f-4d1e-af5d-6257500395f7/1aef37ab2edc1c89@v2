import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  Switch,
  Alert,
  Platform,
  KeyboardAvoidingView,
} from "react-native";
import { useEffect, useRef, useState } from "react";
import { useLocalSearchParams, useRouter } from "expo-router";
import * as Haptics from "expo-haptics";
import { api } from "@/lib/api";
import { GlassCard } from "@/components/GlassCard";

// ── Types ──────────────────────────────────────────────────────────────────
interface Activity {
  id: string;
  name: string;
  category: string;
  excitement: number | null;
}

interface Reflection {
  id: string;
  promptText: string;
  responseText: string | null;
  promptType: string;
  isSharedWithCounselor: boolean;
}

interface Session {
  id: string;
  monthKey: string;
  pulseScore: number | null;
  pulseNote: string | null;
  completedAt: string | null;
  activities: Activity[];
  reflections: Reflection[];
}

interface Prompt {
  promptText: string;
  promptType: string;
}

// ── Constants ──────────────────────────────────────────────────────────────
const STEPS = ["Pulse", "Activities", "Reflection", "Privacy", "Done"];

const ENERGY_LABELS: Record<number, string> = {
  1: "Really drained", 2: "Low energy", 3: "A bit tired", 4: "Okay",
  5: "Neutral", 6: "Decent", 7: "Pretty good", 8: "Good energy",
  9: "High energy", 10: "Thriving",
};

const EXCITEMENT_EMOJIS = ["", "😐", "🙂", "😊", "😄", "🤩"];

const CATEGORIES = [
  "ACADEMIC", "EXTRACURRICULAR", "READING", "PROJECT", "WORK", "VOLUNTEER", "HOBBY",
];

// ── Main Screen ────────────────────────────────────────────────────────────
export default function ReflectSessionScreen() {
  const { sessionId } = useLocalSearchParams<{ sessionId: string }>();
  const router = useRouter();

  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);
  const [step, setStep] = useState(0);

  // Pulse state
  const [pulseScore, setPulseScore] = useState(5);
  const [pulseNote, setPulseNote] = useState("");

  // Activities state
  const [activities, setActivities] = useState<Activity[]>([]);
  const [showAddActivity, setShowAddActivity] = useState(false);
  const [newActivityName, setNewActivityName] = useState("");
  const [newActivityCategory, setNewActivityCategory] = useState("HOBBY");
  const [newActivityExcitement, setNewActivityExcitement] = useState(3);
  const [savingActivity, setSavingActivity] = useState(false);

  // Reflection state
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [responses, setResponses] = useState<Record<number, string>>({});
  const [reflections, setReflections] = useState<Reflection[]>([]);
  const [loadingPrompts, setLoadingPrompts] = useState(false);
  const [savingReflection, setSavingReflection] = useState<number | null>(null);

  // Privacy state
  const [sharedReflections, setSharedReflections] = useState<Set<string>>(new Set());

  // Submitting
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    api
      .getSession(sessionId)
      .then((data) => {
        const s = data as Session;
        setSession(s);
        setPulseScore(s.pulseScore ?? 5);
        setPulseNote(s.pulseNote ?? "");
        setActivities(s.activities ?? []);
        setReflections(s.reflections ?? []);
        const prevResponses: Record<number, string> = {};
        (s.reflections ?? []).forEach((r, i) => {
          if (r.responseText) prevResponses[i] = r.responseText;
        });
        setResponses(prevResponses);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [sessionId]);

  // ── Step 0: Pulse Check ────────────────────────────────────────────────
  async function savePulseAndNext() {
    try {
      await api.updateSession(sessionId, { pulseScore, pulseNote: pulseNote || undefined });
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
      setStep(1);
    } catch (err) {
      console.error(err);
    }
  }

  // ── Step 1: Activities ─────────────────────────────────────────────────
  async function addActivity() {
    if (!newActivityName.trim()) return;
    setSavingActivity(true);
    try {
      const activity = await api.createActivity({
        sessionId,
        name: newActivityName,
        category: newActivityCategory,
        excitement: newActivityExcitement,
        isOngoing: true,
      }) as Activity;
      setActivities((prev) => [...prev, activity]);
      setNewActivityName("");
      setNewActivityExcitement(3);
      setNewActivityCategory("HOBBY");
      setShowAddActivity(false);
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    } catch (err) {
      console.error(err);
    } finally {
      setSavingActivity(false);
    }
  }

  async function goToReflection() {
    setStep(2);
    if (prompts.length === 0) {
      setLoadingPrompts(true);
      try {
        const data = await api.getReflectionPrompts(sessionId) as Prompt[];
        setPrompts(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoadingPrompts(false);
      }
    }
  }

  // ── Step 2: Reflections ────────────────────────────────────────────────
  const autoSaveTimers = useRef<Record<number, ReturnType<typeof setTimeout>>>({});

  function onResponseChange(idx: number, text: string) {
    setResponses((prev) => ({ ...prev, [idx]: text }));
    clearTimeout(autoSaveTimers.current[idx]);
    autoSaveTimers.current[idx] = setTimeout(() => {
      saveReflection(idx, text);
    }, 3000);
  }

  async function saveReflection(idx: number, text: string) {
    if (!text.trim()) return;
    const prompt = prompts[idx];
    if (!prompt) return;

    setSavingReflection(idx);
    try {
      if (reflections[idx]) {
        await api.updateReflection(reflections[idx].id, { responseText: text });
      } else {
        const r = await api.createReflection({
          sessionId,
          promptText: prompt.promptText,
          promptType: prompt.promptType,
          responseText: text,
        }) as Reflection;
        setReflections((prev) => {
          const next = [...prev];
          next[idx] = r;
          return next;
        });
      }
    } catch (err) {
      console.error(err);
    } finally {
      setSavingReflection(null);
    }
  }

  async function goToPrivacy() {
    // Save any unsaved reflections
    for (let i = 0; i < prompts.length; i++) {
      if (responses[i] && !reflections[i]) {
        await saveReflection(i, responses[i]);
      }
    }
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    setStep(3);
  }

  // ── Step 3: Privacy ────────────────────────────────────────────────────
  async function toggleReflectionSharing(reflectionId: string, shared: boolean) {
    await api.updateReflection(reflectionId, { isSharedWithCounselor: shared });
    setSharedReflections((prev) => {
      const next = new Set(prev);
      if (shared) next.add(reflectionId);
      else next.delete(reflectionId);
      return next;
    });
  }

  // ── Step 4: Submit ─────────────────────────────────────────────────────
  async function handleSubmit() {
    setSubmitting(true);
    try {
      await api.submitSession(sessionId);
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      setStep(4);
    } catch (err) {
      console.error(err);
      Alert.alert("Error", "Failed to submit. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading || !session) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator color="#3B82F6" />
      </View>
    );
  }

  return (
    <KeyboardAvoidingView
      style={styles.flex}
      behavior={Platform.OS === "ios" ? "padding" : "height"}
    >
      {/* Progress Bar */}
      <View style={styles.progressContainer}>
        {STEPS.map((_, i) => (
          <View
            key={i}
            style={[
              styles.progressSegment,
              i <= step && styles.progressSegmentActive,
            ]}
          />
        ))}
      </View>

      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
        keyboardShouldPersistTaps="handled"
      >
        {/* ── Step 0: Pulse ─────────────────────────────────────────────── */}
        {step === 0 && (
          <GlassCard style={styles.card}>
            <Text style={styles.stepTitle}>How's your energy?</Text>
            <Text style={styles.stepSubtitle}>
              Not a mood tracker — just context. No right answer.
            </Text>

            <View style={styles.sliderRow}>
              <Text style={styles.sliderLabel}>Low</Text>
              <Text style={styles.sliderValue}>{pulseScore}</Text>
              <Text style={styles.sliderLabel}>High</Text>
            </View>

            {/* Custom slider using buttons since RN slider requires package */}
            <View style={styles.sliderButtons}>
              {Array.from({ length: 10 }, (_, i) => i + 1).map((n) => (
                <TouchableOpacity
                  key={n}
                  style={[
                    styles.sliderButton,
                    pulseScore === n && styles.sliderButtonActive,
                  ]}
                  onPress={() => {
                    setPulseScore(n);
                    Haptics.selectionAsync();
                  }}
                >
                  <Text
                    style={[
                      styles.sliderButtonText,
                      pulseScore === n && styles.sliderButtonTextActive,
                    ]}
                  >
                    {n}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>

            <View style={styles.labelPill}>
              <Text style={styles.labelPillText}>
                {ENERGY_LABELS[pulseScore]}
              </Text>
            </View>

            <Text style={styles.fieldLabel}>What's on your mind? (optional)</Text>
            <TextInput
              value={pulseNote}
              onChangeText={setPulseNote}
              placeholder="Anything you want to set context with..."
              placeholderTextColor="#9CA3AF"
              multiline
              numberOfLines={3}
              style={styles.textarea}
            />

            <TouchableOpacity style={styles.primaryButton} onPress={savePulseAndNext}>
              <Text style={styles.primaryButtonText}>
                Continue to Activities →
              </Text>
            </TouchableOpacity>
          </GlassCard>
        )}

        {/* ── Step 1: Activities ─────────────────────────────────────────── */}
        {step === 1 && (
          <>
            <GlassCard style={styles.card}>
              <Text style={styles.stepTitle}>What have you been doing?</Text>
              <Text style={styles.stepSubtitle}>
                Add or update activities from this past month.
              </Text>

              {activities.map((a) => (
                <View key={a.id} style={styles.activityRow}>
                  <View style={styles.activityInfo}>
                    <Text style={styles.activityName}>{a.name}</Text>
                    <Text style={styles.activityCategory}>{a.category}</Text>
                  </View>
                  {a.excitement !== null && (
                    <Text style={styles.excitementEmoji}>
                      {EXCITEMENT_EMOJIS[a.excitement]}
                    </Text>
                  )}
                </View>
              ))}

              {showAddActivity ? (
                <View style={styles.addForm}>
                  <TextInput
                    value={newActivityName}
                    onChangeText={setNewActivityName}
                    placeholder="Activity name (e.g., Robotics club)"
                    placeholderTextColor="#9CA3AF"
                    style={styles.input}
                  />

                  <ScrollView
                    horizontal
                    showsHorizontalScrollIndicator={false}
                    style={styles.categoryScroll}
                  >
                    {CATEGORIES.map((cat) => (
                      <TouchableOpacity
                        key={cat}
                        style={[
                          styles.categoryChip,
                          newActivityCategory === cat && styles.categoryChipActive,
                        ]}
                        onPress={() => setNewActivityCategory(cat)}
                      >
                        <Text
                          style={[
                            styles.categoryChipText,
                            newActivityCategory === cat && styles.categoryChipTextActive,
                          ]}
                        >
                          {cat}
                        </Text>
                      </TouchableOpacity>
                    ))}
                  </ScrollView>

                  <View style={styles.excitementRow}>
                    <Text style={styles.fieldLabel}>Excitement:</Text>
                    <View style={styles.excitementButtons}>
                      {[1, 2, 3, 4, 5].map((n) => (
                        <TouchableOpacity
                          key={n}
                          onPress={() => {
                            setNewActivityExcitement(n);
                            Haptics.selectionAsync();
                          }}
                        >
                          <Text
                            style={[
                              styles.excitementOption,
                              newActivityExcitement !== n && styles.excitementDim,
                            ]}
                          >
                            {EXCITEMENT_EMOJIS[n]}
                          </Text>
                        </TouchableOpacity>
                      ))}
                    </View>
                  </View>

                  <View style={styles.addFormButtons}>
                    <TouchableOpacity
                      style={styles.ghostButton}
                      onPress={() => setShowAddActivity(false)}
                    >
                      <Text style={styles.ghostButtonText}>Cancel</Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                      style={[
                        styles.primaryButton,
                        styles.flex,
                        (!newActivityName.trim() || savingActivity) &&
                          styles.disabledButton,
                      ]}
                      onPress={addActivity}
                      disabled={!newActivityName.trim() || savingActivity}
                    >
                      {savingActivity ? (
                        <ActivityIndicator color="white" size="small" />
                      ) : (
                        <Text style={styles.primaryButtonText}>Add</Text>
                      )}
                    </TouchableOpacity>
                  </View>
                </View>
              ) : (
                <TouchableOpacity
                  style={styles.dashedButton}
                  onPress={() => setShowAddActivity(true)}
                >
                  <Text style={styles.dashedButtonText}>+ Add Activity</Text>
                </TouchableOpacity>
              )}
            </GlassCard>

            <View style={styles.navRow}>
              <TouchableOpacity
                style={styles.ghostButton}
                onPress={() => setStep(0)}
              >
                <Text style={styles.ghostButtonText}>Back</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.primaryButton, styles.flex]}
                onPress={goToReflection}
              >
                <Text style={styles.primaryButtonText}>
                  Continue to Reflection →
                </Text>
              </TouchableOpacity>
            </View>
          </>
        )}

        {/* ── Step 2: Reflection Prompts ──────────────────────────────────── */}
        {step === 2 && (
          <>
            {loadingPrompts ? (
              <GlassCard style={[styles.card, styles.centered]}>
                <ActivityIndicator color="#3B82F6" />
                <Text style={styles.loadingText}>
                  Generating your reflection prompts...
                </Text>
              </GlassCard>
            ) : (
              prompts.map((prompt, i) => (
                <GlassCard key={i} style={styles.card}>
                  <Text style={styles.promptLabel}>
                    {prompt.promptType.charAt(0) + prompt.promptType.slice(1).toLowerCase()} prompt
                  </Text>
                  <Text style={styles.promptText}>{prompt.promptText}</Text>
                  <TextInput
                    value={responses[i] ?? ""}
                    onChangeText={(t) => onResponseChange(i, t)}
                    placeholder="Your thoughts..."
                    placeholderTextColor="#9CA3AF"
                    multiline
                    numberOfLines={4}
                    style={styles.textarea}
                  />
                  <View style={styles.savingRow}>
                    <Text style={styles.wordCount}>
                      {(responses[i] ?? "").trim().split(/\s+/).filter(Boolean).length} words
                    </Text>
                    {savingReflection === i && (
                      <Text style={styles.savingText}>Saving...</Text>
                    )}
                  </View>
                </GlassCard>
              ))
            )}

            {!loadingPrompts && (
              <View style={styles.navRow}>
                <TouchableOpacity
                  style={styles.ghostButton}
                  onPress={() => setStep(1)}
                >
                  <Text style={styles.ghostButtonText}>Back</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[styles.primaryButton, styles.flex]}
                  onPress={goToPrivacy}
                >
                  <Text style={styles.primaryButtonText}>
                    Review Privacy →
                  </Text>
                </TouchableOpacity>
              </View>
            )}
          </>
        )}

        {/* ── Step 3: Privacy Review ─────────────────────────────────────── */}
        {step === 3 && (
          <>
            <GlassCard style={styles.card}>
              <Text style={styles.stepTitle}>Privacy Review</Text>
              <Text style={styles.stepSubtitle}>
                Choose which reflections to share with your counselor. Everything
                is private by default.
              </Text>

              {reflections.filter((r) => !!r).map((reflection) => (
                <View key={reflection.id} style={styles.reflectionShareRow}>
                  <View style={styles.reflectionShareText}>
                    <Text style={styles.promptLabel}>{reflection.promptType}</Text>
                    <Text style={styles.reflectionPreview} numberOfLines={2}>
                      {reflection.responseText ?? "(no response)"}
                    </Text>
                  </View>
                  <Switch
                    value={sharedReflections.has(reflection.id)}
                    onValueChange={(v) =>
                      toggleReflectionSharing(reflection.id, v)
                    }
                    trackColor={{ false: "#D1D5DB", true: "#93C5FD" }}
                    thumbColor={
                      sharedReflections.has(reflection.id) ? "#3B82F6" : "#F9FAFB"
                    }
                  />
                </View>
              ))}

              {reflections.filter((r) => !!r).length === 0 && (
                <Text style={styles.emptyText}>No responses yet to share.</Text>
              )}
            </GlassCard>

            <View style={styles.navRow}>
              <TouchableOpacity
                style={styles.ghostButton}
                onPress={() => setStep(2)}
              >
                <Text style={styles.ghostButtonText}>Back</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[
                  styles.primaryButton,
                  styles.flex,
                  submitting && styles.disabledButton,
                ]}
                onPress={handleSubmit}
                disabled={submitting}
              >
                {submitting ? (
                  <ActivityIndicator color="white" size="small" />
                ) : (
                  <Text style={styles.primaryButtonText}>
                    Submit Reflection ✓
                  </Text>
                )}
              </TouchableOpacity>
            </View>
          </>
        )}

        {/* ── Step 4: Complete ───────────────────────────────────────────── */}
        {step === 4 && (
          <GlassCard style={[styles.card, styles.completedCard]}>
            <Text style={styles.completedEmoji}>🎯</Text>
            <Text style={styles.completedTitle}>Reflection complete!</Text>
            <Text style={styles.completedSubtitle}>
              Your signal profile is being updated. Check back tomorrow to see
              your updated insights.
            </Text>
            <TouchableOpacity
              style={styles.primaryButton}
              onPress={() => router.replace("/(tabs)")}
            >
              <Text style={styles.primaryButtonText}>Back to Home</Text>
            </TouchableOpacity>
          </GlassCard>
        )}
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  container: { flex: 1, backgroundColor: "#F2F4F7" },
  content: { padding: 20, paddingBottom: 40, gap: 12 },
  centered: { alignItems: "center", justifyContent: "center", padding: 40 },
  progressContainer: {
    flexDirection: "row",
    gap: 6,
    paddingHorizontal: 20,
    paddingTop: Platform.OS === "ios" ? 56 : 16,
    paddingBottom: 8,
    backgroundColor: "#F2F4F7",
  },
  progressSegment: {
    flex: 1,
    height: 4,
    borderRadius: 2,
    backgroundColor: "#E5E7EB",
  },
  progressSegmentActive: { backgroundColor: "#3B82F6" },
  card: { gap: 10 },
  stepTitle: { fontSize: 18, fontWeight: "700", color: "#1A1A2E" },
  stepSubtitle: { fontSize: 13, color: "#6B7280", lineHeight: 18 },
  sliderRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  sliderLabel: { fontSize: 12, color: "#9CA3AF" },
  sliderValue: { fontSize: 32, fontWeight: "700", color: "#1A1A2E" },
  sliderButtons: { flexDirection: "row", gap: 4 },
  sliderButton: {
    flex: 1,
    aspectRatio: 1,
    borderRadius: 8,
    backgroundColor: "rgba(255,255,255,0.6)",
    borderWidth: 1,
    borderColor: "#E5E7EB",
    alignItems: "center",
    justifyContent: "center",
  },
  sliderButtonActive: {
    backgroundColor: "#3B82F6",
    borderColor: "#3B82F6",
  },
  sliderButtonText: { fontSize: 12, color: "#6B7280" },
  sliderButtonTextActive: { color: "white", fontWeight: "700" },
  labelPill: {
    alignSelf: "center",
    backgroundColor: "#EFF6FF",
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 6,
  },
  labelPillText: { fontSize: 13, fontWeight: "500", color: "#3B82F6" },
  fieldLabel: { fontSize: 12, color: "#6B7280", marginBottom: 4 },
  textarea: {
    backgroundColor: "rgba(255,255,255,0.6)",
    borderWidth: 1,
    borderColor: "rgba(229,231,235,0.8)",
    borderRadius: 12,
    padding: 12,
    fontSize: 14,
    color: "#1A1A2E",
    minHeight: 80,
    textAlignVertical: "top",
  },
  input: {
    backgroundColor: "rgba(255,255,255,0.8)",
    borderWidth: 1,
    borderColor: "#E5E7EB",
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 14,
    color: "#1A1A2E",
  },
  primaryButton: {
    backgroundColor: "#3B82F6",
    borderRadius: 12,
    paddingVertical: 14,
    paddingHorizontal: 20,
    alignItems: "center",
  },
  primaryButtonText: { color: "white", fontSize: 14, fontWeight: "600" },
  disabledButton: { opacity: 0.5 },
  ghostButton: {
    borderRadius: 12,
    paddingVertical: 14,
    paddingHorizontal: 16,
    alignItems: "center",
    backgroundColor: "transparent",
    borderWidth: 1,
    borderColor: "rgba(107,114,128,0.3)",
  },
  ghostButtonText: { color: "#6B7280", fontSize: 14, fontWeight: "500" },
  dashedButton: {
    borderWidth: 2,
    borderStyle: "dashed",
    borderColor: "rgba(209,213,219,0.8)",
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: "center",
    marginTop: 4,
  },
  dashedButtonText: { color: "#6B7280", fontSize: 13 },
  navRow: { flexDirection: "row", gap: 10 },
  activityRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingVertical: 10,
    paddingHorizontal: 12,
    backgroundColor: "rgba(255,255,255,0.5)",
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "rgba(229,231,235,0.4)",
  },
  activityInfo: { flex: 1 },
  activityName: { fontSize: 13, fontWeight: "500", color: "#1A1A2E" },
  activityCategory: { fontSize: 11, color: "#9CA3AF", marginTop: 1 },
  excitementEmoji: { fontSize: 18 },
  addForm: { gap: 10, marginTop: 4 },
  categoryScroll: { marginVertical: 4 },
  categoryChip: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    backgroundColor: "rgba(255,255,255,0.6)",
    borderWidth: 1,
    borderColor: "#E5E7EB",
    marginRight: 6,
  },
  categoryChipActive: {
    backgroundColor: "#EFF6FF",
    borderColor: "#93C5FD",
  },
  categoryChipText: { fontSize: 12, color: "#6B7280" },
  categoryChipTextActive: { color: "#3B82F6", fontWeight: "600" },
  excitementRow: { flexDirection: "row", alignItems: "center", gap: 12 },
  excitementButtons: { flexDirection: "row", gap: 8 },
  excitementOption: { fontSize: 24 },
  excitementDim: { opacity: 0.3 },
  addFormButtons: { flexDirection: "row", gap: 8 },
  promptLabel: {
    fontSize: 11,
    fontWeight: "600",
    color: "#6B7280",
    textTransform: "uppercase",
    letterSpacing: 0.5,
  },
  promptText: {
    fontSize: 15,
    fontWeight: "600",
    color: "#1A1A2E",
    lineHeight: 22,
  },
  savingRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  wordCount: { fontSize: 11, color: "#9CA3AF" },
  savingText: { fontSize: 11, color: "#3B82F6" },
  loadingText: { marginTop: 12, fontSize: 13, color: "#6B7280" },
  reflectionShareRow: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(229,231,235,0.3)",
    gap: 12,
  },
  reflectionShareText: { flex: 1 },
  reflectionPreview: { fontSize: 12, color: "#6B7280", marginTop: 2 },
  emptyText: { fontSize: 13, color: "#9CA3AF", textAlign: "center", padding: 12 },
  completedCard: { alignItems: "center", paddingVertical: 32 },
  completedEmoji: { fontSize: 52 },
  completedTitle: {
    fontSize: 22,
    fontWeight: "700",
    color: "#1A1A2E",
    marginTop: 12,
  },
  completedSubtitle: {
    fontSize: 13,
    color: "#6B7280",
    textAlign: "center",
    lineHeight: 19,
    marginVertical: 12,
  },
});
