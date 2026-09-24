import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaArrowLeft,
  FaChartLine,
  FaCheckCircle,
  FaExclamationTriangle,
  FaFire,
  FaLightbulb,
  FaMapMarkerAlt,
  FaRupeeSign
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

const clampScore = (value) => {
  const numberValue = Number(value) || 0;

  return Math.min(
    Math.max(numberValue, 0),
    100
  );
};

function CareerPrediction() {
  const navigate = useNavigate();

  const [analysis, setAnalysis] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const loadCareerPrediction = async () => {
      setIsLoading(true);
      setErrorMessage("");

      try {
        const data = await getLatestResumeAnalysis();
        setAnalysis(data);
      } catch (error) {
        console.error(
          "Career prediction loading error:",
          error
        );

        if (error.response?.status === 401) {
          localStorage.removeItem("token");
          navigate("/login", { replace: true });
          return;
        }

        setErrorMessage(
          getErrorMessage(
            error,
            "Unable to load career prediction."
          )
        );
      } finally {
        setIsLoading(false);
      }
    };

    loadCareerPrediction();
  }, [navigate]);

  if (isLoading) {
    return (
      <main className="app-page">
        <div className="page-container max-w-[1600px]">
          <div className="state-container">
            <div className="spinner" />

            <p className="state-title">
              Loading career predictions
            </p>

            <p className="state-message">
              We are comparing your resume skills with suitable career paths and market trends.
            </p>
          </div>
        </div>
      </main>
    );
  }

  const predictions = analysis?.career_predictions || [];
  const bestPrediction = predictions[0] || null;

  return (
    <main className="app-page">
      <div className="page-container max-w-[1600px]">
        <header
          className="
            flex flex-col gap-5
            border-b border-[var(--border)]
            pb-7
            sm:flex-row sm:items-center sm:justify-between
          "
        >
          <div>
            <p className="font-semibold text-[var(--primary)]">
              CareerCompass
            </p>

            <h1
              className="
                mt-2 text-3xl font-bold
                text-[var(--text-primary)]
              "
            >
              Career Prediction
            </h1>

            <p
              className="
                mt-2 text-[var(--text-secondary)]
              "
            >
              Career recommendations based on your resume, current demand and market-growth indicators.
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
                  Career prediction unavailable
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
            <section
              className="
                app-card mt-8 overflow-hidden
                border-2 border-[var(--border)]
              "
            >
              <div
                className="
                  grid gap-7 p-7
                  md:grid-cols-[1fr_auto]
                  md:items-center
                  xl:p-9
                "
              >
                <div>
                  <p
                    className="
                      text-sm font-bold
                      text-[var(--primary)]
                    "
                  >
                    Latest analyzed resume
                  </p>

                  <h2
                    className="
                      mt-2 text-2xl font-bold
                      text-[var(--text-primary)]
                    "
                  >
                    {analysis.file_name}
                  </h2>

                  <p
                    className="
                      mt-5 text-sm font-medium
                      text-[var(--text-secondary)]
                    "
                  >
                    Best trend-aware career recommendation
                  </p>

                  <p
                    className="
                      mt-2 text-3xl font-bold
                      text-[var(--primary)]
                      md:text-4xl
                    "
                  >
                    {analysis.best_career ||
                      "No recommendation available"}
                  </p>

                  {bestPrediction && (
                    <div className="mt-5 flex flex-wrap gap-3">
                      <SummaryBadge
                        label="Overall Score"
                        value={`${clampScore(
                          bestPrediction.final_career_score ??
                            bestPrediction.match_percentage
                        )}%`}
                      />

                      <SummaryBadge
                        label="Market Demand"
                        value={`${clampScore(
                          bestPrediction.market_demand_score
                        )}%`}
                      />

                      <SummaryBadge
                        label="Salary Range"
                        value={
                          bestPrediction.salary_range ||
                          "Not available"
                        }
                      />
                    </div>
                  )}
                </div>

                <div
                  className="
                    flex h-28 w-28 items-center justify-center
                    rounded-full border-8
                    border-[var(--primary)]
                    bg-[var(--surface-soft)]
                  "
                >
                  <FaChartLine
                    className="
                      text-4xl text-[var(--primary)]
                    "
                  />
                </div>
              </div>
            </section>

            <section className="mt-8 space-y-6">
              {predictions.length > 0 ? (
                predictions.map((prediction, index) => {
                  const resumeMatch = clampScore(
                    prediction.resume_match_score ??
                      prediction.match_percentage
                  );

                  const overallScore = clampScore(
                    prediction.final_career_score ??
                      prediction.match_percentage
                  );

                  const marketDemand = clampScore(
                    prediction.market_demand_score
                  );

                  const growthScore = clampScore(
                    prediction.growth_score
                  );

                  const trendingSkillScore = clampScore(
                    prediction.trending_skill_score
                  );

                  return (
                    <article
                      key={`${prediction.career}-${index}`}
                      className="
                        app-card app-card-hover
                        border-2 border-[var(--border)]
                        p-6 xl:p-7
                      "
                    >
                      <div
                        className="
                          flex flex-col gap-5
                          md:flex-row md:items-start
                          md:justify-between
                        "
                      >
                        <div>
                          <div className="flex items-center gap-3">
                            <span
                              className="
                                flex h-10 w-10 items-center justify-center
                                rounded-full
                                bg-[var(--primary-soft)]
                                text-sm font-bold
                                text-[var(--primary)]
                              "
                            >
                              {index + 1}
                            </span>

                            <h2
                              className="
                                text-xl font-bold
                                text-[var(--text-primary)]
                              "
                            >
                              {prediction.career}
                            </h2>
                          </div>

                          <p
                            className="
                              mt-4 max-w-4xl leading-7
                              text-[var(--text-secondary)]
                            "
                          >
                            {prediction.description}
                          </p>
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
                            {overallScore}%
                          </p>

                          <p
                            className="
                              text-xs font-medium
                              text-[var(--text-muted)]
                            "
                          >
                            overall career score
                          </p>
                        </div>
                      </div>

                      <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                        <ScoreCard
                          title="Resume Match"
                          score={resumeMatch}
                          description="Match with your existing resume skills"
                        />

                        <ScoreCard
                          title="Market Demand"
                          score={marketDemand}
                          description="Current hiring demand for this career"
                        />

                        <ScoreCard
                          title="Growth Score"
                          score={growthScore}
                          description="Expected future growth potential"
                        />

                        <ScoreCard
                          title="Trending Skills"
                          score={trendingSkillScore}
                          description="Match with in-demand market skills"
                        />
                      </div>

                      <div className="mt-6 grid gap-4 md:grid-cols-3">
                        <MarketInfoCard
                          icon={<FaRupeeSign />}
                          title="Salary Range"
                          value={
                            prediction.salary_range ||
                            "Market data unavailable"
                          }
                        />

                        <MarketInfoCard
                          icon={<FaFire />}
                          title="Demand Level"
                          value={
                            prediction.demand_level ||
                            "Moderate"
                          }
                          secondary={
                            prediction.trend_status ||
                            "Stable"
                          }
                        />

                        <MarketInfoCard
                          icon={<FaMapMarkerAlt />}
                          title="Top Hiring Locations"
                          value={
                            prediction.top_locations?.length > 0
                              ? prediction.top_locations.join(", ")
                              : "Location data unavailable"
                          }
                        />
                      </div>

                      <div className="mt-6 grid gap-6 lg:grid-cols-2">
                        <SkillPanel
                          type="matched"
                          title="Matched Skills"
                          skills={prediction.matched_skills}
                          emptyMessage="No matching skills found."
                        />

                        <SkillPanel
                          type="missing"
                          title="Skills to Learn"
                          skills={prediction.missing_skills}
                          emptyMessage="No major missing skills."
                        />
                      </div>

                      <div className="mt-6 grid gap-6 lg:grid-cols-2">
                        <SkillPanel
                          type="trend"
                          title="Trending Market Skills"
                          skills={prediction.trending_skills}
                          emptyMessage="No trending-skill data available."
                        />

                        <SkillPanel
                          type="matchedTrend"
                          title="Your Trending Skill Matches"
                          skills={prediction.matched_trending_skills}
                          emptyMessage="No trending skills currently matched."
                        />
                      </div>
                    </article>
                  );
                })
              ) : (
                <div className="state-container">
                  <FaChartLine
                    className="
                      text-4xl text-[var(--primary)]
                    "
                  />

                  <p className="state-title">
                    No career predictions found
                  </p>

                  <p className="state-message">
                    Analyze a resume to receive career recommendations.
                  </p>
                </div>
              )}
            </section>
          </>
        ) : null}
      </div>
    </main>
  );
}

function SummaryBadge({ label, value }) {
  return (
    <div
      className="
        rounded-2xl border border-[var(--border)]
        bg-[var(--surface-soft)] px-4 py-3
      "
    >
      <p className="text-xs font-semibold text-[var(--text-muted)]">
        {label}
      </p>

      <p className="mt-1 font-bold text-[var(--text-primary)]">
        {value}
      </p>
    </div>
  );
}

function ScoreCard({ title, score, description }) {
  return (
    <article
      className="
        rounded-2xl border border-[var(--border)]
        bg-[var(--surface-soft)] p-5
      "
    >
      <div className="flex items-start justify-between gap-3">
        <p className="font-semibold text-[var(--text-secondary)]">
          {title}
        </p>

        <span
          className="
            rounded-xl bg-[var(--primary-soft)]
            px-3 py-2 text-sm font-bold
            text-[var(--primary)]
          "
        >
          {score}%
        </span>
      </div>

      <div className="progress-track mt-4">
        <div
          className="progress-value"
          style={{ width: `${score}%` }}
        />
      </div>

      <p className="mt-3 text-xs leading-5 text-[var(--text-muted)]">
        {description}
      </p>
    </article>
  );
}

function MarketInfoCard({ icon, title, value, secondary = "" }) {
  return (
    <article
      className="
        rounded-2xl border border-[var(--border)]
        bg-[var(--surface)] p-5
      "
    >
      <div className="flex items-start gap-3">
        <span
          className="
            flex h-10 w-10 shrink-0 items-center justify-center
            rounded-xl bg-[var(--primary-soft)]
            text-[var(--primary)]
          "
        >
          {icon}
        </span>

        <div>
          <p className="text-sm font-semibold text-[var(--text-muted)]">
            {title}
          </p>

          <p className="mt-1 font-bold leading-6 text-[var(--text-primary)]">
            {value}
          </p>

          {secondary && (
            <p className="mt-1 text-xs text-[var(--text-secondary)]">
              Market trend: {secondary}
            </p>
          )}
        </div>
      </div>
    </article>
  );
}

function SkillPanel({ type, title, skills, emptyMessage }) {
  const styles = {
    matched: {
      container:
        "border-green-300 bg-green-50 dark:border-green-900/70 dark:bg-green-950/30",
      heading: "text-green-800 dark:text-green-300",
      badge:
        "border-green-400 bg-white text-green-800 dark:border-green-800 dark:bg-green-950/50 dark:text-green-300",
      icon: <FaCheckCircle />
    },
    missing: {
      container:
        "border-amber-300 bg-amber-50 dark:border-amber-900/70 dark:bg-amber-950/30",
      heading: "text-amber-800 dark:text-amber-300",
      badge:
        "border-amber-400 bg-white text-amber-800 dark:border-amber-800 dark:bg-amber-950/50 dark:text-amber-300",
      icon: <FaLightbulb />
    },
    trend: {
      container:
        "border-blue-300 bg-blue-50 dark:border-blue-900/70 dark:bg-blue-950/30",
      heading: "text-blue-800 dark:text-blue-300",
      badge:
        "border-blue-400 bg-white text-blue-800 dark:border-blue-800 dark:bg-blue-950/50 dark:text-blue-300",
      icon: <FaFire />
    },
    matchedTrend: {
      container:
        "border-teal-300 bg-teal-50 dark:border-teal-900/70 dark:bg-teal-950/30",
      heading: "text-teal-800 dark:text-teal-300",
      badge:
        "border-teal-400 bg-white text-teal-800 dark:border-teal-800 dark:bg-teal-950/50 dark:text-teal-300",
      icon: <FaChartLine />
    }
  };

  const selectedStyle = styles[type] || styles.matched;

  return (
    <div
      className={`
        rounded-2xl border p-5
        ${selectedStyle.container}
      `}
    >
      <h3
        className={`
          flex items-center gap-2 font-bold
          ${selectedStyle.heading}
        `}
      >
        {selectedStyle.icon}
        {title}
      </h3>

      <div className="mt-4 flex flex-wrap gap-2">
        {skills?.length > 0 ? (
          skills.map((skill) => (
            <span
              key={skill}
              className={`
                rounded-full border px-3 py-1.5
                text-xs font-semibold
                ${selectedStyle.badge}
              `}
            >
              {skill}
            </span>
          ))
        ) : (
          <p className="text-sm text-[var(--text-secondary)]">
            {emptyMessage}
          </p>
        )}
      </div>
    </div>
  );
}

export default CareerPrediction;