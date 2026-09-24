import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaArrowLeft,
  FaArrowUp,
  FaBriefcase,
  FaBullseye,
  FaChartLine,
  FaCheckCircle,
  FaChevronDown,
  FaChevronUp,
  FaExclamationTriangle,
  FaFileAlt,
  FaLightbulb,
  FaMagic,
  FaSpinner,
  FaTools
} from "react-icons/fa";

import ThemeToggle from
  "../components/ThemeToggle/ThemeToggle";

import {
  getResumeImprovementByCareer,
  getResumeImprovementSuggestions
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


function ResumeImprovement() {
  const navigate = useNavigate();

  const [data, setData] =
    useState(null);

  const [
    selectedCareer,
    setSelectedCareer
  ] = useState("");

  const [
  isCareerLoading,
  setIsCareerLoading
   ] = useState(false);

  const [isLoading, setIsLoading] =
    useState(true);

  const [
    errorMessage,
    setErrorMessage
  ] = useState("");


  useEffect(() => {
    const loadSuggestions = async () => {
      setIsLoading(true);
      setErrorMessage("");

      try {
        const response =
          await getResumeImprovementSuggestions();

        setData(response);

        setSelectedCareer(
          response.target_career ||
          response.recommended_careers?.[0]
            ?.career ||
          ""
        );
      } catch (error) {
        console.error(
          "Resume improvement error:",
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
            "Unable to load resume improvement suggestions."
          )
        );
      } finally {
        setIsLoading(false);
      }
    };

    loadSuggestions();
  }, [navigate]);
    const handleCareerChange = async (
  careerName
) => {
  if (
    !careerName ||
    careerName === selectedCareer ||
    isCareerLoading
  ) {
    return;
  }

  setSelectedCareer(careerName);
  setIsCareerLoading(true);
  setErrorMessage("");

  try {
    const response =
      await getResumeImprovementByCareer(
        careerName
      );

    setData(response);

    setSelectedCareer(
      response.target_career ||
      careerName
    );
  } catch (error) {
    console.error(
      "Career improvement error:",
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
        "Unable to generate suggestions for the selected career."
      )
    );
  } finally {
    setIsCareerLoading(false);
  }
};

  if (isLoading) {
    return (
      <main className="app-page">
        <div
          className="
            page-container
            flex min-h-[70vh]
            items-center justify-center
          "
        >
          <div
            className="
              flex flex-col items-center
              rounded-3xl
              border border-[var(--border)]
              bg-[var(--surface)]
              px-10 py-12
              text-center
              shadow-[var(--shadow-sm)]
            "
          >
            <FaSpinner
              className="
                animate-spin text-4xl
                text-[var(--primary)]
              "
            />

            <h1
              className="
                mt-6 text-2xl font-bold
                text-[var(--text-primary)]
              "
            >
              Preparing Suggestions
            </h1>

            <p
              className="
                mt-3 max-w-md
                leading-7
                text-[var(--text-secondary)]
              "
            >
              CareerCompass is reviewing your
              latest resume, ATS analysis and
              career skill gaps.
            </p>
          </div>
        </div>
      </main>
    );
  }


  return (
    <main className="app-page">
      <div
        className="
          page-container
          max-w-[1500px]
        "
      >
        {/* Header */}
        <header
          className="
            flex flex-col gap-5
            border-b
            border-[var(--border)]
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
              AI Resume Improvement
            </h1>

            <p
              className="
                mt-3 max-w-3xl
                leading-7
                text-[var(--text-secondary)]
              "
            >
              Review personalized suggestions
              based on your latest ATS analysis,
              missing sections, target career and
              skill gaps.
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

              <div>
                <p className="font-semibold">
                  Unable to load suggestions
                </p>

                <p className="mt-2">
                  {errorMessage}
                </p>

                <button
                  type="button"
                  onClick={() =>
                    navigate("/resume")
                  }
                  className="btn-primary mt-5"
                >
                  Analyze Resume
                </button>
              </div>
            </div>
          </section>
        )}


        {!errorMessage && data && (
          <>
            {/* Hero summary */}
            <section
              className="
                mt-8 overflow-hidden
                rounded-[28px]
                border border-[var(--border)]
                bg-[var(--surface)]
                shadow-[var(--shadow-sm)]
              "
            >
              <div
                className="
                  grid gap-8 p-7

                  lg:grid-cols-[1.2fr_0.8fr]
                  lg:items-center
                  lg:p-9
                "
              >
                <div>
                  <span
                    className="
                      inline-flex items-center
                      gap-2 rounded-full
                      border border-[var(--border)]
                      bg-[var(--primary-soft)]
                      px-4 py-2
                      text-sm font-bold
                      text-[var(--primary)]
                    "
                  >
                    <FaMagic />
                    Personalized AI Review
                  </span>

                  <h2
                    className="
                      mt-5 text-3xl font-bold
                      tracking-tight
                      text-[var(--text-primary)]

                      md:text-4xl
                    "
                  >
                    Improve your resume before
                    applying.
                  </h2>

                  <p
                    className="
                      mt-4 max-w-3xl
                      leading-7
                      text-[var(--text-secondary)]
                    "
                  >
                    {data.summary}
                  </p>

                  <div
                    className="
                      mt-6 flex flex-wrap
                      gap-3
                    "
                  >
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
                      Resume:{" "}
                      <strong
                        className="
                          text-[var(--text-primary)]
                        "
                      >
                        {data.file_name}
                      </strong>
                    </span>

                    {selectedCareer && (
                      <span
                        className="
                          rounded-full
                          border border-[var(--primary)]
                          bg-[var(--primary-soft)]
                          px-4 py-2
                          text-sm font-semibold
                          text-[var(--primary)]
                        "
                      >
                        {isCareerLoading
                          ? "Updating suggestions..."
                          : (
                            <>
                              Selected Career:{" "}
                              <strong>
                                {selectedCareer}
                              </strong>
                            </>
                          )}
                      </span>
                    )}
                  </div>

                  {/* Career selection */}
                  {data.recommended_careers
                    ?.length > 0 && (
                    <div
                      className="
                        mt-8 rounded-3xl
                        border border-[var(--border)]
                        bg-[var(--surface-soft)]
                        p-5
                      "
                    >
                      <div
                        className="
                          flex items-start gap-3
                        "
                      >
                        <div
                          className="
                            flex h-11 w-11
                            shrink-0 items-center
                            justify-center
                            rounded-2xl
                            bg-[var(--primary-soft)]
                            text-lg
                            text-[var(--primary)]
                          "
                        >
                          <FaBriefcase />
                        </div>

                        <div>
                          <h3
                            className="
                              font-bold
                              text-[var(--text-primary)]
                            "
                          >
                            Select Your Target Career
                          </h3>

                          <p
                            className="
                              mt-1 text-sm
                              text-[var(--text-secondary)]
                            "
                          >
                            Choose one of the careers
                            that best matches your
                            resume and interests.
                          </p>
                        </div>
                      </div>

                      <div
                        className="
                          mt-5 grid gap-3

                          sm:grid-cols-2
                        "
                      >
                        {data.recommended_careers
                          .slice(0, 5)
                          .map(
                            (
                              careerItem,
                              index
                            ) => {
                              const isSelected =
                                selectedCareer ===
                                careerItem.career;

                              return (
                                <button
                                  key={
                                    careerItem.career
                                  }
                                  type="button"
                                  disabled={isCareerLoading}
                                  onClick={() =>
                                    handleCareerChange(
                                      careerItem.career
                                    )
                                  }
                                  className={`
                                    group relative
                                    overflow-hidden
                                    rounded-2xl border
                                    p-4 text-left
                                    transition duration-200
                                    disabled:cursor-not-allowed
                                    disabled:opacity-60

                                    ${
                                      isSelected
                                        ? `
                                          border-[var(--primary)]
                                          bg-[var(--primary-soft)]
                                          shadow-sm
                                        `
                                        : `
                                          border-[var(--border)]
                                          bg-[var(--surface)]

                                          hover:-translate-y-0.5
                                          hover:border-[var(--primary)]
                                          hover:shadow-sm
                                        `
                                    }
                                  `}
                                >
                                  <div
                                    className="
                                      flex items-start
                                      justify-between
                                      gap-4
                                    "
                                  >
                                    <div className="min-w-0">
                                      <div
                                        className="
                                          flex items-center
                                          gap-2
                                        "
                                      >
                                        <span
                                          className={`
                                            flex h-7 w-7
                                            shrink-0
                                            items-center
                                            justify-center
                                            rounded-full
                                            text-xs
                                            font-bold

                                            ${
                                              isSelected
                                                ? `
                                                  bg-[var(--primary)]
                                                  text-white
                                                `
                                                : `
                                                  bg-[var(--surface-muted)]
                                                  text-[var(--text-secondary)]
                                                `
                                            }
                                          `}
                                        >
                                          {index + 1}
                                        </span>

                                        <p
                                          className={`
                                            truncate
                                            font-bold

                                            ${
                                              isSelected
                                                ? `
                                                  text-[var(--primary)]
                                                `
                                                : `
                                                  text-[var(--text-primary)]
                                                `
                                            }
                                          `}
                                        >
                                          {
                                            careerItem.career
                                          }
                                        </p>
                                      </div>

                                      {careerItem.description && (
                                        <p
                                          className="
                                            mt-3
                                            line-clamp-2
                                            text-sm
                                            leading-6
                                            text-[var(--text-secondary)]
                                          "
                                        >
                                          {
                                            careerItem.description
                                          }
                                        </p>
                                      )}
                                    </div>

                                    <div
                                      className={`
                                        shrink-0
                                        rounded-xl
                                        px-3 py-2
                                        text-sm
                                        font-bold

                                        ${
                                          isSelected
                                            ? `
                                              bg-[var(--primary)]
                                              text-white
                                            `
                                            : `
                                              bg-[var(--primary-soft)]
                                              text-[var(--primary)]
                                            `
                                        }
                                      `}
                                    >
                                      {
                                        careerItem
                                          .match_percentage
                                      }
                                      %
                                    </div>
                                  </div>

                                  {isSelected && (
                                    <div
                                      className="
                                        mt-4 flex
                                        items-center gap-2
                                        border-t
                                        border-[var(--border)]
                                        pt-3
                                        text-xs
                                        font-semibold
                                        text-[var(--primary)]
                                      "
                                    >
                                      <FaCheckCircle />
                                      Selected target career
                                    </div>
                                  )}
                                </button>
                              );
                            }
                          )}
                      </div>
                    </div>
                  )}
                </div>

                <ScoreComparison
                  currentScore={
                    data.current_ats_score
                  }
                  potentialScore={
                    data.potential_ats_score
                  }
                />
              </div>
            </section>

 {/* Selected career summary */}
{selectedCareer && (
  <section
    className="
      mt-6 rounded-2xl
      border border-[var(--primary)]
      bg-[var(--primary-soft)]
      p-5
    "
  >
    <div
      className="
        flex flex-col gap-4

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
          Current Target Career
        </p>

        <h2
          className="
            mt-1 text-xl font-bold
            text-[var(--text-primary)]
          "
        >
          {selectedCareer}
        </h2>

        <p
          className="
            mt-2 text-sm
            text-[var(--text-secondary)]
          "
        >
          Resume suggestions are currently
          displayed for the selected career.
        </p>

        <button
          type="button"
          onClick={() =>
            navigate(
              "/resume-rewrite",
              {
                state: {
                  targetCareer:
                    selectedCareer
                }
              }
            )
          }
          disabled={
            !selectedCareer ||
            isCareerLoading
          }
          className="
            btn-primary mt-5
            disabled:cursor-not-allowed
            disabled:opacity-60
          "
        >
          <FaMagic />
          Rewrite Resume for This Career
        </button>
      </div>

      <div
        className="
          flex h-12 w-12
          shrink-0 items-center
          justify-center
          rounded-2xl
          bg-[var(--primary)]
          text-xl text-white
        "
      >
        <FaBriefcase />
      </div>
    </div>
  </section>
)}


            {/* Priority statistics */}
            <section className="mt-8">
              <div>
                <h2 className="section-title">
                  Improvement Overview
                </h2>

                <p className="section-description">
                  Review the number and priority of
                  recommendations generated for your
                  latest resume.
                </p>
              </div>

              <div
                className="
                  mt-5 grid gap-5

                  sm:grid-cols-2
                  xl:grid-cols-4
                "
              >
                <PriorityCard
                  title="Total Suggestions"
                  value={
                    data.total_suggestions
                  }
                  description={
                    "Personalized improvements"
                  }
                  type="total"
                  icon={<FaLightbulb />}
                />

                <PriorityCard
                  title="High Priority"
                  value={
                    data.high_priority_count
                  }
                  description={
                    "Fix these improvements first"
                  }
                  type="high"
                  icon={
                    <FaExclamationTriangle />
                  }
                />

                <PriorityCard
                  title="Medium Priority"
                  value={
                    data.medium_priority_count
                  }
                  description={
                    "Important supporting changes"
                  }
                  type="medium"
                  icon={<FaChartLine />}
                />

                <PriorityCard
                  title="Potential Increase"
                  value={`+${Math.max(
                    Number(
                      data.potential_ats_score
                    ) -
                      Number(
                        data.current_ats_score
                      ),
                    0
                  )}%`}
                  description={
                    "Estimated ATS improvement"
                  }
                  type="success"
                  icon={<FaArrowUp />}
                />
              </div>
            </section>

            {/* Missing sections and priority skills */}
            <section className="mt-8">
              <div>
                <h2 className="section-title">
                  Resume Improvement Details
                </h2>

                <p className="section-description">
                  Review missing resume sections and important
                  skills for your selected career.
                </p>
              </div>

              <div
                className="
                  mt-5 grid gap-6

                  lg:grid-cols-2
                "
              >
                <MissingSectionsCard
                  sections={
                    data.missing_sections || []
                  }
                />

                <PrioritySkillsCard
                  skills={
                    data.priority_skills || []
                  }
                  selectedCareer={selectedCareer}
                />
              </div>
            </section>


            {/* Detailed AI suggestions */}
            <section className="mt-8">
              <div
                className="
                  flex flex-col gap-3

                  sm:flex-row
                  sm:items-end
                  sm:justify-between
                "
              >
                <div>
                  <h2 className="section-title">
                    Detailed AI Suggestions
                  </h2>

                  <p className="section-description">
                    Apply these recommendations to improve your
                    resume structure, ATS compatibility and
                    alignment with {selectedCareer || "your target career"}.
                  </p>
                </div>

                <span
                  className="
                    w-fit rounded-full
                    border border-[var(--border)]
                    bg-[var(--surface-soft)]
                    px-4 py-2
                    text-sm font-semibold
                    text-[var(--text-secondary)]
                  "
                >
                  {Array.isArray(data.suggestions)
                    ? data.suggestions.length
                    : 0}{" "}
                  recommendations
                </span>
              </div>

              <SuggestionsList
                suggestions={
                  data.suggestions || []
                }
              />
            </section>
          </>
        )}
      </div>
    </main>
  );
}


function ScoreComparison({
  currentScore,
  potentialScore
}) {
  const current = Math.min(
    Math.max(
      Number(currentScore) || 0,
      0
    ),
    100
  );

  const potential = Math.min(
    Math.max(
      Number(potentialScore) || 0,
      0
    ),
    100
  );

  const improvement = Math.max(
    potential - current,
    0
  );

  return (
    <div
      className="
        rounded-[24px]
        border border-[var(--border)]
        bg-[var(--surface-soft)]
        p-6
      "
    >
      <p
        className="
          text-sm font-semibold
          text-[var(--text-secondary)]
        "
      >
        ATS Score Potential
      </p>

      <div
        className="
          mt-5 grid grid-cols-2
          gap-4
        "
      >
        <ScoreCircle
          label="Current"
          score={current}
          type="current"
        />

        <ScoreCircle
          label="Potential"
          score={potential}
          type="potential"
        />
      </div>

      <div
        className="
          mt-6 rounded-2xl
          border border-emerald-200
          bg-emerald-50 p-4
          text-emerald-800

          dark:border-emerald-900/70
          dark:bg-emerald-950/30
          dark:text-emerald-300
        "
      >
        <div
          className="
            flex items-center gap-3
          "
        >
          <FaArrowUp />

          <div>
            <p className="font-bold">
              Improve by {improvement}%
            </p>

            <p className="mt-1 text-sm">
              Complete the recommended changes to
              move closer to your potential ATS
              score.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}


function ScoreCircle({
  label,
  score,
  type
}) {
  const circleStyle =
    type === "potential"
      ? `
        border-emerald-500
        bg-emerald-50

        dark:bg-emerald-950/30
      `
      : `
        border-amber-500
        bg-amber-50

        dark:bg-amber-950/30
      `;

  return (
    <div
      className="
        flex flex-col
        items-center
      "
    >
      <div
        className={`
          flex h-28 w-28
          flex-col items-center
          justify-center
          rounded-full
          border-[9px]

          ${circleStyle}
        `}
      >
        <strong
          className="
            text-3xl
            text-[var(--text-primary)]
          "
        >
          {score}%
        </strong>

        <span
          className="
            mt-1 text-xs
            text-[var(--text-secondary)]
          "
        >
          ATS
        </span>
      </div>

      <p
        className="
          mt-3 text-sm font-semibold
          text-[var(--text-secondary)]
        "
      >
        {label}
      </p>
    </div>
  );
}


function PriorityCard({
  title,
  value,
  description,
  type,
  icon
}) {
  const typeStyles = {
    total: `
      bg-[var(--primary-soft)]
      text-[var(--primary)]
    `,

    high: `
      bg-red-50
      text-red-600

      dark:bg-red-950/30
      dark:text-red-300
    `,

    medium: `
      bg-amber-50
      text-amber-600

      dark:bg-amber-950/30
      dark:text-amber-300
    `,

    success: `
      bg-emerald-50
      text-emerald-600

      dark:bg-emerald-950/30
      dark:text-emerald-300
    `
  };

  return (
    <article
      className="
        app-card
        app-card-hover
        app-card-padding
      "
    >
      <div
        className="
          flex items-start
          justify-between gap-4
        "
      >
        <div>
          <p
            className="
              text-sm font-medium
              text-[var(--text-secondary)]
            "
          >
            {title}
          </p>

          <p
            className="
              mt-3 text-3xl font-bold
              tracking-tight
              text-[var(--text-primary)]
            "
          >
            {value}
          </p>

          <p
            className="
              mt-2 text-sm
              text-[var(--text-muted)]
            "
          >
            {description}
          </p>
        </div>

        <div
          className={`
            flex h-12 w-12
            shrink-0 items-center
            justify-center
            rounded-2xl text-xl

            ${
              typeStyles[type] ||
              typeStyles.total
            }
          `}
        >
          {icon}
        </div>
      </div>
    </article>
  );
}


function MissingSectionsCard({
  sections
}) {
  const safeSections =
    Array.isArray(sections)
      ? sections
      : [];

  return (
    <article
      className="
        rounded-3xl
        border border-[var(--border)]
        bg-[var(--surface)]
        p-6
        shadow-[var(--shadow-sm)]
      "
    >
      <div
        className="
          flex items-start
          justify-between gap-4
        "
      >
        <div className="flex items-center gap-3">
          <div
            className="
              flex h-12 w-12
              items-center justify-center
              rounded-2xl
              bg-red-50
              text-xl text-red-600

              dark:bg-red-950/30
              dark:text-red-300
            "
          >
            <FaFileAlt />
          </div>

          <div>
            <h3
              className="
                text-xl font-bold
                text-[var(--text-primary)]
              "
            >
              Missing Resume Sections
            </h3>

            <p
              className="
                mt-1 text-sm
                text-[var(--text-secondary)]
              "
            >
              Add these sections to improve resume completeness.
            </p>
          </div>
        </div>

        <span
          className="
            rounded-full bg-red-50
            px-3 py-1
            text-sm font-bold text-red-600

            dark:bg-red-950/30
            dark:text-red-300
          "
        >
          {safeSections.length}
        </span>
      </div>

      {safeSections.length > 0 ? (
        <div className="mt-6 space-y-3">
          {safeSections.map(
            (section, index) => (
              <div
                key={`${section}-${index}`}
                className="
                  flex items-center gap-3
                  rounded-2xl
                  border border-red-200
                  bg-red-50 p-4

                  dark:border-red-900/60
                  dark:bg-red-950/20
                "
              >
                <FaExclamationTriangle
                  className="shrink-0 text-red-500"
                />

                <span
                  className="
                    font-semibold text-red-800
                    dark:text-red-300
                  "
                >
                  {section}
                </span>
              </div>
            )
          )}
        </div>
      ) : (
        <div
          className="
            mt-6 flex items-center gap-3
            rounded-2xl
            border border-emerald-200
            bg-emerald-50 p-5

            dark:border-emerald-900/60
            dark:bg-emerald-950/20
          "
        >
          <FaCheckCircle
            className="shrink-0 text-xl text-emerald-500"
          />

          <div>
            <p
              className="
                font-bold text-emerald-800
                dark:text-emerald-300
              "
            >
              All important sections detected
            </p>

            <p
              className="
                mt-1 text-sm text-emerald-700
                dark:text-emerald-400
              "
            >
              Your resume contains the major sections expected by ATS systems.
            </p>
          </div>
        </div>
      )}
    </article>
  );
}


function PrioritySkillsCard({
  skills,
  selectedCareer
}) {
  const safeSkills =
    Array.isArray(skills)
      ? skills
      : [];

  return (
    <article
      className="
        rounded-3xl
        border border-[var(--border)]
        bg-[var(--surface)]
        p-6
        shadow-[var(--shadow-sm)]
      "
    >
      <div
        className="
          flex items-start
          justify-between gap-4
        "
      >
        <div className="flex items-center gap-3">
          <div
            className="
              flex h-12 w-12
              items-center justify-center
              rounded-2xl
              bg-[var(--primary-soft)]
              text-xl text-[var(--primary)]
            "
          >
            <FaTools />
          </div>

          <div>
            <h3
              className="
                text-xl font-bold
                text-[var(--text-primary)]
              "
            >
              Priority Skills
            </h3>

            <p
              className="
                mt-1 text-sm
                text-[var(--text-secondary)]
              "
            >
              Skills that can improve your readiness
              {selectedCareer ? ` for ${selectedCareer}` : ""}.
            </p>
          </div>
        </div>

        <span
          className="
            rounded-full
            bg-[var(--primary-soft)]
            px-3 py-1
            text-sm font-bold
            text-[var(--primary)]
          "
        >
          {safeSkills.length}
        </span>
      </div>

      {safeSkills.length > 0 ? (
        <div className="mt-6 flex flex-wrap gap-3">
          {safeSkills.map(
            (skill, index) => (
              <span
                key={`${skill}-${index}`}
                className="
                  inline-flex items-center gap-2
                  rounded-full
                  border border-[var(--primary)]
                  bg-[var(--primary-soft)]
                  px-4 py-2
                  text-sm font-semibold
                  text-[var(--primary)]
                "
              >
                <FaCheckCircle />
                {skill}
              </span>
            )
          )}
        </div>
      ) : (
        <div
          className="
            mt-6 flex items-center gap-3
            rounded-2xl
            border border-emerald-200
            bg-emerald-50 p-5

            dark:border-emerald-900/60
            dark:bg-emerald-950/20
          "
        >
          <FaCheckCircle
            className="shrink-0 text-xl text-emerald-500"
          />

          <div>
            <p
              className="
                font-bold text-emerald-800
                dark:text-emerald-300
              "
            >
              No priority skill gaps found
            </p>

            <p
              className="
                mt-1 text-sm text-emerald-700
                dark:text-emerald-400
              "
            >
              Your current skills align well with the selected career.
            </p>
          </div>
        </div>
      )}
    </article>
  );
}


function SuggestionsList({
  suggestions
}) {
  const safeSuggestions =
    Array.isArray(suggestions)
      ? suggestions
      : [];

  if (safeSuggestions.length === 0) {
    return (
      <div
        className="
          mt-5 flex items-center gap-4
          rounded-3xl
          border border-emerald-200
          bg-emerald-50 p-6

          dark:border-emerald-900/60
          dark:bg-emerald-950/20
        "
      >
        <div
          className="
            flex h-12 w-12 shrink-0
            items-center justify-center
            rounded-2xl
            bg-emerald-100
            text-xl text-emerald-600

            dark:bg-emerald-950/50
            dark:text-emerald-300
          "
        >
          <FaCheckCircle />
        </div>

        <div>
          <h3
            className="
              font-bold text-emerald-800
              dark:text-emerald-300
            "
          >
            No additional improvements found
          </h3>

          <p
            className="
              mt-1 text-sm leading-6
              text-emerald-700
              dark:text-emerald-400
            "
          >
            Your latest resume already satisfies the
            current improvement checks.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div
      className="
        mt-5 grid gap-5

        xl:grid-cols-2
      "
    >
      {safeSuggestions.map(
        (suggestion, index) => (
          <SuggestionCard
            key={`${
              suggestion.title ||
              suggestion.category ||
              "suggestion"
            }-${index}`}
            suggestion={suggestion}
            index={index}
          />
        )
      )}
    </div>
  );
}


function SuggestionCard({
  suggestion,
  index
}) {
  const [isExpanded, setIsExpanded] =
    useState(index < 2);

  const severity = String(
    suggestion.severity || "low"
  ).toLowerCase();

  const severityStyles = {
    high: {
      label: "High Priority",
      badge: `
        border-red-300
        bg-red-50
        text-red-700

        dark:border-red-900/70
        dark:bg-red-950/30
        dark:text-red-300
      `,
      icon: `
        bg-red-50
        text-red-600

        dark:bg-red-950/30
        dark:text-red-300
      `,
      accent: "border-l-red-500"
    },

    medium: {
      label: "Medium Priority",
      badge: `
        border-amber-300
        bg-amber-50
        text-amber-700

        dark:border-amber-900/70
        dark:bg-amber-950/30
        dark:text-amber-300
      `,
      icon: `
        bg-amber-50
        text-amber-600

        dark:bg-amber-950/30
        dark:text-amber-300
      `,
      accent: "border-l-amber-500"
    },

    low: {
      label: "Low Priority",
      badge: `
        border-blue-300
        bg-blue-50
        text-blue-700

        dark:border-blue-900/70
        dark:bg-blue-950/30
        dark:text-blue-300
      `,
      icon: `
        bg-blue-50
        text-blue-600

        dark:bg-blue-950/30
        dark:text-blue-300
      `,
      accent: "border-l-blue-500"
    }
  };

  const selectedStyle =
    severityStyles[severity] ||
    severityStyles.low;

  const category =
    suggestion.category ||
    "Resume Improvement";

  const title =
    suggestion.title ||
    "Improve this resume area";

  const description =
    suggestion.description ||
    "Review this recommendation and update your resume accordingly.";

  return (
    <article
      className={`
        self-start h-fit
        overflow-hidden rounded-3xl
        border border-[var(--border)]
        border-l-4
        bg-[var(--surface)]
        shadow-[var(--shadow-sm)]
        transition duration-300

        hover:-translate-y-0.5
        hover:shadow-[var(--shadow-md)]

        ${selectedStyle.accent}
      `}
    >
      <button
        type="button"
        onClick={() =>
          setIsExpanded(
            (current) => !current
          )
        }
        aria-expanded={isExpanded}
        className="
          flex w-full items-start
          justify-between gap-4
          p-6 text-left
        "
      >
        <div
          className="
            flex min-w-0 items-start
            gap-4
          "
        >
          <div
            className={`
              flex h-12 w-12 shrink-0
              items-center justify-center
              rounded-2xl text-xl

              ${selectedStyle.icon}
            `}
          >
            {severity === "high" ? (
              <FaExclamationTriangle />
            ) : severity === "medium" ? (
              <FaLightbulb />
            ) : (
              <FaBullseye />
            )}
          </div>

          <div className="min-w-0">
            <div
              className="
                flex flex-wrap
                items-center gap-2
              "
            >
              <span
                className={`
                  rounded-full border
                  px-3 py-1
                  text-xs font-bold

                  ${selectedStyle.badge}
                `}
              >
                {selectedStyle.label}
              </span>

              <span
                className="
                  rounded-full
                  border border-[var(--border)]
                  bg-[var(--surface-soft)]
                  px-3 py-1
                  text-xs font-semibold
                  text-[var(--text-secondary)]
                "
              >
                {category}
              </span>
            </div>

            <h3
              className="
                mt-3 text-lg font-bold
                leading-7
                text-[var(--text-primary)]
              "
            >
              {title}
            </h3>

            <p
              className={`
                mt-2 text-sm leading-6
                text-[var(--text-secondary)]

                ${
                  isExpanded
                    ? ""
                    : "line-clamp-2"
                }
              `}
            >
              {description}
            </p>
          </div>
        </div>

        <span
          className="
            flex h-10 w-10 shrink-0
            items-center justify-center
            rounded-xl
            bg-[var(--surface-soft)]
            text-[var(--text-secondary)]
            transition-transform
            duration-300
          "
        >
          {isExpanded ? (
            <FaChevronUp />
          ) : (
            <FaChevronDown />
          )}
        </span>
      </button>

      {isExpanded && (
        <div
          className="
            border-t border-[var(--border)]
            px-6 pb-6 pt-5
          "
        >
          <div
            className="
              grid gap-4

              sm:grid-cols-2
            "
          >
            <SuggestionDetail
              title="Expected Impact"
              value={
                suggestion.impact ||
                "Improves resume clarity and relevance."
              }
              icon={<FaChartLine />}
            />

            <SuggestionDetail
              title="Priority Order"
              value={`Priority ${
                suggestion.priority ??
                index + 1
              }`}
              icon={<FaBullseye />}
            />
          </div>

          {suggestion.example && (
            <div
              className="
                mt-4 rounded-2xl
                border border-[var(--border)]
                bg-[var(--surface-soft)]
                p-5
              "
            >
              <p
                className="
                  flex items-center gap-2
                  text-sm font-bold
                  text-[var(--primary)]
                "
              >
                <FaMagic />
                Example Improvement
              </p>

              <p
                className="
                  mt-3 whitespace-pre-line
                  text-sm leading-7
                  text-[var(--text-secondary)]
                "
              >
                {suggestion.example}
              </p>
            </div>
          )}

          <div
            className="
              mt-5 flex items-center
              justify-between gap-4
              rounded-2xl
              bg-[var(--primary-soft)]
              p-4
            "
          >
            <div>
              <p
                className="
                  text-sm font-bold
                  text-[var(--primary)]
                "
              >
                Recommended Action
              </p>

              <p
                className="
                  mt-1 text-xs leading-5
                  text-[var(--text-secondary)]
                "
              >
                Apply this change naturally and only
                include skills or achievements you can
                genuinely demonstrate.
              </p>
            </div>

            <FaCheckCircle
              className="
                shrink-0 text-xl
                text-[var(--primary)]
              "
            />
          </div>
        </div>
      )}
    </article>
  );
}

function SuggestionDetail({
  title,
  value,
  icon
}) {
  return (
    <div
      className="
        rounded-2xl
        border border-[var(--border)]
        bg-[var(--surface-soft)]
        p-4
      "
    >
      <p
        className="
          flex items-center gap-2
          text-xs font-bold
          uppercase tracking-[0.08em]
          text-[var(--text-muted)]
        "
      >
        <span
          className="
            text-[var(--primary)]
          "
        >
          {icon}
        </span>

        {title}
      </p>

      <p
        className="
          mt-3 text-sm font-semibold
          leading-6
          text-[var(--text-primary)]
        "
      >
        {value}
      </p>
    </div>
  );
}


export default ResumeImprovement;