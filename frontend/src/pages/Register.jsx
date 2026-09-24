import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaBriefcase,
  FaChartLine,
  FaCheck,
  FaEnvelope,
  FaEye,
  FaEyeSlash,
  FaGraduationCap,
  FaLock,
  FaTimes,
  FaUser,
  FaUserCheck
} from "react-icons/fa";

import ThemeToggle from "../components/ThemeToggle/ThemeToggle";
import { registerUser } from "../services/authService";


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
    "Registration failed. Please try again."
  );
};


function Register() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    password: "",
    confirmPassword: ""
  });

  const [showPassword, setShowPassword] =
    useState(false);

  const [
    showConfirmPassword,
    setShowConfirmPassword
  ] = useState(false);

  const [isLoading, setIsLoading] =
    useState(false);

  const [errorMessage, setErrorMessage] =
    useState("");

  const [successMessage, setSuccessMessage] =
    useState("");


  const passwordChecks = useMemo(() => {
    const password = formData.password;

    return {
      length: password.length >= 8,
      uppercase: /[A-Z]/.test(password),
      lowercase: /[a-z]/.test(password),
      number: /\d/.test(password),
      special: /[^A-Za-z0-9]/.test(password)
    };
  }, [formData.password]);


  const passwordStrength = useMemo(() => {
    const completedChecks =
      Object.values(passwordChecks)
        .filter(Boolean)
        .length;

    if (completedChecks <= 2) {
      return {
        label: "Weak",
        width: "33%",
        className:
          "bg-red-500"
      };
    }

    if (completedChecks <= 4) {
      return {
        label: "Medium",
        width: "66%",
        className:
          "bg-amber-500"
      };
    }

    return {
      label: "Strong",
      width: "100%",
      className:
        "bg-green-500"
    };
  }, [passwordChecks]);


  const passwordsMatch =
    formData.confirmPassword.length > 0 &&
    formData.password ===
      formData.confirmPassword;


  const handleChange = (event) => {
    const { name, value } =
      event.target;

    setFormData((currentForm) => ({
      ...currentForm,
      [name]: value
    }));

    setErrorMessage("");
    setSuccessMessage("");
  };


  const handleRegister = async (event) => {
    event.preventDefault();

    setErrorMessage("");
    setSuccessMessage("");

    const cleanedName =
      formData.full_name.trim();

    const cleanedEmail =
      formData.email
        .trim()
        .toLowerCase();

    if (cleanedName.length < 2) {
      setErrorMessage(
        "Full name must contain at least 2 characters."
      );

      return;
    }

    if (!cleanedEmail) {
      setErrorMessage(
        "Please enter your email address."
      );

      return;
    }

    const allPasswordChecksPassed =
      Object.values(passwordChecks)
        .every(Boolean);

    if (!allPasswordChecksPassed) {
      setErrorMessage(
        "Please create a stronger password that meets all requirements."
      );

      return;
    }

    if (
      formData.password !==
      formData.confirmPassword
    ) {
      setErrorMessage(
        "Password and confirm password do not match."
      );

      return;
    }

    setIsLoading(true);

    try {
      await registerUser({
        full_name: cleanedName,
        email: cleanedEmail,
        password: formData.password
      });

      setSuccessMessage(
        "Registration successful. Redirecting to login..."
      );

      setTimeout(() => {
        navigate("/login", {
          replace: true
        });
      }, 1200);
    } catch (error) {
      console.error(
        "Registration error:",
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
            <div className="flex items-center gap-3">
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
                Start your career journey
              </span>

              <h1 className="
                mt-6
                text-4xl font-bold
                leading-tight
                tracking-[-0.04em]
                text-[var(--text-primary)]
                xl:text-5xl
              ">
                Create your account and build a clearer career path.
              </h1>

              <p className="
                mt-6
                text-lg leading-8
                text-[var(--text-secondary)]
              ">
                Analyze your resume, understand your strengths,
                discover missing skills and receive practical
                career recommendations.
              </p>
            </div>

            <div className="
              mt-12 grid gap-4
              sm:grid-cols-2
            ">
              <FeatureItem
                icon={<FaChartLine />}
                title="ATS Analysis"
                description="Understand how effectively your resume is structured."
              />

              <FeatureItem
                icon={<FaGraduationCap />}
                title="Skill Gap"
                description="Identify the skills required for your target career."
              />

              <FeatureItem
                icon={<FaBriefcase />}
                title="Career Matches"
                description="Discover careers that match your skills and experience."
              />

              <FeatureItem
                icon={<FaUserCheck />}
                title="Personalized Guidance"
                description="Receive recommendations based on your latest resume."
              />
            </div>
          </div>

          <p className="
            relative mt-10
            text-sm
            text-[var(--text-muted)]
          ">
            Create one account to manage your entire career-development journey.
          </p>
        </section>


        {/* Register form section */}
        <section className="
          flex min-h-screen
          items-center justify-center
          px-5 py-10
          sm:px-8
          lg:px-12
        ">
          <div className="w-full max-w-[540px]">
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
              <span className="badge badge-primary">
                Create account
              </span>

              <h1 className="
                mt-5
                text-3xl font-bold
                tracking-tight
                text-[var(--text-primary)]
              ">
                Join CareerCompass
              </h1>

              <p className="
                mt-3
                leading-7
                text-[var(--text-secondary)]
              ">
                Create your account to save resume analyses,
                career matches and skill-development progress.
              </p>


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


              {successMessage && (
                <div className="
                  mt-6 rounded-2xl
                  border border-green-300
                  bg-green-50 p-4
                  text-sm text-green-800

                  dark:border-green-900/70
                  dark:bg-green-950/30
                  dark:text-green-300
                ">
                  {successMessage}
                </div>
              )}


              <form
                onSubmit={handleRegister}
                className="mt-7 space-y-5"
              >
                <AuthInput
                  id="full_name"
                  name="full_name"
                  label="Full Name"
                  type="text"
                  value={formData.full_name}
                  onChange={handleChange}
                  placeholder="Enter your full name"
                  autoComplete="name"
                  icon={<FaUser />}
                />

                <AuthInput
                  id="email"
                  name="email"
                  label="Email Address"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="Enter your email"
                  autoComplete="email"
                  icon={<FaEnvelope />}
                />


                <PasswordField
                  id="password"
                  name="password"
                  label="Password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Create a strong password"
                  autoComplete="new-password"
                  showPassword={showPassword}
                  onToggle={() =>
                    setShowPassword(
                      (currentValue) =>
                        !currentValue
                    )
                  }
                />


                {formData.password && (
                  <div className="
                    rounded-2xl
                    border border-[var(--border)]
                    bg-[var(--surface-soft)]
                    p-4
                  ">
                    <div className="
                      flex items-center justify-between
                      text-sm
                    ">
                      <span className="
                        font-semibold
                        text-[var(--text-primary)]
                      ">
                        Password strength
                      </span>

                      <span className="
                        font-bold
                        text-[var(--text-secondary)]
                      ">
                        {passwordStrength.label}
                      </span>
                    </div>

                    <div className="
                      mt-3 h-2 overflow-hidden
                      rounded-full
                      bg-[var(--surface-muted)]
                    ">
                      <div
                        className={`
                          h-full rounded-full
                          transition-all duration-300
                          ${passwordStrength.className}
                        `}
                        style={{
                          width:
                            passwordStrength.width
                        }}
                      />
                    </div>

                    <div className="
                      mt-4 grid gap-2
                      sm:grid-cols-2
                    ">
                      <Requirement
                        passed={passwordChecks.length}
                        text="At least 8 characters"
                      />

                      <Requirement
                        passed={passwordChecks.uppercase}
                        text="One uppercase letter"
                      />

                      <Requirement
                        passed={passwordChecks.lowercase}
                        text="One lowercase letter"
                      />

                      <Requirement
                        passed={passwordChecks.number}
                        text="One number"
                      />

                      <Requirement
                        passed={passwordChecks.special}
                        text="One special character"
                      />
                    </div>
                  </div>
                )}


                <PasswordField
                  id="confirmPassword"
                  name="confirmPassword"
                  label="Confirm Password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  placeholder="Confirm your password"
                  autoComplete="new-password"
                  showPassword={
                    showConfirmPassword
                  }
                  onToggle={() =>
                    setShowConfirmPassword(
                      (currentValue) =>
                        !currentValue
                    )
                  }
                />


                {formData.confirmPassword && (
                  <div
                    className={`
                      flex items-center gap-2
                      rounded-xl border p-3
                      text-sm font-medium
                      ${
                        passwordsMatch
                          ? "border-green-300 bg-green-50 text-green-800 dark:border-green-900/70 dark:bg-green-950/30 dark:text-green-300"
                          : "border-red-300 bg-red-50 text-red-800 dark:border-red-900/70 dark:bg-red-950/30 dark:text-red-300"
                      }
                    `}
                  >
                    {passwordsMatch ? (
                      <FaCheck />
                    ) : (
                      <FaTimes />
                    )}

                    {passwordsMatch
                      ? "Passwords match"
                      : "Passwords do not match"}
                  </div>
                )}


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

                      Creating Account...
                    </>
                  ) : (
                    "Create Account"
                  )}
                </button>
              </form>


              <p className="
                mt-7 text-center
                text-[var(--text-secondary)]
              ">
                Already have an account?{" "}
                <button
                  type="button"
                  onClick={() =>
                    navigate("/login")
                  }
                  className="
                    font-semibold
                    text-[var(--primary)]
                    hover:underline
                  "
                >
                  Login
                </button>
              </p>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}


function AuthInput({
  id,
  name,
  label,
  type,
  value,
  onChange,
  placeholder,
  autoComplete,
  icon
}) {
  return (
    <div className="form-group">
      <label
        htmlFor={id}
        className="form-label"
      >
        {label}
      </label>

      <div className="relative">
        <span className="
          pointer-events-none
          absolute left-4 top-1/2
          z-10 -translate-y-1/2
          text-[var(--text-muted)]
        ">
          {icon}
        </span>

        <input
          id={id}
          name={name}
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          autoComplete={autoComplete}
          required
          className="form-input"
          style={{
            paddingLeft: "2.9rem"
          }}
        />
      </div>
    </div>
  );
}


function PasswordField({
  id,
  name,
  label,
  value,
  onChange,
  placeholder,
  autoComplete,
  showPassword,
  onToggle
}) {
  return (
    <div className="form-group">
      <label
        htmlFor={id}
        className="form-label"
      >
        {label}
      </label>

      <div className="relative">
        <FaLock className="
          pointer-events-none
          absolute left-4 top-1/2
          z-10 -translate-y-1/2
          text-[var(--text-muted)]
        " />

        <input
          id={id}
          name={name}
          type={
            showPassword
              ? "text"
              : "password"
          }
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          autoComplete={autoComplete}
          required
          className="form-input"
          style={{
            paddingLeft: "2.9rem",
            paddingRight: "3rem"
          }}
        />

        <button
          type="button"
          onClick={onToggle}
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
  );
}


function Requirement({
  passed,
  text
}) {
  return (
    <div
      className={`
        flex items-center gap-2
        text-xs font-medium
        ${
          passed
            ? "text-green-700 dark:text-green-300"
            : "text-[var(--text-muted)]"
        }
      `}
    >
      {passed ? (
        <FaCheck />
      ) : (
        <FaTimes />
      )}

      {text}
    </div>
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


export default Register;