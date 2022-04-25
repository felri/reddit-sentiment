import React, { FC, useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";

import { signUp, isAuthenticated } from "../utils/auth";

export const SignUp: FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState<string>("mail@gmail.com");
  const [password, setPassword] = useState<string>("1234567890@@");
  const [passwordConfirmation, setPasswordConfirmation] =
    useState<string>("1234567890@@");
  const [error, setError] = useState<string>("");

  const handleSubmit = async (_: React.MouseEvent) => {
    // Password confirmation validation
    if (password !== passwordConfirmation) setError("Passwords do not match");
    else {
      setError("");
      try {
        const data = await signUp(email, password, passwordConfirmation);

        if (data) {
          navigate("/");
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
    }
  };

  return isAuthenticated() ? (
    <Navigate to="/" />
  ) : (
    <div>
      <button onClick={handleSubmit}>Sign Up</button>
    </div>
  );
};
