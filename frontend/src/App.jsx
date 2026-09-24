import { Route, Routes } from "react-router-dom";

import CareerPrediction from "./pages/CareerPrediction";
import Dashboard from "./pages/Dashboard";
import Home from "./pages/Home";
import JobDescriptionAnalyzer from "./pages/JobDescriptionAnalyzer";
import Jobs from "./pages/Jobs";
import LearningRecommendations from "./pages/LearningRecommendations";
import Login from "./pages/Login";
import Profile from "./pages/Profile";
import Register from "./pages/Register";
import ResumeHistory from "./pages/ResumeHistory";
import ResumeImprovement from "./pages/ResumeImprovement";
import ResumeUpload from "./pages/ResumeUpload";
import SkillGap from "./pages/SkillGap";
import ResumeRewrite from "./pages/ResumeRewrite";

import ProtectedRoute from "./routes/ProtectedRoute";


function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={<Home />}
      />

      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/register"
        element={<Register />}
      />

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/resume"
        element={
          <ProtectedRoute>
            <ResumeUpload />
          </ProtectedRoute>
        }
      />

      <Route
        path="/resume-history"
        element={
          <ProtectedRoute>
            <ResumeHistory />
          </ProtectedRoute>
        }
      />

      <Route
        path="/career"
        element={
          <ProtectedRoute>
            <CareerPrediction />
          </ProtectedRoute>
        }
      />

      <Route
        path="/skill-gap"
        element={
          <ProtectedRoute>
            <SkillGap />
          </ProtectedRoute>
        }
      />

      <Route
        path="/jobs"
        element={
          <ProtectedRoute>
            <Jobs />
          </ProtectedRoute>
        }
      />

      <Route
        path="/learning"
        element={
          <ProtectedRoute>
            <LearningRecommendations />
          </ProtectedRoute>
        }
      />

      <Route
        path="/job-description-analyzer"
        element={
          <ProtectedRoute>
            <JobDescriptionAnalyzer />
          </ProtectedRoute>
        }
      />

      <Route
        path="/resume-improvement"
        element={
          <ProtectedRoute>
            <ResumeImprovement />
          </ProtectedRoute>
        }
      />
      <Route
        path="/resume-rewrite"
        element={
       <ProtectedRoute>
          <ResumeRewrite />
        </ProtectedRoute>
        }
      />

      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

export default App;