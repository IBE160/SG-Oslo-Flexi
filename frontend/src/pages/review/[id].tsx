import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

import Flashcard from '../../components/Flashcard';

import axios from 'axios';

const FlashcardReviewPage = () => {
  const router = useRouter();
  const { id } = router.query;
  const [flashcards, setFlashcards] = useState<{id: number, question: string, answer: string}[]>([]);
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
        axios.get(`/api/documents/${id}/flashcards`)
            .then(response => {
                setFlashcards(response.data);
                setLoading(false);
            })
            .catch(err => {
                setError('Failed to load flashcards. Please try again later.');
                setLoading(false);
            });
    }
  }, [id]);

  const handleFlip = () => {
    setFlipped(!flipped);
  };

  const handleNextCard = () => {
    setFlipped(false);
    setCurrentCardIndex((prevIndex) => (prevIndex + 1) % flashcards.length);
  };

    const handlePrevCard = () => {
    setFlipped(false);
    setCurrentCardIndex((prevIndex) => (prevIndex - 1 + flashcards.length) % flashcards.length);
  };

  if (loading) {
    return <div className="text-center mt-10">Loading flashcards...</div>;
  }
  
  if (error) {
    return <div className="text-center mt-10 text-red-500">{error}</div>;
  }

  if (flashcards.length === 0) {
    return <div className="text-center mt-10">No flashcards found for this document.</div>;
  }

  const currentFlashcard = flashcards[currentCardIndex];

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4 text-center">Flashcard Review</h1>
      <div className="max-w-xl mx-auto">
        <Flashcard
          question={currentFlashcard.question}
          answer={currentFlashcard.answer}
          flipped={flipped}
          onFlip={handleFlip}
        />
        <div className="flex justify-between mt-4">
            <button
                onClick={handlePrevCard}
                className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
            >
                Previous
            </button>
            <button
                onClick={handleNextCard}
                className="bg-blue-700 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded"
            >
                Next
            </button>
        </div>
      </div>
    </div>
  );
};

export default FlashcardReviewPage;
