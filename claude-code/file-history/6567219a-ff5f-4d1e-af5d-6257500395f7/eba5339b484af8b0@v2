import { headers } from "next/headers";
import { Webhook } from "svix";
import { WebhookEvent } from "@clerk/nextjs/server";
import { prisma } from "@compass/db";
import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const WEBHOOK_SECRET = process.env.CLERK_WEBHOOK_SECRET;
  if (!WEBHOOK_SECRET) {
    throw new Error("CLERK_WEBHOOK_SECRET is not set");
  }

  // Get svix headers
  const headerPayload = await headers();
  const svix_id = headerPayload.get("svix-id");
  const svix_timestamp = headerPayload.get("svix-timestamp");
  const svix_signature = headerPayload.get("svix-signature");

  if (!svix_id || !svix_timestamp || !svix_signature) {
    return NextResponse.json({ error: "Missing svix headers" }, { status: 400 });
  }

  const payload = await req.json();
  const body = JSON.stringify(payload);

  const wh = new Webhook(WEBHOOK_SECRET);
  let evt: WebhookEvent;

  try {
    evt = wh.verify(body, {
      "svix-id": svix_id,
      "svix-timestamp": svix_timestamp,
      "svix-signature": svix_signature,
    }) as WebhookEvent;
  } catch {
    return NextResponse.json({ error: "Invalid webhook" }, { status: 400 });
  }

  const { type, data } = evt;

  if (type === "user.created" || type === "user.updated") {
    const { id: clerkId, email_addresses, first_name, last_name, public_metadata } = data;
    const email = email_addresses[0]?.email_address;
    const role = (public_metadata?.role as string) ?? "STUDENT";

    if (!email) {
      return NextResponse.json({ error: "No email" }, { status: 400 });
    }

    if (role === "COUNSELOR") {
      await prisma.counselor.upsert({
        where: { clerkId },
        update: {
          email,
          firstName: first_name ?? "",
          lastName: last_name ?? "",
        },
        create: {
          clerkId,
          email,
          firstName: first_name ?? "",
          lastName: last_name ?? "",
          schoolId: (public_metadata?.schoolId as string) ?? "default-school",
        },
      });
    } else {
      // Default to STUDENT
      await prisma.student.upsert({
        where: { clerkId },
        update: {
          email,
          firstName: first_name ?? "",
          lastName: last_name ?? "",
        },
        create: {
          clerkId,
          email,
          firstName: first_name ?? "",
          lastName: last_name ?? "",
          schoolId: (public_metadata?.schoolId as string) ?? undefined,
        },
      });

      // Create default privacy settings
      const student = await prisma.student.findUnique({ where: { clerkId } });
      if (student) {
        await prisma.studentPrivacySettings.upsert({
          where: { studentId: student.id },
          update: {},
          create: { studentId: student.id },
        });

        await prisma.notificationPreferences.upsert({
          where: { studentId: student.id },
          update: {},
          create: { studentId: student.id },
        });
      }
    }
  }

  if (type === "user.deleted") {
    const { id: clerkId } = data;
    // Cascade deletes via DB constraints
    await prisma.student.deleteMany({ where: { clerkId: clerkId! } });
    await prisma.counselor.deleteMany({ where: { clerkId: clerkId! } });
  }

  return NextResponse.json({ received: true });
}
