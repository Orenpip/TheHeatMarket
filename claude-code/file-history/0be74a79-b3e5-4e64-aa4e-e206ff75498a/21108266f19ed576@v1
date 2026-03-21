import { NextResponse } from "next/server";
import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";

export async function GET(
  _req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    await requireStudent();
    const { id } = await params;

    const node = await prisma.mapNode.findUnique({
      where: { id },
      select: {
        id: true,
        type: true,
        label: true,
        description: true,
        metadata: true,
        parentId: true,
        createdAt: true,
        updatedAt: true,
        outEdges: {
          include: {
            target: {
              select: {
                id: true,
                type: true,
                label: true,
                description: true,
                metadata: true,
              },
            },
          },
        },
        inEdges: {
          include: {
            source: {
              select: {
                id: true,
                type: true,
                label: true,
                description: true,
                metadata: true,
              },
            },
          },
        },
        children: {
          select: {
            id: true,
            type: true,
            label: true,
            description: true,
            metadata: true,
          },
        },
      },
    });

    if (!node) {
      return NextResponse.json({ error: "Not found" }, { status: 404 });
    }

    return NextResponse.json(node);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
