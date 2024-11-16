import React, { useState } from 'react';

const styles = `
  .navbar {
    position: fixed;
    top: 0;
    width: 100%;
    background-color: rgba(37, 99, 235, 0.9);
    backdrop-filter: blur(8px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .navbar-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
  }

  .navbar-content {
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 16px;
  }

  .login-button {
    padding: 8px 24px;
    background-color: white;
    color: rgb(37, 99, 235);
    border: none;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .login-button:hover {
    background-color: #f8fafc;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .signup-button {
    padding: 8px 24px;
    background-color: transparent;
    color: white;
    border: 2px solid white;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }

  .signup-button:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }

  .modal-overlay {
    position: fixed;
    inset: 0;
    background-color: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .modal {
    background-color: white;
    padding: 32px;
    border-radius: 12px;
    width: 384px;
    position: relative;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .modal h2 {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 24px;
    color: #1f2937;
  }

  .form-group {
    margin-bottom: 20px;
  }

  .form-label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 8px;
    color: #4b5563;
  }

  .form-input {
    width: 100%;
    padding: 12px;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    outline: none;
    transition: all 0.2s;
  }

  .form-input:focus {
    border-color: rgb(37, 99, 235);
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
  }

  .submit-button {
    width: 100%;
    padding: 12px;
    background-color: rgb(37, 99, 235);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    margin-top: 8px;
  }

  .submit-button:hover {
    background-color: rgb(29, 78, 216);
  }

  .close-button {
    position: absolute;
    top: 16px;
    right: 16px;
    background: none;
    border: none;
    color: #9ca3af;
    font-size: 24px;
    cursor: pointer;
    transition: color 0.2s;
  }

  .close-button:hover {
    color: #4b5563;
  }
`;

const SignIn = ({ onClose }) => {
  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>Welcome Back</h2>
        <form>
          <div className="form-group">
            <label className="form-label">Email</label>
            <input 
              type="email" 
              className="form-input"
              placeholder="Enter your email"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input 
              type="password" 
              className="form-input"
              placeholder="Enter your password"
            />
          </div>
          <button type="submit" className="submit-button">Sign In</button>
        </form>
        <button onClick={onClose} className="close-button">×</button>
      </div>
    </div>
  );
};

const SignUp = ({ onClose }) => {
  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>Create Account</h2>
        <form>
          <div className="form-group">
            <label className="form-label">Full Name</label>
            <input 
              type="text" 
              className="form-input"
              placeholder="Enter your name"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Email</label>
            <input 
              type="email" 
              className="form-input"
              placeholder="Enter your email"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input 
              type="password" 
              className="form-input"
              placeholder="Choose a password"
            />
          </div>
          <button type="submit" className="submit-button">Create Account</button>
        </form>
        <button onClick={onClose} className="close-button">×</button>
      </div>
    </div>
  );
};

const Navbar = () => {
  const [showSignIn, setShowSignIn] = useState(false);
  const [showSignUp, setShowSignUp] = useState(false);

  return (
    <>
      <style>{styles}</style>
      <nav className="navbar">
        <div className="navbar-container">
          <div className="navbar-content">
            <button 
              onClick={() => setShowSignIn(true)}
              className="login-button"
            >
              Login
            </button>
            <button 
              onClick={() => setShowSignUp(true)}
              className="signup-button"
            >
              Sign Up
            </button>
          </div>
        </div>
      </nav>

      {showSignIn && <SignIn onClose={() => setShowSignIn(false)} />}
      {showSignUp && <SignUp onClose={() => setShowSignUp(false)} />}
    </>
  );
};

export default Navbar;