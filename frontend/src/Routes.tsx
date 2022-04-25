import React, { FC, useEffect } from "react";
import { Routes as Switch, Route, useNavigate } from "react-router-dom";

import { Home, Login, SignUp, Protected } from "./views";
import { Admin } from "./admin";
import { logout, isAuthenticated } from "./utils/auth";

const Logout: FC = () => {
  const navigate = useNavigate();
  useEffect(() => {
    logout();
    navigate("/");
  }, []);
  return null;
};

export const Routes: FC = () => {
  return (
    <Switch>
      <Route path="/" element={<Home />} />
      {isAuthenticated() ? (
        <>
          <Route path="/logout" element={<Logout />} />
          <Route path="/protected" element={<Protected />} />
          <Route path="/admin" element={<Admin />} />
        </>
      ) : (
        <>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
        </>
      )}
      <Route path="*" element={<div>404</div>} />
    </Switch>
  );
};
