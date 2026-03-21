import { redirect } from "next/navigation";
import { auth } from "@clerk/nextjs/server";
import { prisma } from "@compass/db";
import CounselorSidebar from "@/components/counselor/CounselorSidebar";

export default async function CounselorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { userId } = await auth();
  if (!userId) redirect("/sign-in");

  const counselor = await prisma.counselor.findUnique({
    where: { clerkId: userId },
    include: { school: true },
  });

  if (!counselor) redirect("/sign-in");

  return (
    <div className="min-h-screen bg-[#F2F4F7] flex">
      {/* Sidebar */}
      <CounselorSidebar counselor={counselor} />

      {/* Main Content */}
      <main className="flex-1 ml-64 p-8">
        <div className="max-w-5xl mx-auto">{children}</div>
      </main>
    </div>
  );
}
