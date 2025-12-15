interface FlashcardProps {
  question: string;
  answer: string;
  flipped: boolean;
  onFlip: () => void;
}

const Flashcard: React.FC<FlashcardProps> = ({ question, answer, flipped, onFlip }) => {
  return (
    <div
      onClick={onFlip}
      className="cursor-pointer p-6 rounded-lg shadow-lg bg-white min-h-[200px] flex items-center justify-center"
    >
      <p className="text-xl">{flipped ? answer : question}</p>
    </div>
  );
};

export default Flashcard;
