import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import axios from 'axios';

import Question from '../../../components/Question';


const QuizPage = () => {
    const router = useRouter();
    const { id } = router.query;
    const [quiz, setQuiz] = useState(null);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [userAnswers, setUserAnswers] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (id) {
            axios.get(`/api/documents/${id}/quiz`)
                .then(response => {
                    setQuiz(response.data);
                    setLoading(false);
                })
                .catch(err => {
                    setError('Failed to load quiz. Please try again later.');
                    setLoading(false);
                });
        }
    }, [id]);

    const handleOptionChange = (questionId, option) => {
        setUserAnswers({ ...userAnswers, [questionId]: option });
    };

    const handleNextQuestion = () => {
        setCurrentQuestionIndex(prev => Math.min(prev + 1, quiz.questions.length - 1));
    };

    const handlePrevQuestion = () => {
        setCurrentQuestionIndex(prev => Math.max(prev - 1, 0));
    };
    
    const handleSubmit = () => {
        // Redirect to results page
        router.push(`/results/${id}?answers=${JSON.stringify(userAnswers)}`);
    };

    if (loading) return <div className="text-center mt-10">Loading quiz...</div>;
    if (error) return <div className="text-center mt-10 text-red-500">{error}</div>;
    if (!quiz) return <div className="text-center mt-10">No quiz found.</div>;

    const currentQuestion = quiz.questions[currentQuestionIndex];

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4 text-center">{quiz.title}</h1>
            <div className="max-w-xl mx-auto bg-white p-6 rounded-lg shadow-lg">
                <Question
                    question={currentQuestion.question}
                    options={currentQuestion.options}
                    selectedOption={userAnswers[currentQuestion.id]}
                    onOptionChange={(option) => handleOptionChange(currentQuestion.id, option)}
                />
                <div className="flex justify-between mt-6">
                    <button onClick={handlePrevQuestion} disabled={currentQuestionIndex === 0} className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50">
                        Previous
                    </button>
                    {currentQuestionIndex === quiz.questions.length - 1 ? (
                         <button onClick={handleSubmit} className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
                            Submit
                        </button>
                    ) : (
                        <button onClick={handleNextQuestion} className="bg-blue-700 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded">
                            Next
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
};

export default QuizPage;
