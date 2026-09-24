import "./HowItWorks.css";

import { motion } from "framer-motion";

import {
  FaChartLine,
  FaFileDownload,
  FaGraduationCap,
  FaRobot,
  FaUpload
} from "react-icons/fa";


const steps = [
  {
    icon: <FaUpload />,
    title: "Upload Resume",
    description:
      "Upload your PDF or DOCX resume securely for analysis."
  },
  {
    icon: <FaRobot />,
    title: "AI Resume Analysis",
    description:
      "The system extracts your skills, education, experience and projects."
  },
  {
    icon: <FaChartLine />,
    title: "Career Prediction",
    description:
      "Your resume skills are compared with suitable career paths."
  },
  {
    icon: <FaGraduationCap />,
    title: "Learning Roadmap",
    description:
      "Receive recommendations for improving your missing career skills."
  },
  {
    icon: <FaFileDownload />,
    title: "Career Report",
    description:
      "Download a detailed report containing your complete career analysis."
  }
];


function HowItWorks() {
  return (
    <section
      className="process"
      id="process"
    >
      <div className="container">
        <motion.div
          className="process-header"
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
            amount: 0.3
          }}
        >
          <span className="process-tag">
            How It Works
          </span>

          <h2>
            How CareerCompass works
          </h2>

          <p>
            From resume upload to career recommendations,
            CareerCompass guides you through a simple and
            practical career-development process.
          </p>
        </motion.div>


        <div className="timeline">
          <div className="timeline-progress" />

          {steps.map((step, index) => (
            <motion.article
              className="timeline-item"
              key={step.title}
              initial={{
                opacity: 0,
                y: 45
              }}
              whileInView={{
                opacity: 1,
                y: 0
              }}
              transition={{
                duration: 0.5,
                delay: index * 0.1
              }}
              viewport={{
                once: true,
                amount: 0.25
              }}
            >
              <div className="timeline-step">
                {String(index + 1).padStart(2, "0")}
              </div>

              <div className="timeline-icon">
                {step.icon}
              </div>

              <div className="timeline-content">
                <h3>{step.title}</h3>

                <p>{step.description}</p>
              </div>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}


export default HowItWorks;