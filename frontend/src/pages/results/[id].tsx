import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import axios from 'axios';

const QuizResultsPage = () => {
    const router = useRouter();
    const { id, answers } = router.query;
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (id && answers) {
            // In a real app, you'd get the quiz ID from the page context, not the document ID
            const quizId = id; 
            
            axios.post(`/api/quizzes/${quizId}/submit`, { answers: JSON.parse(answers as string) })
                .then(response => {
                    setResults(response.data);
                    setLoading(false);
                })
                .catch(err => {
                    setError('Failed to submit quiz results.');
                    setLoading(false);
                });
        }
    }, [id, answers]);

    if (loading) return <div className="text-center mt-10">Loading results...</div>;
    if (error) return <div className="text-center mt-10 text-red-500">{error}</div>;
    if (!results) return <div className="text-center mt-10">No results found.</div>;

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4 text-center">Quiz Results</h1>
            <div className="max-w-xl mx-auto bg-white p-6 rounded-lg shadow-lg">
                <h2 className="text-xl font-semibold mb-4">You scored {results.score} out of {results.totalQuestions}</h2>
                <div>
                    {results.questions.map(q => (
                        <div key={q.id} className="mb-4">
                            <p className="font-semibold">{q.question}</p>
                            <p className={q.isCorrect ? 'text-green-500' : 'text-red-500'}>
                                Your answer: {q.userAnswer}. Correct answer: {q.correctAnswer}.
                            </p>
                        </div>
                    ))}
                </div>
                <button onClick={() => router.push('/dashboard')} className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                    Back to Dashboard
                </button>
            </div>
        </div>
    );
};

export default QuizResultsPage;
