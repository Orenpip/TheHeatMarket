import { auth, currentUser } from "@clerk/nextjs/server";
import { prisma } from "@compass/db";

export async function requireStudent() {
  const { userId } = await auth();
  if (!userId) {
    throw new Error("Unauthorized");
  }

  const student = await prisma.student.findUnique({
    where: { clerkId: userId },
    include: {
      school: true,
      privacySettings: true,
      notificationPrefs: true,
    },
  });

  if (!student) {
    throw new Error("Student not found");
  }

  return student;
}

export async function requireCounselor() {
  const { userId } = await auth();
  if (!userId) {
    throw new Error("Unauthorized");
  }

  const counselor = await prisma.counselor.findUnique({
    where: { clerkId: userId },
    include: {
      school: true,
    },
  });

  if (!counselor) {
    throw new Error("Counselor not found");
  }

  return counselor;
}

export async function getStudentOrNull() {
  try {
    return await requireStudent();
  } catch {
    return null;
  }
}

export async function getCurrentUserId(): Promise<string | null> {
  const { userId } = await auth();
  return userId;
}

export async function requireAdmin() {
  const user = await currentUser();
  if (!user) throw new Error("Unauthorized");
  const role = user.publicMetadata?.role as string | undefined;
  if (role !== "admin") throw new Error("Forbidden");
  return user;
}
