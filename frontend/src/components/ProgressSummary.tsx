import { useEffect, useState } from 'react';
import axios from 'axios';

interface ProgressSummaryData {
    average_score: number;
    total_quizzes: number;
}

const ProgressSummary = () => {
    const [summary, setSummary] = useState<ProgressSummaryData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        axios.get('/api/users/me/progress-summary')
            .then(response => {
                setSummary(response.data);
                setLoading(false);
            })
                  .catch(() => {
                    setError('Failed to load progress summary.');
                    setLoading(false);
                  });    }, []);

    if (loading) return <div>Loading progress...</div>;
    if (error) return <div className="text-red-500">{error}</div>;

    return (
        <div className="bg-white shadow-lg rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4">Progress Summary</h2>
            {summary ? (
                <div className="flex justify-around">
                    <div className="text-center">
                        <p className="text-3xl font-bold">{summary.average_score.toFixed(2)}</p>
                        <p className="text-gray-500">Average Score</p>
                    </div>
                    <div className="text-center">
                        <p className="text-3xl font-bold">{summary.total_quizzes}</p>
                        <p className="text-gray-500">Total Quizzes</p>
                    </div>
                </div>
            ) : (
                <p>No progress to show yet.</p>
            )}
        </div>
    );
};

export default ProgressSummary;
