"use client";

import { useState } from "react";
import axios from "axios";

interface QuizQuestion {
  question: string;
  options: string[];
  correct_answer: string;
}

interface QuizDisplayProps {
  sessionId: string;
}

export const QuizDisplay = ({ sessionId }: QuizDisplayProps) => {
  const [quiz, setQuiz] = useState<QuizQuestion[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleGenerateQuiz = async () => {
    setIsLoading(true);
    setError("");
    try {
      const response = await axios.post(
        `/api/v1/orchestrator/${sessionId}/quiz`
      );
      setQuiz(response.data.history.slice(-1)[0].quiz);
      setCurrentQuestion(0);
      setSelectedAnswer(null);
      setIsCorrect(null);
    } catch (err) {
      setError("Failed to generate quiz.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectAnswer = (option: string) => {
    setSelectedAnswer(option);
    setIsCorrect(option === quiz[currentQuestion].correct_answer);
  };

  const handleNextQuestion = () => {
    if (currentQuestion < quiz.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer(null);
      setIsCorrect(null);
    }
  };

  return (
    <div className="w-full max-w-md p-4 my-4 bg-white rounded-lg shadow-md">
      <button 
        onClick={handleGenerateQuiz} 
        disabled={isLoading}
        className="w-full px-4 py-2 text-white bg-blue-700 rounded-md hover:bg-blue-800 disabled:bg-gray-400"
      >
        {isLoading ? "Generating..." : "Generate Quiz"}
      </button>
      {error && <p className="mt-2 text-red-500">{error}</p>}
      {quiz.length > 0 && (
        <div className="mt-4">
          <h3 className="text-lg font-semibold">{quiz[currentQuestion].question}</h3>
          <div className="flex flex-col mt-2">
            {quiz[currentQuestion].options.map((option, index) => (
              <button
                key={index}
                onClick={() => handleSelectAnswer(option)}
                className={`p-2 my-1 border rounded-md ${
                  selectedAnswer === option
                    ? isCorrect
                      ? "bg-green-200"
                      : "bg-red-200"
                    : "bg-white"
                }`}
                disabled={selectedAnswer !== null}
              >
                {option}
              </button>
            ))}
          </div>
          {selectedAnswer && (
            <div className="mt-4">
              <p>{isCorrect ? "Correct!" : `Incorrect. The correct answer is: ${quiz[currentQuestion].correct_answer}`}</p>
              <button 
                onClick={handleNextQuestion}
                disabled={currentQuestion === quiz.length - 1}
                className="w-full px-4 py-2 mt-2 text-white bg-blue-700 rounded-md hover:bg-blue-800 disabled:bg-gray-400"
              >
                Next Question
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
