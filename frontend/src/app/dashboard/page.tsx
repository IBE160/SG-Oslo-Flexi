"use client";

import { useSession, signOut } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import OnboardingWizard from "@/components/OnboardingWizard";
import { FileUpload } from "@/components/documents/FileUpload";
import { DocumentList } from "@/components/documents/DocumentList";
import QuizHistory from "@/components/QuizHistory";
import ProgressSummary from "@/components/ProgressSummary";

export default function Dashboard() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/login");
    }
  }, [status, router]);

  if (status === "loading") {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  if (!session) {
    return null;
  }

  const showWizard = session.user?.is_onboarded === false;

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      {showWizard && <OnboardingWizard onComplete={() => window.location.reload()} />}
      
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-500 mt-1">Welcome back, {session.user?.email}</p>
          </div>
          <button
            onClick={() => signOut({ callbackUrl: "/login" })}
            className="px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 font-medium shadow-sm"
          >
            Sign Out
          </button>
        </div>
        
        {/* Progress Summary */}
        <div className="mb-8">
          <ProgressSummary />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column: Upload */}
          <div className="lg:col-span-1">
             <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 sticky top-8">
                <h2 className="text-xl font-semibold mb-4 text-gray-800">New Document</h2>
                <FileUpload onUploadSuccess={() => setRefreshTrigger(prev => prev + 1)} />
             </div>
          </div>

          {/* Right Column: List */}
          <div className="lg:col-span-2">
             <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-semibold mb-4 text-gray-800">My Library</h2>
                <DocumentList refreshTrigger={refreshTrigger} />
             </div>
          </div>
        </div>

        {/* New Row for Quiz History */}
        <div className="mt-8">
            <QuizHistory />
        </div>
      </div>
    </div>
  );
}