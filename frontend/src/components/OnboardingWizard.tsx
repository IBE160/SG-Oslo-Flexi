"use client";

import { useState } from "react";
import { useSession } from "next-auth/react";
import { completeOnboarding } from "@/lib/api";

interface OnboardingWizardProps {
  onComplete: () => void;
}

export default function OnboardingWizard({ onComplete }: OnboardingWizardProps) {
  const { data: session, update } = useSession();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);

  const handleNext = async () => {
    if (step < 3) {
      setStep(step + 1);
    } else {
      await handleFinish();
    }
  };

  const handleFinish = async () => {
    if (!session?.accessToken) return;
    setLoading(true);
    try {
      await completeOnboarding(session.accessToken);
      await update({ user: { ...session.user, is_onboarded: true } });
      onComplete();
    } catch (error) {
      console.error("Onboarding failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8 max-w-md w-full shadow-xl">
        {step === 1 && (
          <div className="text-center">
            <h2 className="text-2xl font-bold mb-4">Welcome to AI Buddy! 👋</h2>
            <p className="text-gray-600 mb-6">
              We're excited to help you study smarter. Let's take a quick tour.
            </p>
          </div>
        )}

        {step === 2 && (
          <div className="text-center">
            <h2 className="text-2xl font-bold mb-4">📂 Upload Documents</h2>
            <p className="text-gray-600 mb-6">
              Start by uploading your notes, PDFs, or images. We'll analyze them for you.
            </p>
          </div>
        )}

        {step === 3 && (
          <div className="text-center">
            <h2 className="text-2xl font-bold mb-4">⚡ Generate Quizzes</h2>
            <p className="text-gray-600 mb-6">
              Once analyzed, turn your documents into interactive quizzes and flashcards instantly.
            </p>
          </div>
        )}

        <div className="flex justify-end gap-2 mt-4">
           {/* Skip button logic could act as finish or simple dismiss */}
          <button
            onClick={handleNext}
            disabled={loading}
            className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Finishing..." : step === 3 ? "Get Started" : "Next"}
          </button>
        </div>
      </div>
    </div>
  );
}
