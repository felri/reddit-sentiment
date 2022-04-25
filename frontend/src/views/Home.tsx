import React, { FC, useEffect, useState } from "react";

import { get } from "../utils/api";
import { isAuthenticated } from "../utils/auth";

export const Home: FC = () => {
  const [message, setMessage] = useState<string>("");
  const [error, setError] = useState<string>("");

  useEffect(() => {
    console.log("oi");
  }, []);

  const queryBackend = async () => {
    try {
      const message = await get("/api/hello", {});
      setMessage(message);
    } catch (err) {
      setError(String(err));
    }
  };

  return (
    <>
      {!message && !error && (
        <a href="#" onClick={() => queryBackend()}>
          Click to make request to backend
        </a>
      )}
      {message && (
        <p>
          <code>{message}</code>
        </p>
      )}
      {error && (
        <p>
          Error: <code>{error}</code>
        </p>
      )}
      <a href="/admin">Admin Dashboard</a>
      <a href="/protected">Protected Route</a>
      {isAuthenticated() ? (
        <a href="/logout">Logout</a>
      ) : (
        <>
          <a href="/login">Login</a>
          <a href="/signup">Sign Up</a>
        </>
      )}
    </>
  );
};
