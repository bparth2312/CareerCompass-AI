import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaArrowLeft,
  FaBriefcase,
  FaCheckCircle,
  FaExclamationTriangle,
  FaLightbulb,
  FaSearch,
  FaTimesCircle
} from "react-icons/fa";

import ThemeToggle from
  "../components/ThemeToggle/ThemeToggle";

import {
  analyzeJobDescription
} from "../services/resumeService";


const getErrorMessage = (
  error,
  fallback
) => {
  const detail =
    error.response?.data?.detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) =>
        item?.msg || "Validation error"
      )
      .join(", ");
  }

  if (error.message === "Network Error") {
    return (
      "Unable to connect to the backend. " +
      "Make sure FastAPI is running."
    );
  }

  return fallback;
};


function JobDescriptionAnalyzer() {
  const navigate = useNavigate();

  const [jobTitle, setJobTitle] =
    useState("");

  const [
    jobDescription,
    setJobDescription
  ] = useState("");

  const [analysis, setAnalysis] =
    useState(null);

  const [isLoading, setIsLoading] =
    useState(false);

  const [
    errorMessage,
    setErrorMessage
  ] = useState("");


  const handleAnalyze = async (
    event
  ) => {
    event.preventDefault();

    if (
      jobDescription.trim().length < 50
    ) {
      setErrorMessage(
        "Job description must contain at least 50 characters."
      );

      return;
    }

    setIsLoading(true);
    setErrorMessage("");
    setAnalysis(null);

    try {
      const response =
        await analyzeJobDescription(
          jobTitle.trim(),
          jobDescription.trim()
        );

      setAnalysis(response);

      window.scrollTo({
        top: 0,
        behavior: "smooth"
      });
    } catch (error) {
      console.error(
        "Job description analysis error:",
        error
      );

      if (
        error.response?.status === 401
      ) {
        localStorage.removeItem(
          "token"
        );

        navigate("/login", {
          replace: true
        });

        return;
      }

      setErrorMessage(
        getErrorMessage(
          error,
          "Unable to analyze the job description."
        )
      );
    } finally {
      setIsLoading(false);
    }
  };


  const handleReset = () => {
    setJobTitle("");
    setJobDescription("");
    setAnalysis(null);
    setErrorMessage("");
  };


  return (
    <main className="app-page">
      <div className="page-container max-w-[1500px]">

        {/* Header */}
        <header
          className="
            flex flex-col gap-5
            border-b border-[var(--border)]
            pb-7

            md:flex-row
            md:items-center
            md:justify-between
          "
        >
          <div>
            <p
              className="
                text-sm font-bold
                text-[var(--primary)]
              "
            >
              CareerCompass AI
            </p>

            <h1
              className="
                mt-2 text-3xl font-bold
                tracking-tight
                text-[var(--text-primary)]

                md:text-4xl
              "
            >
              Resume vs Job Description
            </h1>

            <p
              className="
                mt-3 max-w-3xl
                leading-7
                text-[var(--text-secondary)]
              "
            >
              Compare your latest analyzed resume
              with a job description and identify
              matched skills, missing skills,
              important keywords and improvement
              suggestions.
            </p>
          </div>

          <div
            className="
              flex items-center gap-3
            "
          >
            <ThemeToggle />

            <button
              type="button"
              onClick={() =>
                navigate("/dashboard")
              }
              className="btn-outline"
            >
              <FaArrowLeft />
              Back to Dashboard
            </button>
          </div>
        </header>


        {/* Error */}
        {errorMessage && (
          <section
            className="
              mt-7 rounded-2xl
              border border-red-300
              bg-red-50 p-5
              text-red-800

              dark:border-red-900/70
              dark:bg-red-950/30
              dark:text-red-300
            "
          >
            <div
              className="
                flex items-start gap-3
              "
            >
              <FaExclamationTriangle
                className="
                  mt-1 shrink-0
                "
              />

              <p>
                {errorMessage}
              </p>
            </div>
          </section>
        )}


        <div
          className="
            mt-8 grid gap-7

            xl:grid-cols-[0.95fr_1.4fr]
          "
        >
          {/* Input form */}
          <section
            className="
              h-fit rounded-3xl
              border border-[var(--border)]
              bg-[var(--surface)]
              p-7
              shadow-[var(--shadow-sm)]
            "
          >
            <div
              className="
                flex items-center gap-4
              "
            >
              <div
                className="
                  flex h-12 w-12
                  items-center justify-center
                  rounded-2xl
                  bg-[var(--primary-soft)]
                  text-xl
                  text-[var(--primary)]
                "
              >
                <FaBriefcase />
              </div>

              <div>
                <h2
                  className="
                    text-2xl font-bold
                    text-[var(--text-primary)]
                  "
                >
                  Job Information
                </h2>

                <p
                  className="
                    mt-1 text-sm
                    text-[var(--text-secondary)]
                  "
                >
                  Paste the complete job description
                  for better results.
                </p>
              </div>
            </div>


            <form
              onSubmit={handleAnalyze}
              className="mt-7"
            >
              <label
                htmlFor="job-title"
                className="
                  mb-2 block
                  text-sm font-semibold
                  text-[var(--text-primary)]
                "
              >
                Job Title
              </label>

              <input
                id="job-title"
                type="text"
                value={jobTitle}
                onChange={(event) =>
                  setJobTitle(
                    event.target.value
                  )
                }
                maxLength={150}
                placeholder="Example: Full Stack Developer"
                className="form-input"
              />


              <div className="mt-6">
                <div
                  className="
                    mb-2 flex
                    items-center
                    justify-between gap-4
                  "
                >
                  <label
                    htmlFor="job-description"
                    className="
                      block text-sm
                      font-semibold
                      text-[var(--text-primary)]
                    "
                  >
                    Job Description
                  </label>

                  <span
                    className="
                      text-xs
                      text-[var(--text-muted)]
                    "
                  >
                    {jobDescription.length}
                    /20000
                  </span>
                </div>

                <textarea
                  id="job-description"
                  value={jobDescription}
                  onChange={(event) =>
                    setJobDescription(
                      event.target.value
                    )
                  }
                  minLength={50}
                  maxLength={20000}
                  rows={15}
                  required
                  placeholder="Paste responsibilities, required skills, qualifications and experience requirements here..."
                  className="
                    form-input resize-y
                    leading-7
                  "
                />
              </div>


              <button
                type="submit"
                disabled={isLoading}
                className="
                  btn-primary mt-6
                  w-full justify-center
                  py-4
                  disabled:cursor-not-allowed
                  disabled:opacity-60
                "
              >
                <FaSearch />

                {isLoading
                  ? "Analyzing..."
                  : "Analyze Job Match"}
              </button>

              {(jobTitle ||
                jobDescription ||
                analysis) && (
                <button
                  type="button"
                  onClick={handleReset}
                  disabled={isLoading}
                  className="
                    btn-outline mt-3
                    w-full justify-center
                  "
                >
                  Clear Analysis
                </button>
              )}
            </form>
          </section>


          {/* Result */}
          <section>
            {analysis ? (
              <AnalysisResult
                analysis={analysis}
              />
            ) : (
              <EmptyResult />
            )}
          </section>
        </div>
      </div>
    </main>
  );
}


function EmptyResult() {
  return (
    <div
      className="
        flex min-h-[520px]
        flex-col items-center
        justify-center
        rounded-3xl
        border border-dashed
        border-[var(--border)]
        bg-[var(--surface)]
        p-10 text-center
      "
    >
      <div
        className="
          flex h-20 w-20
          items-center justify-center
          rounded-3xl
          bg-[var(--primary-soft)]
          text-3xl
          text-[var(--primary)]
        "
      >
        <FaSearch />
      </div>

      <h2
        className="
          mt-6 text-2xl font-bold
          text-[var(--text-primary)]
        "
      >
        Analyze Your Job Match
      </h2>

      <p
        className="
          mt-3 max-w-lg
          leading-7
          text-[var(--text-secondary)]
        "
      >
        Enter a job title and paste the job
        description. CareerCompass AI will compare
        it with your latest analyzed resume.
      </p>
    </div>
  );
}


function AnalysisResult({
  analysis
}) {
  const score =
    Number(
      analysis.overall_match_score
    ) || 0;

  const scoreStyles =
    getScoreStyles(score);

  return (
    <div className="space-y-6">

      {/* Main score */}
      <section
        className="
          rounded-3xl
          border border-[var(--border)]
          bg-[var(--surface)]
          p-7
          shadow-[var(--shadow-sm)]
        "
      >
        <div
          className="
            flex flex-col gap-6

            sm:flex-row
            sm:items-center
            sm:justify-between
          "
        >
          <div>
            <p
              className="
                text-sm font-semibold
                text-[var(--primary)]
              "
            >
              Job Match Result
            </p>

            <h2
              className="
                mt-2 text-3xl font-bold
                text-[var(--text-primary)]
              "
            >
              {analysis.job_title}
            </h2>

            <p
              className="
                mt-2
                text-[var(--text-secondary)]
              "
            >
              Resume:{" "}
              <strong
                className="
                  text-[var(--text-primary)]
                "
              >
                {analysis.file_name}
              </strong>
            </p>

            <div
              className="
                mt-5 flex flex-wrap
                gap-3
              "
            >
              <span
                className={`
                  rounded-full
                  border px-4 py-2
                  text-sm font-bold

                  ${scoreStyles.badge}
                `}
              >
                {analysis.match_level}
              </span>

              <span
                className="
                  rounded-full
                  border border-[var(--border)]
                  bg-[var(--surface-soft)]
                  px-4 py-2
                  text-sm font-semibold
                  text-[var(--text-secondary)]
                "
              >
                {analysis.application_status}
              </span>
            </div>
          </div>

          <div
            className={`
              flex h-32 w-32 shrink-0
              flex-col items-center
              justify-center
              rounded-full
              border-[10px]

              ${scoreStyles.circle}
            `}
          >
            <span
              className="
                text-4xl font-bold
                text-[var(--text-primary)]
              "
            >
              {score}%
            </span>

            <span
              className="
                mt-1 text-xs
                text-[var(--text-secondary)]
              "
            >
              Overall Match
            </span>
          </div>
        </div>
      </section>


      {/* Score breakdown */}
      <section
        className="
          grid gap-4

          sm:grid-cols-3
        "
      >
        <ScoreCard
          label="Skill Match"
          value={
            analysis
              .skill_match_percentage
          }
        />

        <ScoreCard
          label="Keyword Match"
          value={
            analysis
              .keyword_match_percentage
          }
        />

        <ScoreCard
          label="Resume Quality"
          value={
            analysis
              .resume_quality_score * 10
          }
        />
      </section>


      {/* Skills */}
      <section
        className="
          grid gap-5

          lg:grid-cols-2
        "
      >
        <ListCard
          title="Matched Skills"
          items={
            analysis.matched_skills
          }
          type="success"
          emptyMessage={
            "No required skills were matched."
          }
        />

        <ListCard
          title="Missing Skills"
          items={
            analysis.missing_skills
          }
          type="danger"
          emptyMessage={
            "No missing technical skills."
          }
        />
      </section>


      {/* Keywords */}
      <section
        className="
          grid gap-5

          lg:grid-cols-2
        "
      >
        <ListCard
          title="Matched Keywords"
          items={
            analysis.matched_keywords
          }
          type="success"
          emptyMessage={
            "No important keywords were matched."
          }
        />

        <ListCard
          title="Missing Keywords"
          items={
            analysis.missing_keywords
          }
          type="warning"
          emptyMessage={
            "No important keywords are missing."
          }
        />
      </section>


      {/* Experience */}
      {analysis.experience_requirement && (
        <section
          className="
            rounded-2xl
            border border-blue-300
            bg-blue-50 p-5
            text-blue-900

            dark:border-blue-900/70
            dark:bg-blue-950/30
            dark:text-blue-300
          "
        >
          <p className="font-semibold">
            Experience Requirement
          </p>

          <p className="mt-2">
            {
              analysis
                .experience_requirement
            }
          </p>
        </section>
      )}


      {/* Strengths and suggestions */}
      <section
        className="
          grid gap-5

          lg:grid-cols-2
        "
      >
        <MessageCard
          title="Resume Strengths"
          items={analysis.strengths}
          icon={<FaCheckCircle />}
          type="success"
        />

        <MessageCard
          title="Improvement Suggestions"
          items={analysis.suggestions}
          icon={<FaLightbulb />}
          type="warning"
        />
      </section>
    </div>
  );
}


function ScoreCard({
  label,
  value
}) {
  const safeValue = Math.min(
    Math.max(
      Number(value) || 0,
      0
    ),
    100
  );

  return (
    <div
      className="
        rounded-2xl
        border border-[var(--border)]
        bg-[var(--surface)]
        p-5
        shadow-[var(--shadow-sm)]
      "
    >
      <div
        className="
          flex items-center
          justify-between gap-3
        "
      >
        <p
          className="
            text-sm font-semibold
            text-[var(--text-secondary)]
          "
        >
          {label}
        </p>

        <strong
          className="
            text-xl
            text-[var(--text-primary)]
          "
        >
          {safeValue}%
        </strong>
      </div>

      <div
        className="
          mt-4 h-2.5
          overflow-hidden
          rounded-full
          bg-[var(--surface-muted)]
        "
      >
        <div
          className="
            h-full rounded-full
            bg-[var(--primary)]
            transition-all duration-500
          "
          style={{
            width: `${safeValue}%`
          }}
        />
      </div>
    </div>
  );
}


function ListCard({
  title,
  items = [],
  type,
  emptyMessage
}) {
  const styles = {
    success: {
      icon: (
        <FaCheckCircle />
      ),
      title:
        "text-emerald-700 dark:text-emerald-300",
      chip: `
        border-emerald-300
        bg-emerald-50
        text-emerald-800

        dark:border-emerald-900/70
        dark:bg-emerald-950/40
        dark:text-emerald-300
      `
    },

    danger: {
      icon: (
        <FaTimesCircle />
      ),
      title:
        "text-red-700 dark:text-red-300",
      chip: `
        border-red-300
        bg-red-50
        text-red-800

        dark:border-red-900/70
        dark:bg-red-950/40
        dark:text-red-300
      `
    },

    warning: {
      icon: (
        <FaExclamationTriangle />
      ),
      title:
        "text-amber-700 dark:text-amber-300",
      chip: `
        border-amber-300
        bg-amber-50
        text-amber-800

        dark:border-amber-900/70
        dark:bg-amber-950/40
        dark:text-amber-300
      `
    }
  };

  const selected =
    styles[type] ||
    styles.success;

  return (
    <div
      className="
        rounded-2xl
        border border-[var(--border)]
        bg-[var(--surface)]
        p-6
        shadow-[var(--shadow-sm)]
      "
    >
      <h3
        className={`
          flex items-center gap-2
          text-lg font-bold

          ${selected.title}
        `}
      >
        {selected.icon}
        {title}
      </h3>

      {items.length > 0 ? (
        <div
          className="
            mt-5 flex flex-wrap
            gap-2
          "
        >
          {items.map(
            (item, index) => (
              <span
                key={`${item}-${index}`}
                className={`
                  rounded-full
                  border px-3 py-1.5
                  text-sm font-semibold

                  ${selected.chip}
                `}
              >
                {item}
              </span>
            )
          )}
        </div>
      ) : (
        <p
          className="
            mt-5 text-sm
            text-[var(--text-secondary)]
          "
        >
          {emptyMessage}
        </p>
      )}
    </div>
  );
}


function MessageCard({
  title,
  items = [],
  icon,
  type
}) {
  const isSuccess =
    type === "success";

  return (
    <div
      className="
        rounded-2xl
        border border-[var(--border)]
        bg-[var(--surface)]
        p-6
        shadow-[var(--shadow-sm)]
      "
    >
      <h3
        className={`
          flex items-center gap-2
          text-lg font-bold

          ${
            isSuccess
              ? `
                text-emerald-700
                dark:text-emerald-300
              `
              : `
                text-amber-700
                dark:text-amber-300
              `
          }
        `}
      >
        {icon}
        {title}
      </h3>

      <div className="mt-5 space-y-3">
        {items.map(
          (item, index) => (
            <div
              key={`${item}-${index}`}
              className="
                flex items-start gap-3
                rounded-xl
                bg-[var(--surface-soft)]
                p-4
              "
            >
              <span
                className={`
                  mt-1 shrink-0

                  ${
                    isSuccess
                      ? "text-emerald-500"
                      : "text-amber-500"
                  }
                `}
              >
                {icon}
              </span>

              <p
                className="
                  text-sm leading-6
                  text-[var(--text-secondary)]
                "
              >
                {item}
              </p>
            </div>
          )
        )}
      </div>
    </div>
  );
}


function getScoreStyles(
  score
) {
  if (score >= 80) {
    return {
      circle:
        "border-emerald-500 bg-emerald-50 dark:bg-emerald-950/30",

      badge: `
        border-emerald-300
        bg-emerald-50
        text-emerald-800

        dark:border-emerald-900/70
        dark:bg-emerald-950/40
        dark:text-emerald-300
      `
    };
  }

  if (score >= 65) {
    return {
      circle:
        "border-teal-500 bg-teal-50 dark:bg-teal-950/30",

      badge: `
        border-teal-300
        bg-teal-50
        text-teal-800

        dark:border-teal-900/70
        dark:bg-teal-950/40
        dark:text-teal-300
      `
    };
  }

  if (score >= 50) {
    return {
      circle:
        "border-amber-500 bg-amber-50 dark:bg-amber-950/30",

      badge: `
        border-amber-300
        bg-amber-50
        text-amber-800

        dark:border-amber-900/70
        dark:bg-amber-950/40
        dark:text-amber-300
      `
    };
  }

  return {
    circle:
      "border-red-500 bg-red-50 dark:bg-red-950/30",

    badge: `
      border-red-300
      bg-red-50
      text-red-800

      dark:border-red-900/70
      dark:bg-red-950/40
      dark:text-red-300
    `
  };
}


export default JobDescriptionAnalyzer;