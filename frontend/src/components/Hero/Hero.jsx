import "./Hero.css";

import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

import {
  FaArrowRight,
  FaBookOpen,
  FaBriefcase,
  FaChartLine,
  FaCheckCircle,
  FaUpload
} from "react-icons/fa";


function Hero() {
  const navigate = useNavigate();

  const goToResumeUpload = () => {
    navigate("/resume");
  };

  return (
    <section
      className="hero"
      id="hero"
    >
      <div className="hero-background-grid" />

      <div className="hero-glow hero-glow-one" />
      <div className="hero-glow hero-glow-two" />

      <div className="container hero-container">

        {/* Left section */}
        <motion.div
          className="hero-left"
          initial={{
            opacity: 0,
            x: -60
          }}
          animate={{
            opacity: 1,
            x: 0
          }}
          transition={{
            duration: 0.75,
            ease: "easeOut"
          }}
        >
          <motion.span
            className="hero-badge"
            initial={{
              opacity: 0,
              y: 12
            }}
            animate={{
              opacity: 1,
              y: 0
            }}
            transition={{
              delay: 0.15,
              duration: 0.5
            }}
          >
            🚀 AI Powered Career Guidance
          </motion.span>

          <h1>
            Discover Your
            <span> Dream Career </span>
            Using Artificial Intelligence
          </h1>

          <p className="hero-description">
            Upload your resume and receive personalized
            insights about your skills, suitable careers,
            skill gaps, learning resources and job
            opportunities.
          </p>

          <div className="hero-buttons">
            <button
              type="button"
              className="primary-btn"
              onClick={goToResumeUpload}
            >
              Get Started
              <FaArrowRight />
            </button>
          </div>

          <div className="hero-stats">
            <HeroStatistic
              value="25K+"
              label="Students"
            />

            <HeroStatistic
              value="500+"
              label="Companies"
            />

            <HeroStatistic
              value="98%"
              label="Accuracy"
            />
          </div>
        </motion.div>


        {/* Right section */}
        <motion.div
          className="hero-right"
          initial={{
            opacity: 0,
            x: 60
          }}
          animate={{
            opacity: 1,
            x: 0
          }}
          transition={{
            duration: 0.75,
            ease: "easeOut"
          }}
        >
          <div className="dashboard-card-wrapper">
            <div className="dashboard-card-glow" />

            <motion.div
              className="dashboard-card"
              animate={{
                y: [0, -8, 0]
              }}
              transition={{
                duration: 5,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            >
              <div className="dashboard-header">
                <div>
                  <span className="dashboard-label">
                    Resume overview
                  </span>

                  <h2>
                    Resume Analysis
                  </h2>
                </div>

                <div className="verified-wrapper">
                  <FaCheckCircle className="verified" />
                </div>
              </div>


              <div className="ats-progress-section">
                <div className="ats-progress-heading">
                  <span>ATS Score</span>
                  <strong>94%</strong>
                </div>

                <div className="ats-progress-track">
                  <motion.div
                    className="ats-progress-value"
                    initial={{
                      width: 0
                    }}
                    animate={{
                      width: "94%"
                    }}
                    transition={{
                      delay: 0.5,
                      duration: 1.2,
                      ease: "easeOut"
                    }}
                  />
                </div>
              </div>


              <div className="analysis">
                <AnalysisRow
                  label="Career"
                  value="Data Scientist"
                />

                <AnalysisRow
                  label="Skills Detected"
                  value="14"
                />

                <AnalysisRow
                  label="Missing Skills"
                  value="4"
                />
              </div>


              <div className="dashboard-grid">
                <MiniCard
                  icon={<FaChartLine />}
                  value="96%"
                  label="Career Match"
                />

                <MiniCard
                  icon={<FaBookOpen />}
                  value="18"
                  label="Courses"
                />

                <MiniCard
                  icon={<FaBriefcase />}
                  value="48"
                  label="Jobs"
                />
              </div>


              <button
                type="button"
                className="resume-upload-btn"
                onClick={goToResumeUpload}
              >
                <FaUpload />
                Upload Your Resume
              </button>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}


function HeroStatistic({
  value,
  label
}) {
  return (
    <div className="hero-stat-item">
      <h2>{value}</h2>
      <span>{label}</span>
    </div>
  );
}


function AnalysisRow({
  label,
  value
}) {
  return (
    <div className="analysis-row">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}


function MiniCard({
  icon,
  value,
  label
}) {
  return (
    <div className="mini-card">
      <div className="mini-card-icon">
        {icon}
      </div>

      <h3>{value}</h3>
      <span>{label}</span>
    </div>
  );
}


export default Hero;