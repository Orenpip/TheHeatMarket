import { redirect } from "next/navigation";
import { auth } from "@clerk/nextjs/server";
import { prisma } from "@compass/db";
import BottomNav from "@/components/BottomNav";

export default async function StudentLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { userId } = await auth();
  if (!userId) redirect("/sign-in");

  const student = await prisma.student.findUnique({
    where: { clerkId: userId },
  });

  if (!student) redirect("/sign-in");

  // Redirect to onboarding if not completed
  if (!student.onboardingCompleted) {
    redirect("/onboarding");
  }

  return (
    <div className="min-h-screen bg-[#F2F4F7] pb-20">
      {/* Background gradients */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute top-[-20%] right-[-10%] w-[600px] h-[600px] rounded-full bg-blue-100/40 blur-[80px]" />
        <div className="absolute bottom-[20%] left-[-10%] w-[400px] h-[400px] rounded-full bg-violet-100/30 blur-[80px]" />
      </div>

      <main className="relative z-10 max-w-2xl mx-auto px-4 pt-6">
        {children}
      </main>

      <BottomNav />
    </div>
  );
}
