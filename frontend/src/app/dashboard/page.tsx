"use client";

import { useSession, signOut } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import OnboardingWizard from "@/components/OnboardingWizard";

export default function Dashboard() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [showWizard, setShowWizard] = useState(false);

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/login");
    }
    if (status === "authenticated" && session?.user?.is_onboarded === false) {
      setShowWizard(true);
    }
  }, [status, router, session]);

  if (status === "loading") {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  if (!session) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      {showWizard && <OnboardingWizard onComplete={() => setShowWizard(false)} />}
      
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
          <button
            onClick={() => signOut({ callbackUrl: "/login" })}
            className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Sign Out
          </button>
        </div>
        
        <div className="bg-blue-50 border border-blue-200 rounded p-4 mb-6">
          <p className="text-blue-800">
            Welcome back, <span className="font-semibold">{session.user?.email}</span>!
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="border rounded p-4 hover:shadow-md transition">
            <h2 className="text-xl font-semibold mb-2">My Documents</h2>
            <p className="text-gray-600">Upload and manage your study materials.</p>
            <button className="mt-4 text-blue-600 hover:underline">View Documents &rarr;</button>
          </div>
          <div className="border rounded p-4 hover:shadow-md transition">
            <h2 className="text-xl font-semibold mb-2">Quizzes</h2>
            <p className="text-gray-600">Review your past quiz performance.</p>
            <button className="mt-4 text-blue-600 hover:underline">View History &rarr;</button>
          </div>
        </div>
      </div>
    </div>
  );
}
