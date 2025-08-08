// src/routes/AppRouter.tsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "../pages/App";
import Login from "../pages/Login";
import GitHubCallback from "../components/GithubCallback";

const AppRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/home" element={<Home />} />
        <Route path="/" element={<Login />} />
        <Route path="/github-callback" element={<GitHubCallback />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;
