import "./Features.css";

import { motion } from "framer-motion";

import {
  FaBrain,
  FaBriefcase,
  FaChartLine,
  FaFileAlt,
  FaGraduationCap,
  FaUserTie
} from "react-icons/fa";


const features = [
  {
    icon: <FaFileAlt />,
    title: "Resume Analysis",
    description:
      "Upload your resume and let AI extract your skills, education, projects and experience automatically."
  },
  {
    icon: <FaUserTie />,
    title: "Career Prediction",
    description:
      "Discover suitable career paths based on the skills and experience found in your resume."
  },
  {
    icon: <FaChartLine />,
    title: "ATS Score",
    description:
      "Check how well your resume performs against modern Applicant Tracking Systems."
  },
  {
    icon: <FaGraduationCap />,
    title: "Learning Roadmap",
    description:
      "Receive personalized learning recommendations to improve your career readiness."
  },
  {
    icon: <FaBrain />,
    title: "Skill Gap Analysis",
    description:
      "Compare your current skills with career requirements and identify the skills you should improve."
  },
  {
    icon: <FaBriefcase />,
    title: "Job Recommendations",
    description:
      "Explore suitable internships and job roles that match your current skills and career profile."
  }
];


function Features() {
  return (
    <section
      className="features"
      id="features"
    >
      <div className="container">
        <motion.div
          className="section-header"
          initial={{
            opacity: 0,
            y: 35
          }}
          whileInView={{
            opacity: 1,
            y: 0
          }}
          transition={{
            duration: 0.6
          }}
          viewport={{
            once: true,
            amount: 0.25
          }}
        >
          <span className="section-tag">
            Powerful Features
          </span>

          <h2>
            Everything you need to build your career
          </h2>

          <p>
            CareerCompass helps you analyze your resume,
            discover suitable career paths, identify missing
            skills and prepare for better opportunities.
          </p>
        </motion.div>


        <div className="feature-grid">
          {features.map((feature, index) => (
            <motion.article
              className="feature-card"
              key={feature.title}
              initial={{
                opacity: 0,
                y: 32
              }}
              whileInView={{
                opacity: 1,
                y: 0
              }}
              transition={{
                duration: 0.5,
                delay: index * 0.08
              }}
              viewport={{
                once: true,
                amount: 0.2
              }}
            >
              <div className="feature-card-top">
                <div className="feature-icon">
                  {feature.icon}
                </div>

                <span className="feature-number">
                  {String(index + 1).padStart(2, "0")}
                </span>
              </div>

              <h3>{feature.title}</h3>

              <p>{feature.description}</p>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}


export default Features;