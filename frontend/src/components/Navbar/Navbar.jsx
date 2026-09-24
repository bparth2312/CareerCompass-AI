import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { FaRobot } from "react-icons/fa";
import {
  HiOutlineMenuAlt3,
  HiOutlineX
} from "react-icons/hi";

import ThemeToggle from "../ThemeToggle/ThemeToggle";
import "./Navbar.css";


const navigationItems = [
  {
    id: "hero",
    label: "Home"
  },
  {
    id: "features",
    label: "Features"
  },
  {
    id: "process",
    label: "How It Works"
  },
  {
    id: "statistics",
    label: "Statistics"
  },
  {
    id: "footer",
    label: "Contact"
  }
];


function Navbar() {
  const [menuOpen, setMenuOpen] =
    useState(false);

  const [isScrolled, setIsScrolled] =
    useState(false);

  const [activeSection, setActiveSection] =
    useState("hero");


  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);

      const scrollPosition =
        window.scrollY + 140;

      let currentSection = "hero";

      navigationItems.forEach((item) => {
        const section =
          document.getElementById(item.id);

        if (
          section &&
          section.offsetTop <= scrollPosition
        ) {
          currentSection = item.id;
        }
      });

      setActiveSection(currentSection);
    };

    handleScroll();

    window.addEventListener(
      "scroll",
      handleScroll,
      {
        passive: true
      }
    );

    return () => {
      window.removeEventListener(
        "scroll",
        handleScroll
      );
    };
  }, []);


  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 900) {
        setMenuOpen(false);
      }
    };

    window.addEventListener(
      "resize",
      handleResize
    );

    return () => {
      window.removeEventListener(
        "resize",
        handleResize
      );
    };
  }, []);


  useEffect(() => {
    document.body.style.overflow =
      menuOpen ? "hidden" : "";

    return () => {
      document.body.style.overflow = "";
    };
  }, [menuOpen]);


  const handleNavigation = (
    event,
    sectionId
  ) => {
    event.preventDefault();

    const section =
      document.getElementById(sectionId);

    if (section) {
      section.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });

      setActiveSection(sectionId);
    }

    setMenuOpen(false);
  };


  const closeMenu = () => {
    setMenuOpen(false);
  };


  return (
    <nav
      className={`
        navbar
        ${isScrolled ? "navbar-scrolled" : ""}
      `}
    >
      <div className="nav-container">

        {/* Logo */}
        <Link
          to="/"
          className="logo"
          onClick={closeMenu}
          aria-label="CareerCompass home"
        >
          <span className="logo-icon-wrapper">
            <FaRobot className="logo-icon" />
          </span>

          <span className="logo-text">
            CareerCompass
            <span className="logo-ai">
              AI
            </span>
          </span>
        </Link>


        {/* Desktop and mobile navigation */}
        <ul
          className={`
            nav-links
            ${menuOpen ? "active" : ""}
          `}
        >
          {navigationItems.map((item) => (
            <li key={item.id}>
              <a
                href={`#${item.id}`}
                onClick={(event) =>
                  handleNavigation(
                    event,
                    item.id
                  )
                }
                className={
                  activeSection === item.id
                    ? "active-link"
                    : ""
                }
              >
                {item.label}
              </a>
            </li>
          ))}


          {/* Mobile-only account actions */}
          <li className="mobile-nav-actions">
            <div className="mobile-theme-row">
              <span>Appearance</span>
              <ThemeToggle />
            </div>

            <Link
              to="/login"
              className="login-btn"
              onClick={closeMenu}
            >
              Login
            </Link>

            <Link
              to="/register"
              className="register-btn"
              onClick={closeMenu}
            >
              Register
            </Link>
          </li>
        </ul>


        {/* Desktop right-side buttons */}
        <div className="nav-buttons">
          <ThemeToggle />

          <Link
            to="/login"
            className="login-btn"
          >
            Login
          </Link>

          <Link
            to="/register"
            className="register-btn"
          >
            Register
          </Link>
        </div>


        {/* Mobile menu button */}
        <button
          type="button"
          className="menu-btn"
          onClick={() =>
            setMenuOpen(
              (currentValue) =>
                !currentValue
            )
          }
          aria-label={
            menuOpen
              ? "Close navigation menu"
              : "Open navigation menu"
          }
          aria-expanded={menuOpen}
        >
          {menuOpen ? (
            <HiOutlineX size={28} />
          ) : (
            <HiOutlineMenuAlt3 size={28} />
          )}
        </button>
      </div>


      {menuOpen && (
        <button
          type="button"
          className="navbar-overlay"
          onClick={closeMenu}
          aria-label="Close navigation menu"
        />
      )}
    </nav>
  );
}


export default Navbar;