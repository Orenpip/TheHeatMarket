import { NextResponse } from "next/server";
import { requireStudent, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { MapNodeType } from "@compass/db";
import { z } from "zod";

const querySchema = z.object({
  q: z.string().min(1).max(200),
  type: z.nativeEnum(MapNodeType).optional(),
});

export async function GET(req: Request) {
  try {
    await requireStudent();
    const { searchParams } = new URL(req.url);

    const query = querySchema.parse({
      q: searchParams.get("q") ?? "",
      type: searchParams.get("type") ?? undefined,
    });

    const nodes = await prisma.mapNode.findMany({
      where: {
        ...(query.type ? { type: query.type } : {}),
        OR: [
          { label: { contains: query.q, mode: "insensitive" } },
          { description: { contains: query.q, mode: "insensitive" } },
        ],
      },
      select: {
        id: true,
        type: true,
        label: true,
        description: true,
        metadata: true,
        parentId: true,
      },
      take: 20,
      orderBy: { label: "asc" },
    });

    return NextResponse.json(nodes);
  } catch (error) {
    return apiError(error);
  }
}
