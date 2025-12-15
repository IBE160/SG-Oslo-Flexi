interface QuestionProps {
  question: string;
  options: string[];
  selectedOption: string;
  onOptionChange: (option: string) => void;
}

const Question: React.FC<QuestionProps> = ({ question, options, selectedOption, onOptionChange }) => {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">{question}</h2>
      <div className="space-y-2">
        {options.map((option, index) => (
          <div key={index} className="flex items-center">
            <input
              type="radio"
              id={`option-${index}`}
              name="quiz-option"
              value={option}
              checked={selectedOption === option}
              onChange={(e) => onOptionChange(e.target.value)}
              className="mr-2"
            />
            <label htmlFor={`option-${index}`}>{option}</label>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Question;
