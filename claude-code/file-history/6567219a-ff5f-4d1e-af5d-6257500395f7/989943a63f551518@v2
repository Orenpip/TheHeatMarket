import { NextResponse } from "next/server";
import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";
import { MapNodeType } from "@compass/db";
import { z } from "zod";

const querySchema = z.object({
  type: z.nativeEnum(MapNodeType).optional(),
  parentId: z.string().optional(),
});

export async function GET(req: Request) {
  try {
    await requireStudent();
    const { searchParams } = new URL(req.url);

    const query = querySchema.parse({
      type: searchParams.get("type") ?? undefined,
      parentId: searchParams.get("parentId") ?? undefined,
    });

    const nodes = await prisma.mapNode.findMany({
      where: {
        ...(query.type ? { type: query.type } : {}),
        ...(query.parentId ? { parentId: query.parentId } : {}),
      },
      select: {
        id: true,
        type: true,
        label: true,
        description: true,
        metadata: true,
        parentId: true,
        createdAt: true,
        updatedAt: true,
      },
      orderBy: { label: "asc" },
    });

    return NextResponse.json(nodes);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
