"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@compass/ui";

export default function StartSessionButton() {
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleStart() {
    setLoading(true);
    try {
      const res = await fetch("/api/sessions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });

      if (!res.ok) throw new Error("Failed to create session");

      const session = await res.json() as { id: string };
      router.push(`/reflect/${session.id}`);
    } catch {
      setLoading(false);
    }
  }

  return (
    <Button onClick={handleStart} loading={loading} fullWidth size="lg">
      Start Reflection
    </Button>
  );
}
