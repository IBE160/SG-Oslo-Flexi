"use client";

import { useState } from "react";
import axios from "axios";

interface Flashcard {
  question: string;
  answer: string;
}

interface FlashcardDisplayProps {
  sessionId: string;
}

export const FlashcardDisplay = ({ sessionId }: FlashcardDisplayProps) => {
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
  const [currentCard, setCurrentCard] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleGenerateFlashcards = async () => {
    setIsLoading(true);
    setError("");
    try {
      const response = await axios.post(
        `/api/v1/orchestrator/${sessionId}/flashcards`
      );
      setFlashcards(response.data.history.slice(-1)[0].flashcards);
      setCurrentCard(0);
      setIsFlipped(false);
    } catch (err) {
      setError("Failed to generate flashcards.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNextCard = () => {
    if (currentCard < flashcards.length - 1) {
      setCurrentCard(currentCard + 1);
      setIsFlipped(false);
    }
  };

  const handlePrevCard = () => {
    if (currentCard > 0) {
      setCurrentCard(currentCard - 1);
      setIsFlipped(false);
    }
  };

  return (
    <div className="w-full max-w-md p-4 my-4 bg-white rounded-lg shadow-md">
      <button 
        onClick={handleGenerateFlashcards} 
        disabled={isLoading}
        className="w-full px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
      >
        {isLoading ? "Generating..." : "Generate Flashcards"}
      </button>
      {error && <p className="mt-2 text-red-500">{error}</p>}
      {flashcards.length > 0 && (
        <div className="mt-4">
          <button 
            type="button"
            className="flex items-center justify-center w-full p-8 border rounded-md h-64 cursor-pointer hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-600 transition-colors"
            onClick={() => setIsFlipped(!isFlipped)}
            aria-label={isFlipped ? "Answer: " + flashcards[currentCard].answer : "Question: " + flashcards[currentCard].question}
          >
            <p className="text-xl text-center">{isFlipped ? flashcards[currentCard].answer : flashcards[currentCard].question}</p>
          </button>
          <div className="flex justify-between mt-4">
            <button onClick={handlePrevCard} disabled={currentCard === 0}>Previous</button>
            <p>{currentCard + 1} / {flashcards.length}</p>
            <button onClick={handleNextCard} disabled={currentCard === flashcards.length - 1}>Next</button>
          </div>
        </div>
      )}
    </div>
  );
};
