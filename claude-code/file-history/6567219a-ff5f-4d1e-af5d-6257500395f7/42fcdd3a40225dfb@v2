/**
 * register-crons.ts
 *
 * Registers recurring QStash cron jobs for the COMPASS application.
 * Run this once during deployment: `pnpm tsx scripts/register-crons.ts`
 *
 * QStash crons deliver an HTTP POST to the destination URL on schedule.
 * The handler lives at: apps/web/app/api/webhooks/qstash/route.ts
 */

import { Client } from "@upstash/qstash";

const qstash = new Client({ token: process.env.QSTASH_TOKEN! });

const BASE_URL =
  process.env.NEXT_PUBLIC_APP_URL ?? "https://compass.vercel.app";
const WEBHOOK_URL = `${BASE_URL}/api/webhooks/qstash`;

async function registerCrons() {
  console.log("Registering QStash cron jobs...");
  console.log(`Webhook URL: ${WEBHOOK_URL}`);

  // ── 1. Weekly nudge sweep — every Monday at 9:00 AM UTC ──────────────
  const nudgeSweep = await qstash.schedules.create({
    destination: WEBHOOK_URL,
    cron: "0 9 * * 1", // Monday 09:00 UTC
    body: JSON.stringify({ type: "WEEKLY_NUDGE_SWEEP" }),
    headers: { "Content-Type": "application/json" },
    retries: 3,
  });
  console.log(`✓ WEEKLY_NUDGE_SWEEP scheduled: ${nudgeSweep.scheduleId}`);

  // ── 2. Opportunity sweep — nightly at 2:00 AM UTC ────────────────────
  const opportunitySweep = await qstash.schedules.create({
    destination: WEBHOOK_URL,
    cron: "0 2 * * *", // Daily 02:00 UTC
    body: JSON.stringify({ type: "OPPORTUNITY_SWEEP" }),
    headers: { "Content-Type": "application/json" },
    retries: 3,
  });
  console.log(
    `✓ OPPORTUNITY_SWEEP scheduled: ${opportunitySweep.scheduleId}`
  );

  console.log("\nAll cron jobs registered successfully.");
  console.log(
    "View schedules at: https://console.upstash.com/qstash → Schedules"
  );
}

registerCrons().catch((err) => {
  console.error("Failed to register cron jobs:", err);
  process.exit(1);
});
