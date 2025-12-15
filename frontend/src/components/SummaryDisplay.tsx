"use client";

import { useState } from "react";
import axios from "axios";

interface SummaryDisplayProps {
  sessionId: string;
}

export const SummaryDisplay = ({ sessionId }: SummaryDisplayProps) => {
  const [summary, setSummary] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleGenerateSummary = async () => {
    setIsLoading(true);
    setError("");
    try {
      const response = await axios.post(
        `/api/v1/orchestrator/${sessionId}/summarize`
      );
      setSummary(response.data.history.slice(-1)[0].summary);
    } catch (err) {
      setError("Failed to generate summary.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md p-4 my-4 bg-white rounded-lg shadow-md">
      <button 
        onClick={handleGenerateSummary} 
        disabled={isLoading}
        className="w-full px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
      >
        {isLoading ? "Generating..." : "Generate Summary"}
      </button>
      {error && <p className="mt-2 text-red-500">{error}</p>}
      {summary && (
        <pre className="p-4 mt-4 overflow-auto text-sm bg-gray-100 rounded-md">
          <code>{summary}</code>
        </pre>
      )}
    </div>
  );
};
