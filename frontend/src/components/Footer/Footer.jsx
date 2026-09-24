import "./Footer.css";

import { useNavigate } from "react-router-dom";

import {
  FaArrowRight,
  FaBriefcase,
  FaChartLine,
  FaFileAlt,
  FaGithub,
  FaGraduationCap,
  FaInstagram,
  FaLinkedin,
  FaRobot
} from "react-icons/fa";

import { MdEmail } from "react-icons/md";


const quickLinks = [
  {
    label: "Home",
    sectionId: "hero"
  },
  {
    label: "Features",
    sectionId: "features"
  },
  {
    label: "How It Works",
    sectionId: "process"
  },
  {
    label: "Project Highlights",
    sectionId: "statistics"
  }
];


const resourceLinks = [
  {
    label: "Resume Analysis",
    path: "/resume",
    icon: <FaFileAlt />
  },
  {
    label: "Career Prediction",
    path: "/career",
    icon: <FaChartLine />
  },
  {
    label: "Skill Gap Analysis",
    path: "/skill-gap",
    icon: <FaGraduationCap />
  },
  {
    label: "Job Recommendations",
    path: "/jobs",
    icon: <FaBriefcase />
  }
];


function Footer() {
  const navigate = useNavigate();


  const scrollToSection = (sectionId) => {
    const section =
      document.getElementById(sectionId);

    if (section) {
      section.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });
    }
  };


  const handleResourceNavigation = (path) => {
    const token =
      localStorage.getItem("token");

    if (!token) {
      navigate("/login");
      return;
    }

    navigate(path);
  };


  return (
    <footer
      className="footer"
      id="footer"
    >
      <div className="footer-glow" />

      <div className="container footer-container">

        <div className="footer-grid">

          {/* Brand */}
          <section className="footer-brand">
            <button
              type="button"
              className="footer-logo"
              onClick={() =>
                scrollToSection("hero")
              }
              aria-label="Go to the top of the page"
            >
              <span className="footer-logo-icon">
                <FaRobot />
              </span>

              <span>
                CareerCompass
                <strong> AI</strong>
              </span>
            </button>

            <p>
              A career-development platform that helps
              students analyze resumes, discover suitable
              career paths, identify skill gaps and prepare
              for better job opportunities.
            </p>

            <div className="footer-auth-buttons">
              <button
                type="button"
                className="footer-login-button"
                onClick={() =>
                  navigate("/login")
                }
              >
                Login
              </button>

              <button
                type="button"
                className="footer-register-button"
                onClick={() =>
                  navigate("/register")
                }
              >
                Get Started
                <FaArrowRight />
              </button>
            </div>
          </section>


          {/* Quick links */}
          <section className="footer-column">
            <h3>Quick Links</h3>

            <ul>
              {quickLinks.map((link) => (
                <li key={link.sectionId}>
                  <button
                    type="button"
                    onClick={() =>
                      scrollToSection(
                        link.sectionId
                      )
                    }
                  >
                    {link.label}
                  </button>
                </li>
              ))}
            </ul>
          </section>


          {/* Resources */}
          <section className="footer-column footer-resources">
            <h3>Career Tools</h3>

            <ul>
              {resourceLinks.map((link) => (
                <li key={link.path}>
                  <button
                    type="button"
                    onClick={() =>
                      handleResourceNavigation(
                        link.path
                      )
                    }
                  >
                    <span className="footer-resource-icon">
                      {link.icon}
                    </span>

                    {link.label}
                  </button>
                </li>
              ))}
            </ul>
          </section>


          {/* Connect */}
          <section className="footer-column">
            <h3>Connect</h3>

            <p className="footer-connect-text">
              Follow the project journey and stay connected.
            </p>

            <div className="socials">
              <button
                type="button"
                aria-label="GitHub"
                title="GitHub"
              >
                <FaGithub />
              </button>

              <button
                type="button"
                aria-label="LinkedIn"
                title="LinkedIn"
              >
                <FaLinkedin />
              </button>

              <button
                type="button"
                aria-label="Instagram"
                title="Instagram"
              >
                <FaInstagram />
              </button>

              <button
                type="button"
                aria-label="Email"
                title="Email"
              >
                <MdEmail />
              </button>
            </div>
          </section>
        </div>


        <div className="footer-bottom">
          <p>
            © 2026 CareerCompass AI. Built as a major project
            using React and FastAPI.
          </p>

          <div className="footer-bottom-links">
            <button
              type="button"
              onClick={() =>
                scrollToSection("features")
              }
            >
              Features
            </button>

            <button
              type="button"
              onClick={() =>
                scrollToSection("process")
              }
            >
              How It Works
            </button>

            <button
              type="button"
              onClick={() =>
                navigate("/login")
              }
            >
              Login
            </button>
          </div>
        </div>
      </div>
    </footer>
  );
}


export default Footer;