import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaArrowLeft,
  FaCheckCircle,
  FaExclamationTriangle,
  FaGraduationCap,
  FaTimesCircle
} from "react-icons/fa";

import ThemeToggle from "../components/ThemeToggle/ThemeToggle";
import { getLatestResumeAnalysis } from "../services/resumeService";

const getErrorMessage = (error, fallbackMessage) => {
  const detail = error.response?.data?.detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) => item?.msg || "Validation error")
      .join(", ");
  }

  return fallbackMessage;
};

function SkillGap() {
  const navigate = useNavigate();

  const [analysis, setAnalysis] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const loadSkillGapAnalysis = async () => {
      setIsLoading(true);
      setErrorMessage("");

      try {
        const data = await getLatestResumeAnalysis();
        setAnalysis(data);
      } catch (error) {
        console.error("Skill gap loading error:", error);

        if (error.response?.status === 401) {
          localStorage.removeItem("token");
          navigate("/login", { replace: true });
          return;
        }

        setErrorMessage(
          getErrorMessage(
            error,
            "Unable to load skill gap analysis."
          )
        );
      } finally {
        setIsLoading(false);
      }
    };

    loadSkillGapAnalysis();
  }, [navigate]);

  if (isLoading) {
    return (
      <main className="app-page">
        <div className="page-container max-w-[1600px]">
          <div className="state-container">
            <div className="spinner" />
            <p className="state-title">
              Loading skill gap analysis
            </p>
            <p className="state-message">
              We are comparing your skills with the requirements of your recommended career.
            </p>
          </div>
        </div>
      </main>
    );
  }

  const skillGap =
    analysis?.skill_gap_analysis || {};

  const matchedSkills =
    skillGap.matched_skills || [];

  const missingSkills =
    skillGap.missing_skills || [];

  const prioritySkills =
    skillGap.priority_skills || [];

  const readinessScore =
    skillGap.readiness_score ??
    analysis?.career_readiness ??
    0;

  return (
    <main className="app-page">
      <div className="page-container max-w-[1600px]">
        <header className="
          flex flex-col gap-5
          border-b border-[var(--border)]
          pb-7
          sm:flex-row sm:items-center sm:justify-between
        ">
          <div>
            <p className="font-semibold text-[var(--primary)]">
              CareerCompass
            </p>

            <h1 className="
              mt-2 text-3xl font-bold
              text-[var(--text-primary)]
            ">
              Skill Gap Analysis
            </h1>

            <p className="
              mt-2 text-[var(--text-secondary)]
            ">
              Identify the skills you already have and the skills required for your recommended career.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <ThemeToggle />

            <button
              type="button"
              onClick={() => navigate("/dashboard")}
              className="btn-outline"
            >
              <FaArrowLeft />
              Back to Dashboard
            </button>
          </div>
        </header>

        {errorMessage ? (
          <section className="
            mt-8 rounded-2xl
            border border-red-300
            bg-red-50 p-6
            text-red-800
            dark:border-red-900/70
            dark:bg-red-950/30
            dark:text-red-300
          ">
            <div className="flex items-start gap-3">
              <FaExclamationTriangle className="mt-1 shrink-0" />

              <div>
                <h2 className="font-semibold">
                  Skill gap analysis unavailable
                </h2>

                <p className="mt-2 text-sm">
                  {errorMessage}
                </p>

                <button
                  type="button"
                  onClick={() => navigate("/resume")}
                  className="btn-primary mt-5"
                >
                  Upload and Analyze Resume
                </button>
              </div>
            </div>
          </section>
        ) : analysis ? (
          <>
            <section className="
              app-card mt-8
              border-2 border-[var(--border)]
              p-7 xl:p-9
            ">
              <div className="
                flex flex-col gap-7
                md:flex-row md:items-center
                md:justify-between
              ">
                <div>
                  <p className="
                    text-sm font-bold
                    text-[var(--primary)]
                  ">
                    Recommended Career
                  </p>

                  <h2 className="
                    mt-2 text-3xl font-bold
                    text-[var(--text-primary)]
                  ">
                    {skillGap.target_career ||
                      analysis.best_career ||
                      "Not available"}
                  </h2>

                  <p className="
                    mt-4 max-w-4xl leading-7
                    text-[var(--text-secondary)]
                  ">
                    {skillGap.summary ||
                      "Your skill gap is calculated by comparing your extracted resume skills with the required skills for your recommended career."}
                  </p>
                </div>

                <div className="shrink-0 text-center">
                  <div className="
                    flex h-32 w-32 items-center justify-center
                    rounded-full border-8
                    border-[var(--primary)]
                    bg-[var(--surface-soft)]
                  ">
                    <div>
                      <p className="
                        text-3xl font-bold
                        text-[var(--text-primary)]
                      ">
                        {readinessScore}%
                      </p>

                      <p className="
                        mt-1 text-xs font-medium
                        text-[var(--text-secondary)]
                      ">
                        readiness
                      </p>
                    </div>
                  </div>

                  <p className="
                    mt-3 font-bold
                    text-[var(--primary)]
                  ">
                    {skillGap.readiness_level ||
                      analysis.readiness_level ||
                      "Not available"}
                  </p>
                </div>
              </div>
            </section>

            <section className="
              mt-8 grid gap-6
              lg:grid-cols-2
            ">
              <article className="
                rounded-2xl border-2
                border-green-300
                bg-green-50 p-6
                dark:border-green-900/70
                dark:bg-green-950/30
              ">
                <h2 className="
                  flex items-center gap-2
                  text-xl font-bold
                  text-green-800
                  dark:text-green-300
                ">
                  <FaCheckCircle />
                  Skills You Already Have
                </h2>

                <div className="
                  mt-5 flex flex-wrap gap-3
                ">
                  {matchedSkills.length > 0 ? (
                    matchedSkills.map((skill) => (
                      <span
                        key={skill}
                        className="
                          rounded-full border
                          border-green-400
                          bg-white px-4 py-2
                          text-sm font-semibold
                          text-green-800
                          dark:border-green-800
                          dark:bg-green-950/50
                          dark:text-green-300
                        "
                      >
                        {skill}
                      </span>
                    ))
                  ) : (
                    <p className="
                      text-sm text-[var(--text-secondary)]
                    ">
                      No matching skills were found.
                    </p>
                  )}
                </div>
              </article>

              <article className="
                rounded-2xl border-2
                border-red-300
                bg-red-50 p-6
                dark:border-red-900/70
                dark:bg-red-950/30
              ">
                <h2 className="
                  flex items-center gap-2
                  text-xl font-bold
                  text-red-800
                  dark:text-red-300
                ">
                  <FaTimesCircle />
                  Missing Career Skills
                </h2>

                <div className="
                  mt-5 flex flex-wrap gap-3
                ">
                  {missingSkills.length > 0 ? (
                    missingSkills.map((skill) => (
                      <span
                        key={skill}
                        className="
                          rounded-full border
                          border-red-400
                          bg-white px-4 py-2
                          text-sm font-semibold
                          text-red-800
                          dark:border-red-800
                          dark:bg-red-950/50
                          dark:text-red-300
                        "
                      >
                        {skill}
                      </span>
                    ))
                  ) : (
                    <p className="
                      text-sm text-[var(--text-secondary)]
                    ">
                      No major skill gaps found.
                    </p>
                  )}
                </div>
              </article>
            </section>

            <section className="
              mt-8 grid gap-6
              lg:grid-cols-2
            ">
              <article className="
                rounded-2xl border-2
                border-amber-300
                bg-amber-50 p-6
                dark:border-amber-900/70
                dark:bg-amber-950/30
              ">
                <h2 className="
                  flex items-center gap-2
                  text-xl font-bold
                  text-amber-800
                  dark:text-amber-300
                ">
                  <FaGraduationCap />
                  Priority Skills to Learn
                </h2>

                <div className="mt-5 space-y-3">
                  {prioritySkills.length > 0 ? (
                    prioritySkills.map((skill, index) => (
                      <div
                        key={skill}
                        className="
                          flex items-center gap-3
                          rounded-xl border
                          border-amber-300
                          bg-white p-4
                          dark:border-amber-800
                          dark:bg-amber-950/50
                        "
                      >
                        <span className="
                          flex h-8 w-8 items-center justify-center
                          rounded-full
                          bg-amber-100
                          text-sm font-bold
                          text-amber-900
                          dark:bg-amber-900/50
                          dark:text-amber-200
                        ">
                          {index + 1}
                        </span>

                        <span className="
                          font-semibold
                          text-[var(--text-primary)]
                        ">
                          {skill}
                        </span>
                      </div>
                    ))
                  ) : (
                    <p className="
                      text-sm text-[var(--text-secondary)]
                    ">
                      No priority skills are currently required.
                    </p>
                  )}
                </div>
              </article>

              <article className="
                app-card border-2
                border-[var(--border)]
                p-6
              ">
                <p className="
                  text-sm font-bold
                  text-[var(--primary)]
                ">
                  Estimated Learning Time
                </p>

                <p className="
                  mt-4 text-4xl font-bold
                  text-[var(--text-primary)]
                ">
                  {skillGap.estimated_learning_time ||
                    "Not available"}
                </p>

                <p className="
                  mt-4 leading-7
                  text-[var(--text-secondary)]
                ">
                  This estimate is based on the number and importance of missing skills. Actual learning time may vary depending on your current knowledge and daily study schedule.
                </p>
              </article>
            </section>
          </>
        ) : null}
      </div>
    </main>
  );
}

export default SkillGap;