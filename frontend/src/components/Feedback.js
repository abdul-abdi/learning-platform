import React, { useState } from 'react';
import { sendFeedback } from '../services/api';

const Feedback = () => {
  const [feedback, setFeedback] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await sendFeedback(feedback);
      setSubmitted(true);
      setFeedback('');
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  return (
    <div className="mt-8">
      <h2 className="text-2xl font-bold mb-4">Feedback</h2>
      {submitted ? (
        <p className="text-green-600">Thank you for your feedback!</p>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <textarea
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            className="w-full p-2 border rounded"
            rows="4"
            placeholder="Please share your thoughts or report any issues..."
            required
          ></textarea>
          <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
            Submit Feedback
          </button>
        </form>
      )}
    </div>
  );
};

export default Feedback;