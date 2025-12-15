import { useEffect, useState } from 'react';
import axios from 'axios';

interface QuizHistoryItem {
    quiz_title: string;
    score: number;
    taken_at: string;
}

const QuizHistory = () => {
    const [history, setHistory] = useState<QuizHistoryItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        axios.get('/api/users/me/quiz-history')
            .then(response => {
                setHistory(response.data);
                setLoading(false);
            })
                  .catch(() => {
                    setError('Failed to load quiz history.');
                    setLoading(false);
                  });    }, []);

    if (loading) return <div>Loading quiz history...</div>;
    if (error) return <div className="text-red-500">{error}</div>;

    return (
        <div className="bg-white shadow-lg rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4">Quiz History</h2>
            {history.length === 0 ? (
                <p>No quiz history found.</p>
            ) : (
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Quiz
                            </th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Score
                            </th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Date
                            </th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {history.map((item, index) => (
                            <tr key={index}>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    {item.quiz_title}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    {item.score}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    {new Date(item.taken_at).toLocaleDateString()}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default QuizHistory;
