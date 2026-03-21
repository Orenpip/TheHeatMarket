import { SignIn } from "@clerk/nextjs";

export default function SignInPage() {
  return (
    <div className="min-h-screen bg-[#F2F4F7] flex items-center justify-center p-4">
      {/* Background gradient */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-20%] right-[-10%] w-[600px] h-[600px] rounded-full bg-blue-200/30 blur-[80px]" />
        <div className="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] rounded-full bg-violet-200/20 blur-[80px]" />
      </div>

      <div className="relative z-10 text-center">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-[#1A1A2E] mb-2">COMPASS</h1>
          <p className="text-[#6B7280]">Your longitudinal learning journey</p>
        </div>
        <SignIn
          appearance={{
            elements: {
              formButtonPrimary:
                "bg-[#3B82F6] hover:bg-blue-600 text-white font-medium",
              card: "shadow-[0_8px_32px_0_rgba(31,38,135,0.15)] rounded-[16px] border border-white/[0.18] bg-white/[0.72] backdrop-blur-[20px]",
            },
          }}
        />
      </div>
    </div>
  );
}
