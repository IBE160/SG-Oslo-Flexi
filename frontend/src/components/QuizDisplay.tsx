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
        className="w-full px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
      >
        {isLoading ? "Generating..." : "Generate Quiz"}
      </button>
      {error && <p className="mt-2 text-red-500">{error}</p>}
      {quiz.length > 0 && (
        <div className="mt-4">
          <fieldset>
            <legend className="text-lg font-semibold mb-2">{quiz[currentQuestion].question}</legend>
            <div className="flex flex-col">
              {quiz[currentQuestion].options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => handleSelectAnswer(option)}
                  className={`p-2 my-1 border rounded-md text-left transition-colors focus:outline-none focus:ring-2 focus:ring-blue-600 ${
                    selectedAnswer === option
                      ? isCorrect
                        ? "bg-green-200 border-green-400"
                        : "bg-red-200 border-red-400"
                      : "bg-white hover:bg-gray-50 border-gray-200"
                  }`}
                  disabled={selectedAnswer !== null}
                >
                  {option}
                </button>
              ))}
            </div>
          </fieldset>
          {selectedAnswer && (
            <div className="mt-4" aria-live="polite">
              <p className="font-medium">
                {isCorrect 
                  ? <span className="text-green-700">Correct!</span> 
                  : <span className="text-red-700">Incorrect. The correct answer is: {quiz[currentQuestion].correct_answer}</span>
                }
              </p>
              <button 
                onClick={handleNextQuestion}
                disabled={currentQuestion === quiz.length - 1}
                className="w-full px-4 py-2 mt-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-600"
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
