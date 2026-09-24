import "./Statistics.css";

import { motion } from "framer-motion";

import {
  FaBrain,
  FaChartLine,
  FaLayerGroup,
  FaTools
} from "react-icons/fa";

const highlights = [
  {
    icon: <FaBrain />,
    value: "6+",
    title: "Core Features",
    description:
      "Resume analysis, ATS scoring, career prediction, skill-gap analysis, job recommendations and reports."
  },
  {
    icon: <FaTools />,
    value: "20+",
    title: "Technical Skills",
    description:
      "The system can identify and compare multiple technical skills from uploaded resumes."
  },
  {
    icon: <FaLayerGroup />,
    value: "5",
    title: "Career Modules",
    description:
      "Resume, career prediction, skill gap, learning roadmap and job recommendation modules."
  },
  {
    icon: <FaChartLine />,
    value: "3+",
    title: "Analysis Categories",
    description:
      "Resume quality, career readiness and job suitability are analyzed separately."
  }
];

function Statistics() {
  return (
    <section
      className="statistics"
      id="statistics"
    >
      <div className="container">
        <motion.div
          className="statistics-header"
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
          <span className="statistics-tag">
            Project Highlights
          </span>

          <h2>
            Built around practical career analysis
          </h2>

          <p>
            These figures describe the capabilities currently
            included in CareerCompass, rather than estimated
            user or company statistics.
          </p>
        </motion.div>

        <div className="statistics-grid">
          {highlights.map((item, index) => (
            <motion.article
              className="statistics-card"
              key={item.title}
              initial={{
                opacity: 0,
                y: 30
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
              <div className="statistics-icon">
                {item.icon}
              </div>

              <p className="statistics-value">
                {item.value}
              </p>

              <h3>{item.title}</h3>

              <p className="statistics-description">
                {item.description}
              </p>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}

export default Statistics;