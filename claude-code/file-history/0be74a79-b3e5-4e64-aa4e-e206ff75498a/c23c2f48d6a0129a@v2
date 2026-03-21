import { NextResponse } from "next/server";
import { requireAdmin, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { z } from "zod";

const promptSchema = z.object({
  promptText: z.string().min(1),
  promptType: z.enum(["PATTERN", "EXPLORATION", "IDENTITY", "CHALLENGE"]),
});

const createSchema = z.object({
  title: z.string().min(1),
  description: z.string().optional(),
  orderNum: z.number().int().min(1),
  yearKey: z.string().regex(/^\d{4}$/),
  prompts: z.array(promptSchema).min(1),
});

export async function GET() {
  try {
    await requireAdmin();
    const templates = await prisma.reflectionTemplate.findMany({
      orderBy: [{ yearKey: "desc" }, { orderNum: "asc" }],
    });
    return NextResponse.json(templates);
  } catch (error) {
    return apiError(error);
  }
}

export async function POST(req: Request) {
  try {
    await requireAdmin();
    const body = await req.json();
    const data = createSchema.parse(body);
    const template = await prisma.reflectionTemplate.create({ data });
    return NextResponse.json(template);
  } catch (error) {
    return apiError(error);
  }
}
