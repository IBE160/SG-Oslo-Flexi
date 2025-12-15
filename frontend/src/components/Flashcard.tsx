interface FlashcardProps {
  question: string;
  answer: string;
  flipped: boolean;
  onFlip: () => void;
}

const Flashcard: React.FC<FlashcardProps> = ({ question, answer, flipped, onFlip }) => {
  return (
    <button
      type="button"
      onClick={onFlip}
      aria-pressed={flipped}
      className="p-6 rounded-lg shadow-lg bg-white min-h-[200px] flex items-center justify-center w-full text-left"
    >
      <p className="text-xl">{flipped ? answer : question}</p>
    </button>
  );
};

export default Flashcard;
