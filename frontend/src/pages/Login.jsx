import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaBriefcase,
  FaChartLine,
  FaEnvelope,
  FaEye,
  FaEyeSlash,
  FaGraduationCap,
  FaLock,
  FaUserCheck
} from "react-icons/fa";

import ThemeToggle from "../components/ThemeToggle/ThemeToggle";
import { loginUser } from "../services/authService";


const getErrorMessage = (error) => {
  const detail = error.response?.data?.detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) => item?.msg || "Validation error")
      .join(", ");
  }

  if (error.message === "Network Error") {
    return (
      "Unable to connect to the backend. " +
      "Make sure FastAPI is running."
    );
  }

  return (
    error.message ||
    "Invalid email or password. Please try again."
  );
};


function Login() {
  const navigate = useNavigate();

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [showPassword, setShowPassword] =
    useState(false);

  const [rememberMe, setRememberMe] =
    useState(false);

  const [isLoading, setIsLoading] =
    useState(false);

  const [errorMessage, setErrorMessage] =
    useState("");


  useEffect(() => {
    const savedEmail = localStorage.getItem(
      "careercompass-email"
    );

    if (savedEmail) {
      setEmail(savedEmail);
      setRememberMe(true);
    }

    const searchParams = new URLSearchParams(
      window.location.search
    );

    if (searchParams.get("session") === "expired") {
      setErrorMessage(
        "Your login session expired. Please log in again."
      );
    }
  }, []);


  const handleLogin = async (event) => {
    event.preventDefault();

    setErrorMessage("");

    const cleanedEmail =
      email.trim().toLowerCase();

    if (!cleanedEmail || !password) {
      setErrorMessage(
        "Please enter your email and password."
      );

      return;
    }

    setIsLoading(true);

    try {
      localStorage.removeItem("token");

      const data = await loginUser(
        cleanedEmail,
        password
      );

      if (!data?.access_token) {
        throw new Error(
          "Access token was not returned by the server."
        );
      }

      localStorage.setItem(
        "token",
        String(data.access_token).trim()
      );

      localStorage.setItem(
        "token_type",
        data.token_type || "bearer"
      );

      const storedToken =
        localStorage.getItem("token");

      if (!storedToken) {
        throw new Error(
          "The login token could not be saved in the browser."
        );
      }

      if (rememberMe) {
        localStorage.setItem(
          "careercompass-email",
          cleanedEmail
        );
      } else {
        localStorage.removeItem(
          "careercompass-email"
        );
      }

      const searchParams = new URLSearchParams(
        window.location.search
      );

      const returnTo =
        searchParams.get("returnTo");

      navigate(
        returnTo || "/dashboard",
        { replace: true }
      );
    } catch (error) {
      console.error(
        "Login error:",
        error
      );

      setErrorMessage(
        getErrorMessage(error)
      );
    } finally {
      setIsLoading(false);
    }
  };


  return (
    <main className="app-page">
      <div className="
        min-h-screen
        lg:grid
        lg:grid-cols-[1.05fr_0.95fr]
      ">

        {/* Left information section */}
        <section className="
          relative hidden
          overflow-hidden
          border-r border-[var(--border)]
          bg-[var(--surface-soft)]
          p-12
          lg:flex
          lg:flex-col
          lg:justify-between
          xl:p-16
        ">
          <div className="
            absolute -left-24 -top-24
            h-80 w-80
            rounded-full
            bg-[var(--primary-soft)]
            blur-3xl
          " />

          <div className="
            absolute -bottom-32 -right-24
            h-96 w-96
            rounded-full
            bg-[var(--accent-soft)]
            blur-3xl
          " />

          <div className="relative">
            <div className="
              flex items-center gap-3
            ">
              <div className="
                flex h-12 w-12
                items-center justify-center
                rounded-2xl
                bg-[var(--primary)]
                text-xl
                text-white
                dark:text-[#06221f]
              ">
                <FaGraduationCap />
              </div>

              <div>
                <p className="
                  text-xl font-bold
                  text-[var(--text-primary)]
                ">
                  CareerCompass
                </p>

                <p className="
                  text-sm
                  text-[var(--text-muted)]
                ">
                  Personal Career Development Platform
                </p>
              </div>
            </div>

            <div className="mt-16 max-w-xl">
              <span className="badge badge-primary">
                <FaUserCheck />
                Personalized career guidance
              </span>

              <h1 className="
                mt-6
                text-4xl font-bold
                leading-tight
                tracking-[-0.04em]
                text-[var(--text-primary)]
                xl:text-5xl
              ">
                Make confident decisions about your career.
              </h1>

              <p className="
                mt-6
                text-lg leading-8
                text-[var(--text-secondary)]
              ">
                Analyze your resume, understand your
                strengths, identify missing skills and
                discover career opportunities that match
                your profile.
              </p>
            </div>

            <div className="
              mt-12 grid gap-4
              sm:grid-cols-2
            ">
              <FeatureItem
                icon={<FaChartLine />}
                title="ATS Analysis"
                description="Measure resume quality and identify improvements."
              />

              <FeatureItem
                icon={<FaGraduationCap />}
                title="Skill Gap"
                description="Understand what skills you should learn next."
              />

              <FeatureItem
                icon={<FaBriefcase />}
                title="Career Matches"
                description="Discover suitable roles based on your profile."
              />

              <FeatureItem
                icon={<FaUserCheck />}
                title="Personalized Guidance"
                description="Receive recommendations based on your resume."
              />
            </div>
          </div>

          <p className="
            relative mt-10
            text-sm
            text-[var(--text-muted)]
          ">
            CareerCompass helps students and professionals
            build practical career plans.
          </p>
        </section>


        {/* Login form section */}
        <section className="
          flex min-h-screen
          items-center justify-center
          px-5 py-10
          sm:px-8
          lg:px-12
        ">
          <div className="
            w-full max-w-[500px]
          ">
            <div className="
              mb-7
              flex items-center
              justify-between
              lg:justify-end
            ">
              <div className="
                flex items-center gap-3
                lg:hidden
              ">
                <div className="
                  flex h-10 w-10
                  items-center justify-center
                  rounded-xl
                  bg-[var(--primary-soft)]
                  text-[var(--primary)]
                ">
                  <FaGraduationCap />
                </div>

                <span className="
                  font-bold
                  text-[var(--text-primary)]
                ">
                  CareerCompass
                </span>
              </div>

              <ThemeToggle />
            </div>

            <div className="
              app-card
              p-6
              sm:p-8
              lg:p-10
            ">
              <div>
                <span className="badge badge-primary">
                  Welcome back
                </span>

                <h1 className="
                  mt-5
                  text-3xl font-bold
                  tracking-tight
                  text-[var(--text-primary)]
                ">
                  Login to your account
                </h1>

                <p className="
                  mt-3
                  leading-7
                  text-[var(--text-secondary)]
                ">
                  Continue your resume analysis and career
                  development journey.
                </p>
              </div>


              {errorMessage && (
                <div className="
                  mt-6 rounded-2xl
                  border border-red-300
                  bg-red-50 p-4
                  text-sm text-red-800

                  dark:border-red-900/70
                  dark:bg-red-950/30
                  dark:text-red-300
                ">
                  {errorMessage}
                </div>
              )}


              <form
                onSubmit={handleLogin}
                className="mt-7 space-y-5"
              >
                <div className="form-group">
                  <label
                    htmlFor="email"
                    className="form-label"
                  >
                    Email Address
                  </label>

                  <div className="relative">
                    <FaEnvelope className="
                      pointer-events-none
                      absolute left-4 top-1/2
                      z-10 -translate-y-1/2
                      text-[var(--text-muted)]
                    " />

                    <input
                      id="email"
                      name="email"
                      type="email"
                      placeholder="Enter your email"
                      value={email}
                      onChange={(event) =>
                        setEmail(event.target.value)
                      }
                      autoComplete="email"
                      required
                      className="form-input"
                      style={{
                        paddingLeft: "2.9rem"
                      }}
                    />
                  </div>
                </div>


                <div className="form-group">
                  <div className="
                    flex items-center
                    justify-between gap-3
                  ">
                    <label
                      htmlFor="password"
                      className="form-label"
                    >
                      Password
                    </label>

                    <button
                      type="button"
                      className="
                        text-sm font-semibold
                        text-[var(--primary)]
                        hover:underline
                      "
                      onClick={() => {
                        setErrorMessage(
                          "Password recovery will be added later."
                        );
                      }}
                    >
                      Forgot password?
                    </button>
                  </div>

                  <div className="relative">
                    <FaLock className="
                      pointer-events-none
                      absolute left-4 top-1/2
                      z-10 -translate-y-1/2
                      text-[var(--text-muted)]
                    " />

                    <input
                      id="password"
                      name="password"
                      type={
                        showPassword
                          ? "text"
                          : "password"
                      }
                      placeholder="Enter your password"
                      value={password}
                      onChange={(event) =>
                        setPassword(
                          event.target.value
                        )
                      }
                      autoComplete="current-password"
                      required
                      className="form-input"
                      style={{
                        paddingLeft: "2.9rem",
                        paddingRight: "3rem"
                      }}
                    />

                    <button
                      type="button"
                      onClick={() =>
                        setShowPassword(
                          (current) => !current
                        )
                      }
                      aria-label={
                        showPassword
                          ? "Hide password"
                          : "Show password"
                      }
                      className="
                        absolute right-4 top-1/2
                        -translate-y-1/2
                        text-[var(--text-muted)]
                        hover:text-[var(--primary)]
                      "
                    >
                      {showPassword
                        ? <FaEyeSlash />
                        : <FaEye />}
                    </button>
                  </div>
                </div>


                <label className="
                  flex cursor-pointer
                  items-center gap-3
                  text-sm
                  text-[var(--text-secondary)]
                ">
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(event) =>
                      setRememberMe(
                        event.target.checked
                      )
                    }
                    className="
                      h-4 w-4
                      rounded
                      accent-[var(--primary)]
                    "
                  />

                  Remember my email
                </label>


                <button
                  type="submit"
                  disabled={isLoading}
                  className="
                    btn-primary
                    w-full py-4
                    disabled:cursor-not-allowed
                    disabled:opacity-60
                  "
                >
                  {isLoading ? (
                    <>
                      <span className="
                        h-5 w-5
                        animate-spin
                        rounded-full
                        border-2
                        border-white/40
                        border-t-white
                        dark:border-[#06221f]/30
                        dark:border-t-[#06221f]
                      " />

                      Logging in...
                    </>
                  ) : (
                    "Login"
                  )}
                </button>
              </form>


              <p className="
                mt-7 text-center
                text-[var(--text-secondary)]
              ">
                Don&apos;t have an account?{" "}
                <button
                  type="button"
                  onClick={() =>
                    navigate("/register")
                  }
                  className="
                    font-semibold
                    text-[var(--primary)]
                    hover:underline
                  "
                >
                  Create Account
                </button>
              </p>
            </div>

            <p className="
              mt-6 text-center
              text-xs
              text-[var(--text-muted)]
            ">
              By continuing, you agree to use the platform
              responsibly and keep your account information
              secure.
            </p>
          </div>
        </section>
      </div>
    </main>
  );
}


function FeatureItem({
  icon,
  title,
  description
}) {
  return (
    <article className="
      rounded-2xl
      border border-[var(--border)]
      bg-[var(--surface)]
      p-5
      shadow-[var(--shadow-sm)]
    ">
      <div className="
        flex h-11 w-11
        items-center justify-center
        rounded-xl
        bg-[var(--primary-soft)]
        text-lg
        text-[var(--primary)]
      ">
        {icon}
      </div>

      <h2 className="
        mt-4 font-bold
        text-[var(--text-primary)]
      ">
        {title}
      </h2>

      <p className="
        mt-2 text-sm leading-6
        text-[var(--text-secondary)]
      ">
        {description}
      </p>
    </article>
  );
}


export default Login;