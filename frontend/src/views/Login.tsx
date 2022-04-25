import React, { FC, useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';

import { login, isAuthenticated } from '../utils/auth';


export const Login: FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState<string>('mail@gmail.com');
  const [password, setPassword] = useState<string>('1234567890@@');
  const [error, setError] = useState<string>('');

  const handleSubmit = async (_: React.MouseEvent) => {
    setError('');
    try {
      const data = await login(email, password);

      if (data) {
        navigate('/');
      }
    } catch (err) {
      if (err instanceof Error) {
        // handle errors thrown from frontend
        setError(err.message);
      } else {
        // handle errors thrown from backend
        setError(String(err));
      }
    }
  };

  return isAuthenticated() ? (
    <Navigate to="/" />
  ) : (
      <div>
        <div>
          <div>
            <button onClick={handleSubmit}>Login</button>
        </div>
      </div>
    </div>
  );
};
