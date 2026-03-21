import type { Metadata } from "next";
import { ClerkProvider } from "@clerk/nextjs";
import "./globals.css";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "COMPASS — Your Learning Journey",
  description: "A longitudinal student operating system for high school self-authorship",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className="min-h-screen bg-[#F2F4F7]">{children}</body>
      </html>
    </ClerkProvider>
  );
}
