import React, { useState, useEffect } from 'react';
import { Paper, Typography, RadioGroup, FormControlLabel, Radio, Button, Box } from '@material-ui/core';
import { getQuiz, submitQuiz } from '../../services/api';

const Quiz = ({ materialId }) => {
  const [quiz, setQuiz] = useState(null);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchQuiz = async () => {
      try {
        const response = await getQuiz(materialId);
        setQuiz(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load quiz');
        setLoading(false);
      }
    };

    fetchQuiz();
  }, [materialId]);

  const handleAnswerChange = (questionId, answer) => {
    setAnswers({ ...answers, [questionId]: answer });
  };

  const handleSubmit = async () => {
    try {
      const response = await submitQuiz(materialId, { answers: Object.entries(answers).map(([questionId, answer]) => ({ question_id: questionId, user_answer: answer })) });
      setResult(response.data);
    } catch (err) {
      setError('Failed to submit quiz');
    }
  };

  if (loading) return <Typography>Loading quiz...</Typography>;
  if (error) return <Typography color="error">{error}</Typography>;
  if (!quiz) return <Typography>No quiz found for this material</Typography>;

  return (
    <Paper style={{ padding: '2rem', marginTop: '2rem' }}>
      <Typography variant="h4" gutterBottom>{quiz.title}</Typography>
      <Typography variant="body1" paragraph>{quiz.description}</Typography>
      {!result && (
        <>
          {quiz.questions.map((question) => (
            <Box key={question.id} my={3}>
              <Typography variant="h6">{question.question_text}</Typography>
              <RadioGroup
                value={answers[question.id] || ''}
                onChange={(e) => handleAnswerChange(question.id, e.target.value)}
              >
                {question.options.map((option, index) => (
                  <FormControlLabel
                    key={index}
                    value={option}
                    control={<Radio />}
                    label={option}
                  />
                ))}
              </RadioGroup>
            </Box>
          ))}
          <Button variant="contained" color="primary" onClick={handleSubmit}>
            Submit Quiz
          </Button>
        </>
      )}
      {result && (
        <Box mt={3}>
          <Typography variant="h5">Quiz Result</Typography>
          <Typography>Score: {result.score} / {result.total_questions}</Typography>
          <Typography>Percentage: {result.percentage_score.toFixed(2)}%</Typography>
        </Box>
      )}
    </Paper>
  );
};

export default Quiz;