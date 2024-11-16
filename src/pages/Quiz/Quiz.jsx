import React, { useState } from 'react';

// Custom Button Component
const Button = ({ children, onClick, disabled, className }) => (
  <button
    onClick={onClick}
    disabled={disabled}
    className={`button ${disabled ? 'disabled' : ''} ${className}`}
  >
    {children}
  </button>
);

// Custom Card Component
const Card = ({ children }) => (
  <div className="card">
    {children}
  </div>
);

// Custom Alert Component
const Alert = ({ children, type }) => (
  <div className={`alert ${type}`}>
    {children}
  </div>
);

const Quiz = () => {
  const [showQuiz, setShowQuiz] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [score, setScore] = useState(0);
  const [showResult, setShowResult] = useState(false);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [showFeedback, setShowFeedback] = useState(false);

  const questions = [
    {
      question: "What is the capital of France?",
      options: ["London", "Berlin", "Paris", "Madrid"],
      correctAnswer: 2
    },
    {
      question: "Which planet is known as the Red Planet?",
      options: ["Jupiter", "Mars", "Venus", "Saturn"],
      correctAnswer: 1
    },
    // Add more questions here to make it 20
  ];

  const handleStartQuiz = () => {
    setShowQuiz(true);
    setScore(0);
    setCurrentQuestion(0);
    setShowResult(false);
  };

  const handleAnswerSelect = (selectedIndex) => {
    setSelectedAnswer(selectedIndex);
    setShowFeedback(true);

    if (selectedIndex === questions[currentQuestion].correctAnswer) {
      setScore(score + 1);
    }

    setTimeout(() => {
      setShowFeedback(false);
      setSelectedAnswer(null);
      
      if (currentQuestion < questions.length - 1) {
        setCurrentQuestion(currentQuestion + 1);
      } else {
        setShowResult(true);
      }
    }, 1500);
  };

  const getButtonStyles = (index) => {
    if (!showFeedback) return 'default';
    if (index === questions[currentQuestion].correctAnswer) return 'correct';
    if (index === selectedAnswer) return 'wrong';
    return 'default';
  };

  return (
    <div className="quiz-container">
      {!showQuiz ? (
        <Button onClick={handleStartQuiz} className="start-button">
          Start Quiz
        </Button>
      ) : showResult ? (
        <Card>
          <h2>Quiz Completed</h2>
          <p>Your score is {score} out of {questions.length}.</p>
          <Button onClick={handleStartQuiz} className="retry-button">
            Retry
          </Button>
        </Card>
      ) : (
        <Card>
          <h2>
            Question {currentQuestion + 1}: {questions[currentQuestion].question}
          </h2>
          <div className="options-container">
            {questions[currentQuestion].options.map((option, index) => (
              <Button
                key={index}
                onClick={() => handleAnswerSelect(index)}
                disabled={showFeedback}
                className={getButtonStyles(index)}
              >
                {option}
              </Button>
            ))}
          </div>
          {showFeedback && (
            <Alert type={
              selectedAnswer === questions[currentQuestion].correctAnswer
                ? 'success'
                : 'error'
            }>
              {selectedAnswer === questions[currentQuestion].correctAnswer
                ? 'Correct!'
                : `Incorrect. The correct answer is "${questions[currentQuestion].options[questions[currentQuestion].correctAnswer]}".`}
            </Alert>
          )}
        </Card>
      )}

      <style jsx>{`
        .quiz-container {
          max-width: 600px;
          margin: 0 auto;
          padding: 20px;
        }

        .card {
          background: white;
          border: 1px solid #ddd;
          border-radius: 8px;
          padding: 20px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .button {
          padding: 10px 20px;
          border: none;
          border-radius: 4px;
          color: white;
          font-weight: 500;
          cursor: pointer;
          width: 100%;
          margin-bottom: 10px;
          transition: opacity 0.2s;
        }

        .button.disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .button.default {
          background-color: #3b82f6;
        }

        .button.correct {
          background-color: #22c55e;
        }

        .button.wrong {
          background-color: #ef4444;
        }

        .start-button, .retry-button {
          background-color: #3b82f6;
        }

        .alert {
          padding: 15px;
          border-radius: 4px;
          margin-top: 15px;
        }

        .alert.success {
          background-color: #dcfce7;
          color: #166534;
        }

        .alert.error {
          background-color: #fee2e2;
          color: #991b1b;
        }

        h2 {
          font-size: 1.25rem;
          font-weight: bold;
          margin-bottom: 20px;
        }

        p {
          margin-bottom: 20px;
        }

        .options-container {
          display: flex;
          flex-direction: column;
          gap: 10px;
        }
      `}</style>
    </div>
  );
};

export default Quiz;