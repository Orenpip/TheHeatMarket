import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  Platform,
  KeyboardAvoidingView,
} from "react-native";
import { useState } from "react";
import { useRouter } from "expo-router";
import * as Haptics from "expo-haptics";
import { api } from "@/lib/api";
import { GlassCard } from "@/components/GlassCard";

const CATEGORIES = [
  { value: "ACADEMIC", label: "Academics", emoji: "📚" },
  { value: "EXTRACURRICULAR", label: "Extracurriculars", emoji: "🏃" },
  { value: "READING", label: "Reading", emoji: "📖" },
  { value: "PROJECT", label: "Personal Projects", emoji: "🛠️" },
  { value: "WORK", label: "Work / Internship", emoji: "💼" },
  { value: "VOLUNTEER", label: "Volunteering", emoji: "🤝" },
  { value: "HOBBY", label: "Hobbies", emoji: "🎨" },
];

interface Activity {
  name: string;
  category: string;
  excitement: number;
}

export default function OnboardingScreen() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [gradeLevel, setGradeLevel] = useState(10);

  const [activities, setActivities] = useState<Activity[]>([]);
  const [newName, setNewName] = useState("");
  const [newCategory, setNewCategory] = useState("HOBBY");
  const [newExcitement, setNewExcitement] = useState(3);

  const [submitting, setSubmitting] = useState(false);

  function addActivity() {
    if (!newName.trim()) return;
    setActivities((prev) => [
      ...prev,
      { name: newName.trim(), category: newCategory, excitement: newExcitement },
    ]);
    setNewName("");
    setNewExcitement(3);
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
  }

  function removeActivity(idx: number) {
    setActivities((prev) => prev.filter((_, i) => i !== idx));
  }

  async function handleSubmit() {
    setSubmitting(true);
    try {
      await api.completeOnboarding({ gradeLevel, initialActivities: activities });
      router.replace("/(tabs)");
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  }

  const excitementEmojis = ["", "😐", "🙂", "😊", "😄", "🤩"];

  return (
    <KeyboardAvoidingView
      style={styles.flex}
      behavior={Platform.OS === "ios" ? "padding" : "height"}
    >
      {/* Progress dots */}
      <View style={styles.progressContainer}>
        {[1, 2, 3].map((n) => (
          <View
            key={n}
            style={[
              styles.progressDot,
              n === step
                ? styles.progressDotActive
                : n < step
                ? styles.progressDotDone
                : styles.progressDotInactive,
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
        {/* ── Step 1: Welcome + Grade ───────────────────────────────────── */}
        {step === 1 && (
          <GlassCard style={styles.card}>
            <Text style={styles.bigEmoji}>🧭</Text>
            <Text style={styles.title}>Welcome to COMPASS</Text>
            <Text style={styles.subtitle}>
              I&apos;m here to help you see patterns in your interests and
              explore what&apos;s possible — not tell you what to do.
            </Text>

            <Text style={styles.fieldLabel}>What grade are you in?</Text>
            <View style={styles.gradeRow}>
              {[9, 10, 11, 12].map((grade) => (
                <TouchableOpacity
                  key={grade}
                  style={[
                    styles.gradeButton,
                    gradeLevel === grade && styles.gradeButtonActive,
                  ]}
                  onPress={() => {
                    setGradeLevel(grade);
                    Haptics.selectionAsync();
                  }}
                >
                  <Text
                    style={[
                      styles.gradeButtonText,
                      gradeLevel === grade && styles.gradeButtonTextActive,
                    ]}
                  >
                    {grade}th
                  </Text>
                </TouchableOpacity>
              ))}
            </View>

            <TouchableOpacity
              style={styles.primaryButton}
              onPress={() => {
                Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
                setStep(2);
              }}
            >
              <Text style={styles.primaryButtonText}>Next →</Text>
            </TouchableOpacity>
          </GlassCard>
        )}

        {/* ── Step 2: Activities ────────────────────────────────────────── */}
        {step === 2 && (
          <GlassCard style={styles.card}>
            <Text style={styles.title}>What are you into?</Text>
            <Text style={styles.subtitle}>
              Add 2–5 things you&apos;ve been doing lately — school, hobbies,
              projects, anything. Be honest, not impressive.
            </Text>

            {/* Added activities */}
            {activities.map((a, i) => (
              <View key={i} style={styles.activityRow}>
                <View style={styles.activityInfo}>
                  <Text style={styles.activityName}>{a.name}</Text>
                  <Text style={styles.activityCategory}>{a.category}</Text>
                </View>
                <Text style={styles.excitementEmoji}>
                  {excitementEmojis[a.excitement]}
                </Text>
                <TouchableOpacity
                  onPress={() => removeActivity(i)}
                  style={styles.removeButton}
                >
                  <Text style={styles.removeButtonText}>✕</Text>
                </TouchableOpacity>
              </View>
            ))}

            {/* Add form */}
            <View style={styles.addForm}>
              <TextInput
                value={newName}
                onChangeText={setNewName}
                placeholder="Activity name (e.g., Robotics club)"
                placeholderTextColor="#9CA3AF"
                style={styles.input}
                returnKeyType="done"
                onSubmitEditing={addActivity}
              />

              <ScrollView
                horizontal
                showsHorizontalScrollIndicator={false}
                style={styles.categoryScroll}
              >
                {CATEGORIES.map((c) => (
                  <TouchableOpacity
                    key={c.value}
                    style={[
                      styles.categoryChip,
                      newCategory === c.value && styles.categoryChipActive,
                    ]}
                    onPress={() => setNewCategory(c.value)}
                  >
                    <Text style={styles.categoryChipEmoji}>{c.emoji}</Text>
                    <Text
                      style={[
                        styles.categoryChipText,
                        newCategory === c.value && styles.categoryChipTextActive,
                      ]}
                    >
                      {c.label}
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
                        setNewExcitement(n);
                        Haptics.selectionAsync();
                      }}
                    >
                      <Text
                        style={[
                          styles.excitementOption,
                          newExcitement !== n && styles.excitementDim,
                        ]}
                      >
                        {excitementEmojis[n]}
                      </Text>
                    </TouchableOpacity>
                  ))}
                </View>
              </View>

              <TouchableOpacity
                style={[
                  styles.dashedButton,
                  !newName.trim() && styles.dashedButtonDisabled,
                ]}
                onPress={addActivity}
                disabled={!newName.trim()}
              >
                <Text style={styles.dashedButtonText}>+ Add</Text>
              </TouchableOpacity>
            </View>

            <View style={styles.navRow}>
              <TouchableOpacity
                style={styles.ghostButton}
                onPress={() => setStep(1)}
              >
                <Text style={styles.ghostButtonText}>Back</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[
                  styles.primaryButton,
                  styles.flex,
                  activities.length === 0 && styles.disabledButton,
                ]}
                disabled={activities.length === 0}
                onPress={() => {
                  Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
                  setStep(3);
                }}
              >
                <Text style={styles.primaryButtonText}>Next →</Text>
              </TouchableOpacity>
            </View>
          </GlassCard>
        )}

        {/* ── Step 3: Confirm ───────────────────────────────────────────── */}
        {step === 3 && (
          <GlassCard style={[styles.card, styles.centered]}>
            <Text style={styles.bigEmoji}>🎯</Text>
            <Text style={styles.title}>You&apos;re all set!</Text>
            <Text style={styles.subtitle}>
              COMPASS will learn about your interests as you complete monthly
              reflections. No judgment, no pressure.
            </Text>

            <View style={styles.howItWorks}>
              <Text style={styles.howItWorksTitle}>Here&apos;s how it works:</Text>
              {[
                { icon: "📓", text: "Monthly 10-min reflections on your activities" },
                { icon: "🧭", text: "AI builds a signal profile from your patterns" },
                { icon: "🗺️", text: "Explore careers and paths that match your interests" },
                { icon: "🔒", text: "You control exactly what your counselor sees" },
              ].map(({ icon, text }) => (
                <View key={text} style={styles.howItWorksRow}>
                  <Text style={styles.howItWorksIcon}>{icon}</Text>
                  <Text style={styles.howItWorksText}>{text}</Text>
                </View>
              ))}
            </View>

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
                  <Text style={styles.primaryButtonText}>Start Exploring →</Text>
                )}
              </TouchableOpacity>
            </View>
          </GlassCard>
        )}
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  container: { flex: 1, backgroundColor: "#F2F4F7" },
  content: {
    padding: 20,
    paddingBottom: 60,
    gap: 16,
    flexGrow: 1,
    justifyContent: "center",
  },
  centered: { alignItems: "center" },
  progressContainer: {
    flexDirection: "row",
    justifyContent: "center",
    gap: 8,
    paddingTop: Platform.OS === "ios" ? 60 : 24,
    paddingBottom: 16,
    backgroundColor: "#F2F4F7",
  },
  progressDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  progressDotActive: { backgroundColor: "#3B82F6", width: 24 },
  progressDotDone: { backgroundColor: "#93C5FD" },
  progressDotInactive: { backgroundColor: "#D1D5DB" },
  card: { gap: 14 },
  bigEmoji: { fontSize: 52, textAlign: "center" },
  title: {
    fontSize: 22,
    fontWeight: "700",
    color: "#1A1A2E",
    textAlign: "center",
  },
  subtitle: {
    fontSize: 13,
    color: "#6B7280",
    textAlign: "center",
    lineHeight: 19,
  },
  fieldLabel: { fontSize: 13, fontWeight: "500", color: "#1A1A2E" },
  gradeRow: { flexDirection: "row", gap: 8 },
  gradeButton: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 12,
    backgroundColor: "rgba(255,255,255,0.6)",
    borderWidth: 1,
    borderColor: "#E5E7EB",
    alignItems: "center",
  },
  gradeButtonActive: {
    backgroundColor: "#3B82F6",
    borderColor: "#3B82F6",
  },
  gradeButtonText: { fontSize: 14, fontWeight: "600", color: "#6B7280" },
  gradeButtonTextActive: { color: "white" },
  primaryButton: {
    backgroundColor: "#3B82F6",
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: "center",
  },
  primaryButtonText: { color: "white", fontSize: 14, fontWeight: "600" },
  disabledButton: { opacity: 0.4 },
  ghostButton: {
    borderRadius: 12,
    paddingVertical: 14,
    paddingHorizontal: 16,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "rgba(107,114,128,0.3)",
  },
  ghostButtonText: { color: "#6B7280", fontSize: 14 },
  navRow: { flexDirection: "row", gap: 10 },
  activityRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    padding: 10,
    backgroundColor: "rgba(255,255,255,0.5)",
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "rgba(229,231,235,0.4)",
  },
  activityInfo: { flex: 1 },
  activityName: { fontSize: 13, fontWeight: "500", color: "#1A1A2E" },
  activityCategory: { fontSize: 11, color: "#9CA3AF" },
  excitementEmoji: { fontSize: 18 },
  removeButton: { padding: 4 },
  removeButtonText: { fontSize: 12, color: "#9CA3AF" },
  addForm: { gap: 10 },
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
  categoryScroll: { marginVertical: 2 },
  categoryChip: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    paddingHorizontal: 10,
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
  categoryChipEmoji: { fontSize: 13 },
  categoryChipText: { fontSize: 12, color: "#6B7280" },
  categoryChipTextActive: { color: "#3B82F6", fontWeight: "600" },
  excitementRow: { flexDirection: "row", alignItems: "center", gap: 12 },
  excitementButtons: { flexDirection: "row", gap: 8 },
  excitementOption: { fontSize: 24 },
  excitementDim: { opacity: 0.3 },
  dashedButton: {
    borderWidth: 2,
    borderStyle: "dashed",
    borderColor: "rgba(209,213,219,0.8)",
    borderRadius: 12,
    paddingVertical: 12,
    alignItems: "center",
  },
  dashedButtonDisabled: { opacity: 0.4 },
  dashedButtonText: { fontSize: 13, color: "#6B7280" },
  howItWorks: {
    backgroundColor: "rgba(239,246,255,0.6)",
    borderRadius: 14,
    padding: 16,
    gap: 10,
    width: "100%",
  },
  howItWorksTitle: { fontSize: 13, fontWeight: "600", color: "#1A1A2E" },
  howItWorksRow: { flexDirection: "row", alignItems: "flex-start", gap: 10 },
  howItWorksIcon: { fontSize: 15 },
  howItWorksText: { fontSize: 12, color: "#6B7280", flex: 1, lineHeight: 17 },
});
