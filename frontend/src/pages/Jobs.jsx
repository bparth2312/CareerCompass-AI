import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaArrowLeft,
  FaBriefcase,
  FaBuilding,
  FaCheckCircle,
  FaClock,
  FaExclamationTriangle,
  FaFire,
  FaMapMarkerAlt,
  FaMoneyBillWave,
  FaStar
} from "react-icons/fa";

import ThemeToggle from "../components/ThemeToggle/ThemeToggle";

import {
  getLatestResumeAnalysis
} from "../services/resumeService";


const getErrorMessage = (
  error,
  fallbackMessage
) => {
  const detail = error.response?.data?.detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map(
        (item) =>
          item?.msg || "Validation error"
      )
      .join(", ");
  }

  return fallbackMessage;
};


const clampScore = (value) =>
  Math.min(
    Math.max(
      Number(value) || 0,
      0
    ),
    100
  );


const formatUpdatedTime = (value) => {
  if (!value) {
    return "Not available";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "Not available";
  }

  return date.toLocaleString();
};


function Jobs() {
  const navigate = useNavigate();

  const [analysis, setAnalysis] =
    useState(null);

  const [isLoading, setIsLoading] =
    useState(true);

  const [errorMessage, setErrorMessage] =
    useState("");

  useEffect(() => {
    const loadJobRecommendations =
      async () => {
        setIsLoading(true);
        setErrorMessage("");

        try {
          const data =
            await getLatestResumeAnalysis();

          setAnalysis(data);
        } catch (error) {
          console.error(
            "Job recommendations loading error:",
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
              "Unable to load job recommendations."
            )
          );
        } finally {
          setIsLoading(false);
        }
      };

    loadJobRecommendations();
  }, [navigate]);

  const jobData = useMemo(
    () =>
      analysis?.job_recommendations ||
      {},
    [analysis]
  );

  const recommendations = useMemo(
    () =>
      Array.isArray(jobData)
        ? jobData
        : jobData.recommendations ||
          [],
    [jobData]
  );

  const bestJob =
    jobData.best_job ||
    analysis?.best_job ||
    "No recommendation available";

  const bestRecommendation =
    recommendations[0] || null;

  if (isLoading) {
    return (
      <main className="app-page">
        <div className="page-container max-w-[1600px]">
          <div className="state-container">
            <div className="spinner" />

            <p className="state-title">
              Loading job recommendations
            </p>

            <p className="state-message">
              We are preparing suitable job
              roles using your resume and current
              market data.
            </p>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="app-page">
      <div className="page-container max-w-[1600px]">
        <header
          className="
            flex flex-col gap-5
            border-b border-[var(--border)]
            pb-6

            md:flex-row
            md:items-center
            md:justify-between
          "
        >
          <div>
            <p
              className="
                text-sm font-semibold
                text-[var(--primary)]
              "
            >
              CareerCompass
            </p>

            <h1 className="page-title mt-2">
              Recommended Jobs
            </h1>

            <p className="page-subtitle">
              Explore suitable job roles based on
              your resume, career readiness and
              current market demand.
            </p>
          </div>

          <div className="flex items-center gap-3">
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

        {errorMessage ? (
          <section
            className="
              mt-8 rounded-2xl
              border border-red-300
              bg-red-50 p-6
              text-red-800

              dark:border-red-900/70
              dark:bg-red-950/30
              dark:text-red-300
            "
          >
            <div className="flex items-start gap-3">
              <FaExclamationTriangle className="mt-1 shrink-0" />

              <div>
                <h2 className="font-semibold">
                  Job recommendations unavailable
                </h2>

                <p className="mt-2 text-sm">
                  {errorMessage}
                </p>

                <button
                  type="button"
                  onClick={() =>
                    navigate("/resume")
                  }
                  className="btn-primary mt-5"
                >
                  Upload and Analyze Resume
                </button>
              </div>
            </div>
          </section>
        ) : analysis ? (
          <>
            <section
              className="
                app-card mt-8 overflow-hidden
              "
            >
              <div
                className="
                  grid gap-6 p-7

                  md:grid-cols-[1fr_auto]
                  md:items-center

                  xl:p-9
                "
              >
                <div>
                  <span className="badge badge-primary">
                    <FaStar />
                    Best Job Match
                  </span>

                  <h2
                    className="
                      mt-5 text-3xl font-bold
                      tracking-tight
                      text-[var(--text-primary)]

                      md:text-4xl
                    "
                  >
                    {bestJob}
                  </h2>

                  <p
                    className="
                      mt-4 max-w-3xl
                      leading-7
                      text-[var(--text-secondary)]
                    "
                  >
                    Recommendations combine your
                    skills, predicted career path,
                    readiness score and live job
                    market information.
                  </p>

                  {bestRecommendation && (
                    <div
                      className="
                        mt-6 flex flex-wrap gap-3
                      "
                    >
                      <SummaryPill
                        label="Final Score"
                        value={`${clampScore(
                          bestRecommendation.recommendation_score
                        )}%`}
                      />

                      <SummaryPill
                        label="Live Jobs"
                        value={
                          bestRecommendation.live_job_count ??
                          0
                        }
                      />

                      <SummaryPill
                        label="Salary"
                        value={
                          bestRecommendation.salary_range ||
                          "Unavailable"
                        }
                      />

                      <SummaryPill
                        label="Demand"
                        value={
                          bestRecommendation.demand_level ||
                          "Unavailable"
                        }
                      />
                    </div>
                  )}
                </div>

                <div
                  className="
                    flex h-28 w-28
                    items-center justify-center
                    rounded-full
                    border-8 border-[var(--primary)]
                    bg-[var(--surface-soft)]
                    text-4xl
                    text-[var(--primary)]
                  "
                >
                  <FaBriefcase />
                </div>
              </div>
            </section>

            <section className="mt-8 space-y-6">
              {recommendations.length > 0 ? (
                recommendations.map(
                  (job, index) => {
                    const recommendationScore =
                      clampScore(
                        job.recommendation_score
                      );

                    const matchPercentage =
                      clampScore(
                        job.match_percentage
                      );

                    const marketDemandScore =
                      clampScore(
                        job.market_demand_score
                      );

                    const trendingSkillScore =
                      clampScore(
                        job.trending_skill_score
                      );

                    const readinessScore =
                      clampScore(
                        job.readiness_score
                      );

                    return (
                      <article
                        key={`${job.job_title}-${index}`}
                        className="
                          app-card app-card-hover
                          p-6 xl:p-7
                        "
                      >
                        <div
                          className="
                            flex flex-col gap-5

                            md:flex-row
                            md:items-start
                            md:justify-between
                          "
                        >
                          <div className="flex items-start gap-4">
                            <span
                              className="
                                flex h-11 w-11
                                shrink-0 items-center
                                justify-center
                                rounded-full
                                bg-[var(--primary-soft)]
                                font-bold
                                text-[var(--primary)]
                              "
                            >
                              {index + 1}
                            </span>

                            <div>
                              <h2
                                className="
                                  text-2xl font-bold
                                  tracking-tight
                                  text-[var(--text-primary)]
                                "
                              >
                                {job.job_title}
                              </h2>

                              <div
                                className="
                                  mt-3 flex flex-wrap gap-2
                                "
                              >
                                {job.career_category && (
                                  <span className="badge badge-primary">
                                    {job.career_category}
                                  </span>
                                )}

                                {job.experience_level && (
                                  <span
                                    className="
                                      badge
                                      border border-blue-200
                                      bg-blue-50
                                      text-blue-800

                                      dark:border-blue-900/60
                                      dark:bg-blue-950/30
                                      dark:text-blue-300
                                    "
                                  >
                                    {job.experience_level}
                                  </span>
                                )}

                                {job.application_status && (
                                  <span className="badge badge-success">
                                    {job.application_status}
                                  </span>
                                )}

                                {job.live_data_available ? (
                                  <span
                                    className="
                                      badge
                                      border border-emerald-200
                                      bg-emerald-50
                                      text-emerald-800

                                      dark:border-emerald-900/60
                                      dark:bg-emerald-950/30
                                      dark:text-emerald-300
                                    "
                                  >
                                    Live Market Data
                                  </span>
                                ) : (
                                  <span
                                    className="
                                      badge
                                      border border-slate-200
                                      bg-slate-50
                                      text-slate-700

                                      dark:border-slate-800
                                      dark:bg-slate-900/40
                                      dark:text-slate-300
                                    "
                                  >
                                    Local Calculation
                                  </span>
                                )}
                              </div>

                              <p
                                className="
                                  mt-4 max-w-4xl
                                  leading-7
                                  text-[var(--text-secondary)]
                                "
                              >
                                {job.description}
                              </p>
                            </div>
                          </div>

                          <div
                            className="
                              shrink-0 rounded-2xl
                              border border-[var(--border)]
                              bg-[var(--surface-soft)]
                              px-5 py-4
                              md:text-right
                            "
                          >
                            <p
                              className="
                                text-3xl font-bold
                                text-[var(--primary)]
                              "
                            >
                              {recommendationScore}%
                            </p>

                            <p
                              className="
                                mt-1 text-xs
                                text-[var(--text-muted)]
                              "
                            >
                              final job score
                            </p>
                          </div>
                        </div>

                        <div
                          className="
                            mt-6 grid gap-4

                            sm:grid-cols-2
                            xl:grid-cols-4
                          "
                        >
                          <MetricCard
                            title="Resume Match"
                            value={`${matchPercentage}%`}
                            score={matchPercentage}
                          />

                          <MetricCard
                            title="Market Demand"
                            value={`${marketDemandScore}%`}
                            score={marketDemandScore}
                          />

                          <MetricCard
                            title="Trending Skill Match"
                            value={`${trendingSkillScore}%`}
                            score={trendingSkillScore}
                          />

                          <MetricCard
                            title="Readiness"
                            value={`${readinessScore}%`}
                            score={readinessScore}
                          />
                        </div>

                        <div
                          className="
                            mt-6 grid gap-4

                            sm:grid-cols-2
                            xl:grid-cols-4
                          "
                        >
                          <MarketInfoCard
                            icon={<FaBriefcase />}
                            label="Live Jobs"
                            value={
                              job.live_job_count ??
                              0
                            }
                          />

                          <MarketInfoCard
                            icon={<FaMoneyBillWave />}
                            label="Average Salary"
                            value={
                              job.salary_range ||
                              "Unavailable"
                            }
                          />

                          <MarketInfoCard
                            icon={<FaFire />}
                            label="Demand Level"
                            value={
                              job.demand_level ||
                              "Unavailable"
                            }
                          />

                          <MarketInfoCard
                            icon={<FaClock />}
                            label="Last Updated"
                            value={formatUpdatedTime(
                              job.market_data_updated_at
                            )}
                          />
                        </div>

                        <div
                          className="
                            mt-6 grid gap-6

                            lg:grid-cols-2
                          "
                        >
                          <SkillPanel
                            title="Matched Skills"
                            icon={<FaCheckCircle />}
                            tone="success"
                            skills={
                              job.matched_skills ||
                              []
                            }
                            emptyMessage="No matching skills found."
                          />

                          <SkillPanel
                            title="Skills to Improve"
                            tone="warning"
                            skills={
                              job.missing_skills ||
                              []
                            }
                            emptyMessage="No major missing skills."
                          />
                        </div>

                        <div
                          className="
                            mt-6 grid gap-6

                            lg:grid-cols-2
                          "
                        >
                          <ListPanel
                            title="Top Hiring Companies"
                            icon={<FaBuilding />}
                            items={
                              job.top_companies ||
                              []
                            }
                            emptyMessage="Company information is unavailable."
                          />

                          <ListPanel
                            title="Top Hiring Locations"
                            icon={<FaMapMarkerAlt />}
                            items={
                              job.top_locations ||
                              []
                            }
                            emptyMessage="Location information is unavailable."
                          />
                        </div>

                        <div className="mt-6">
                          <SkillPanel
                            title="Trending Market Skills"
                            icon={<FaFire />}
                            tone="primary"
                            skills={
                              job.trending_skills ||
                              []
                            }
                            emptyMessage="Trending skill data is unavailable."
                          />
                        </div>

                        {job.preparation_advice && (
                          <div
                            className="
                              mt-6 rounded-2xl
                              border border-blue-200
                              bg-blue-50 p-5

                              dark:border-blue-900/60
                              dark:bg-blue-950/30
                            "
                          >
                            <h3
                              className="
                                font-semibold
                                text-blue-800

                                dark:text-blue-300
                              "
                            >
                              Application Advice
                            </h3>

                            <p
                              className="
                                mt-3 leading-7
                                text-blue-900/80

                                dark:text-blue-200/80
                              "
                            >
                              {job.preparation_advice}
                            </p>
                          </div>
                        )}

                        <div
                          className="
                            mt-5 flex flex-wrap
                            items-center justify-between
                            gap-3 border-t
                            border-[var(--border)]
                            pt-4 text-xs
                            text-[var(--text-muted)]
                          "
                        >
                          <span>
                            Data source:{" "}
                            {job.market_data_source ||
                              "Local calculation"}
                          </span>

                          <span>
                            Live data:{" "}
                            {job.live_data_available
                              ? "Available"
                              : "Unavailable"}
                          </span>
                        </div>
                      </article>
                    );
                  }
                )
              ) : (
                <div className="state-container">
                  <FaBriefcase
                    className="
                      text-4xl
                      text-[var(--primary)]
                    "
                  />

                  <p className="state-title">
                    No job recommendations found
                  </p>

                  <p className="state-message">
                    Analyze a recent resume to
                    receive suitable job role
                    recommendations.
                  </p>

                  <button
                    type="button"
                    onClick={() =>
                      navigate("/resume")
                    }
                    className="btn-primary mt-2"
                  >
                    Analyze Resume
                  </button>
                </div>
              )}
            </section>
          </>
        ) : null}
      </div>
    </main>
  );
}


function SummaryPill({
  label,
  value
}) {
  return (
    <div
      className="
        rounded-2xl
        border border-[var(--border)]
        bg-[var(--surface-soft)]
        px-4 py-3
      "
    >
      <p
        className="
          text-xs font-medium
          text-[var(--text-muted)]
        "
      >
        {label}
      </p>

      <p
        className="
          mt-1 font-bold
          text-[var(--text-primary)]
        "
      >
        {value}
      </p>
    </div>
  );
}


function MetricCard({
  title,
  value,
  score
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
      <div
        className="
          flex items-center
          justify-between gap-3
        "
      >
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
            font-bold
            text-[var(--primary)]
          "
        >
          {value}
        </p>
      </div>

      <div className="progress-track mt-3">
        <div
          className="progress-value"
          style={{
            width: `${clampScore(
              score
            )}%`
          }}
        />
      </div>
    </div>
  );
}


function MarketInfoCard({
  icon,
  label,
  value
}) {
  return (
    <div
      className="
        rounded-2xl
        border border-[var(--border)]
        bg-[var(--surface)]
        p-5
      "
    >
      <div
        className="
          flex items-start gap-3
        "
      >
        <span
          className="
            mt-0.5 text-lg
            text-[var(--primary)]
          "
        >
          {icon}
        </span>

        <div className="min-w-0">
          <p
            className="
              text-xs font-medium
              text-[var(--text-muted)]
            "
          >
            {label}
          </p>

          <p
            className="
              mt-1 break-words
              font-bold
              text-[var(--text-primary)]
            "
          >
            {value}
          </p>
        </div>
      </div>
    </div>
  );
}


function ListPanel({
  title,
  icon,
  items,
  emptyMessage
}) {
  return (
    <div
      className="
        rounded-2xl
        border border-[var(--border)]
        bg-[var(--surface-soft)]
        p-5
      "
    >
      <h3
        className="
          flex items-center gap-2
          font-semibold
          text-[var(--text-primary)]
        "
      >
        <span className="text-[var(--primary)]">
          {icon}
        </span>

        {title}
      </h3>

      {items.length > 0 ? (
        <ul className="mt-4 space-y-2">
          {items.map((item) => (
            <li
              key={item}
              className="
                rounded-xl
                border border-[var(--border)]
                bg-[var(--surface)]
                px-3 py-2
                text-sm
                text-[var(--text-secondary)]
              "
            >
              {item}
            </li>
          ))}
        </ul>
      ) : (
        <p
          className="
            mt-4 text-sm
            text-[var(--text-secondary)]
          "
        >
          {emptyMessage}
        </p>
      )}
    </div>
  );
}


function SkillPanel({
  title,
  icon,
  tone,
  skills,
  emptyMessage
}) {
  const toneStyles = {
    success: {
      wrapper:
        "border-green-200 bg-green-50 dark:border-green-900/60 dark:bg-green-950/30",
      title:
        "text-green-800 dark:text-green-300",
      chip:
        "border-green-300 bg-white text-green-800 dark:border-green-800 dark:bg-green-950/40 dark:text-green-300"
    },

    warning: {
      wrapper:
        "border-amber-200 bg-amber-50 dark:border-amber-900/60 dark:bg-amber-950/30",
      title:
        "text-amber-800 dark:text-amber-300",
      chip:
        "border-amber-300 bg-white text-amber-800 dark:border-amber-800 dark:bg-amber-950/40 dark:text-amber-300"
    },

    primary: {
      wrapper:
        "border-teal-200 bg-teal-50 dark:border-teal-900/60 dark:bg-teal-950/30",
      title:
        "text-teal-800 dark:text-teal-300",
      chip:
        "border-teal-300 bg-white text-teal-800 dark:border-teal-800 dark:bg-teal-950/40 dark:text-teal-300"
    }
  };

  const selectedTone =
    toneStyles[tone] ||
    toneStyles.warning;

  return (
    <div
      className={`
        rounded-2xl border p-5
        ${selectedTone.wrapper}
      `}
    >
      <h3
        className={`
          flex items-center gap-2
          font-semibold
          ${selectedTone.title}
        `}
      >
        {icon}
        {title}
      </h3>

      <div className="mt-4 flex flex-wrap gap-2">
        {skills.length > 0 ? (
          skills.map((skill) => (
            <span
              key={skill}
              className={`
                rounded-full border
                px-3 py-1.5
                text-xs font-medium
                ${selectedTone.chip}
              `}
            >
              {skill}
            </span>
          ))
        ) : (
          <p
            className="
              text-sm
              text-[var(--text-secondary)]
            "
          >
            {emptyMessage}
          </p>
        )}
      </div>
    </div>
  );
}


export default Jobs;