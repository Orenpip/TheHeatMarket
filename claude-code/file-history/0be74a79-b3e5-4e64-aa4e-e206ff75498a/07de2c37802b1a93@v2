import { auth, currentUser } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";
import { prisma } from "@compass/db";

export class AuthError extends Error {
  constructor(
    message: string,
    public readonly status: 401 | 403 = 401
  ) {
    super(message);
    this.name = "AuthError";
  }
}

export function apiError(error: unknown): NextResponse {
  if (error instanceof AuthError) {
    return NextResponse.json({ error: error.message }, { status: error.status });
  }
  console.error("[API Error]", error);
  return NextResponse.json({ error: "Internal server error" }, { status: 500 });
}

export async function requireStudent() {
  const { userId } = await auth();
  if (!userId) {
    throw new AuthError("Unauthorized", 401);
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
    throw new AuthError("Unauthorized", 401);
  }

  return student;
}

export async function requireCounselor() {
  const { userId } = await auth();
  if (!userId) {
    throw new AuthError("Unauthorized", 401);
  }

  const counselor = await prisma.counselor.findUnique({
    where: { clerkId: userId },
    include: {
      school: true,
    },
  });

  if (!counselor) {
    throw new AuthError("Forbidden", 403);
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
  if (!user) throw new AuthError("Unauthorized", 401);
  const role = user.publicMetadata?.role as string | undefined;
  if (role !== "admin") throw new AuthError("Forbidden", 403);
  return user;
}
