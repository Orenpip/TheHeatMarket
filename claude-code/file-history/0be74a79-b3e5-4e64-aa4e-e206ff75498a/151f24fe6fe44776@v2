import { NextResponse } from "next/server";
import { requireStudent, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { z } from "zod";

const querySchema = z.object({
  page: z.coerce.number().default(1),
  limit: z.coerce.number().min(1).max(100).default(20),
  unreadOnly: z.coerce.boolean().default(false),
});

export async function GET(req: Request) {
  try {
    const student = await requireStudent();
    const { searchParams } = new URL(req.url);

    const { page, limit, unreadOnly } = querySchema.parse({
      page: searchParams.get("page"),
      limit: searchParams.get("limit"),
      unreadOnly: searchParams.get("unreadOnly"),
    });

    const skip = (page - 1) * limit;

    const [notifications, total] = await Promise.all([
      prisma.notification.findMany({
        where: {
          studentId: student.id,
          ...(unreadOnly ? { readAt: null } : {}),
        },
        orderBy: { createdAt: "desc" },
        skip,
        take: limit,
        include: {
          relatedNode: {
            select: {
              id: true,
              type: true,
              label: true,
            },
          },
        },
      }),
      prisma.notification.count({
        where: {
          studentId: student.id,
          ...(unreadOnly ? { readAt: null } : {}),
        },
      }),
    ]);

    return NextResponse.json({
      notifications,
      total,
      page,
      totalPages: Math.ceil(total / limit),
    });
  } catch (error) {
    return apiError(error);
  }
}
