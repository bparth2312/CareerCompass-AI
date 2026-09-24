import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaArrowLeft,
  FaBookOpen,
  FaCheckCircle,
  FaClock,
  FaExternalLinkAlt,
  FaExclamationTriangle,
  FaEye,
  FaGraduationCap,
  FaSearch,
  FaYoutube
} from "react-icons/fa";

import ThemeToggle from "../components/ThemeToggle/ThemeToggle";

import {
  getLatestLearningResources
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


function LearningRecommendations() {
  const navigate = useNavigate();

  const [data, setData] =
    useState(null);

  const [isLoading, setIsLoading] =
    useState(true);

  const [errorMessage, setErrorMessage] =
    useState("");

  const [searchTerm, setSearchTerm] =
    useState("");


  useEffect(() => {
    const loadResources = async () => {
      setIsLoading(true);
      setErrorMessage("");

      try {
        const response =
          await getLatestLearningResources();

        setData(response);
      } catch (error) {
        console.error(
          "Learning resources error:",
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
            "Unable to load learning resources."
          )
        );
      } finally {
        setIsLoading(false);
      }
    };

    loadResources();
  }, [navigate]);


  const filteredRecommendations =
    useMemo(() => {
      const recommendations =
        data?.recommendations || [];

      const normalizedSearch =
        searchTerm
          .trim()
          .toLowerCase();

      if (!normalizedSearch) {
        return recommendations;
      }

      return recommendations
        .map((group) => {
          const matchingResources =
            (group.resources || []).filter(
              (resource) => {
                const searchableText = [
                  group.skill,
                  resource.title,
                  resource.description,
                  resource.provider,
                  resource.platform
                ]
                  .filter(Boolean)
                  .join(" ")
                  .toLowerCase();

                return searchableText.includes(
                  normalizedSearch
                );
              }
            );

          const skillMatches =
            group.skill
              ?.toLowerCase()
              .includes(
                normalizedSearch
              );

          if (
            skillMatches &&
            matchingResources.length === 0
          ) {
            return group;
          }

          return {
            ...group,
            resources:
              matchingResources,
            total_resources:
              matchingResources.length
          };
        })
        .filter(
          (group) =>
            group.resources?.length > 0 ||
            group.skill
              ?.toLowerCase()
              .includes(
                normalizedSearch
              )
        );
    }, [
      data,
      searchTerm
    ]);


  const totalResources =
    filteredRecommendations.reduce(
      (total, group) =>
        total +
        (group.resources?.length || 0),
      0
    );


  if (isLoading) {
    return (
      <main className="app-page">
        <div className="page-container max-w-[1600px]">
          <div className="state-container">
            <div className="spinner" />

            <p className="state-title">
              Finding learning resources
            </p>

            <p className="state-message">
              We are preparing recent courses and free
              resources for your missing skills.
            </p>
          </div>
        </div>
      </main>
    );
  }


  return (
    <main className="app-page">
      <div className="page-container max-w-[1600px]">

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
              CareerCompass
            </p>

            <h1
              className="
                mt-2 text-3xl font-bold
                tracking-tight
                text-[var(--text-primary)]

                md:text-4xl
              "
            >
              Learning Recommendations
            </h1>

            <p
              className="
                mt-3 max-w-3xl
                leading-7
                text-[var(--text-secondary)]
              "
            >
              Explore recent courses, tutorials and free
              resources based on the skills you need to
              improve.
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


        {/* Error state */}
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
              <FaExclamationTriangle
                className="mt-1 shrink-0"
              />

              <div>
                <h2 className="font-semibold">
                  Learning resources unavailable
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
                  Analyze Resume
                </button>
              </div>
            </div>
          </section>
        ) : (
          <>
            {/* Target career */}
            <section
              className="
                mt-8 overflow-hidden
                rounded-3xl
                border border-[var(--border)]
                bg-[var(--surface)]
                shadow-[var(--shadow-sm)]
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
                  <span
                    className="
                      inline-flex items-center gap-2
                      rounded-full
                      border border-teal-300
                      bg-teal-50
                      px-3 py-1.5
                      text-xs font-bold
                      uppercase
                      tracking-[0.08em]
                      text-teal-800

                      dark:border-teal-900/70
                      dark:bg-teal-950/40
                      dark:text-teal-300
                    "
                  >
                    Target Career
                  </span>

                  <h2
                    className="
                      mt-4 text-3xl font-bold
                      tracking-tight
                      text-[var(--text-primary)]

                      md:text-4xl
                    "
                  >
                    {data?.target_career ||
                      "Career Development"}
                  </h2>

                  <p
                    className="
                      mt-3
                      text-[var(--text-secondary)]
                    "
                  >
                    Resume:{" "}
                    <span
                      className="
                        font-semibold
                        text-[var(--text-primary)]
                      "
                    >
                      {data?.file_name ||
                        "Latest analyzed resume"}
                    </span>
                  </p>
                </div>

                <div
                  className="
                    flex h-20 w-20
                    items-center justify-center
                    rounded-2xl
                    border border-teal-300
                    bg-teal-50
                    text-3xl text-teal-700

                    dark:border-teal-900/70
                    dark:bg-teal-950/40
                    dark:text-teal-300
                  "
                >
                  <FaBookOpen />
                </div>
              </div>
            </section>


            {/* Search and summary */}
            <section
              className="
                mt-8 grid gap-5

                lg:grid-cols-[1fr_auto]
                lg:items-center
              "
            >
              <div className="relative">
                <FaSearch
                  className="
                    pointer-events-none
                    absolute left-4 top-1/2
                    z-10 -translate-y-1/2
                    text-[var(--text-muted)]
                  "
                />

                <input
                  type="search"
                  value={searchTerm}
                  onChange={(event) =>
                    setSearchTerm(
                      event.target.value
                    )
                  }
                  placeholder="Search skills, courses or providers..."
                  className="form-input"
                  style={{
                    paddingLeft: "2.9rem"
                  }}
                />
              </div>

              <div
                className="
                  flex flex-wrap gap-3
                "
              >
                <SummaryBadge
                  label="Skills"
                  value={
                    filteredRecommendations.length
                  }
                />

                <SummaryBadge
                  label="Resources"
                  value={totalResources}
                />
              </div>
            </section>


            {/* Recommendations */}
            <section className="mt-8 space-y-7">
              {filteredRecommendations.length > 0 ? (
                filteredRecommendations.map(
                  (group) => (
                    <article
                      key={group.skill}
                      className="
                        overflow-hidden
                        rounded-3xl
                        border border-[var(--border)]
                        bg-[var(--surface)]
                        shadow-[var(--shadow-sm)]
                      "
                    >
                      <div
                        className="
                          flex flex-col gap-4
                          border-b border-[var(--border)]
                          bg-[var(--surface-soft)]
                          p-6

                          sm:flex-row
                          sm:items-center
                          sm:justify-between
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
                              shrink-0 items-center
                              justify-center
                              rounded-2xl
                              bg-[var(--primary-soft)]
                              text-xl
                              text-[var(--primary)]
                            "
                          >
                            <FaBookOpen />
                          </div>

                          <div>
                            <h2
                              className="
                                text-2xl font-bold
                                text-[var(--text-primary)]
                              "
                            >
                              Learn {group.skill}
                            </h2>

                            <p
                              className="
                                mt-1 text-sm
                                text-[var(--text-secondary)]
                              "
                            >
                              {group.resources?.length ||
                                group.total_resources ||
                                0}{" "}
                              resources found
                            </p>
                          </div>
                        </div>

                        <span
                          className="
                            w-fit rounded-full
                            border border-teal-300
                            bg-teal-50
                            px-3 py-1.5
                            text-xs font-bold
                            text-teal-800

                            dark:border-teal-900/70
                            dark:bg-teal-950/40
                            dark:text-teal-300
                          "
                        >
                          {group.skill}
                        </span>
                      </div>


                      <div
                        className="
                          grid gap-5 p-6

                          md:grid-cols-2
                          xl:grid-cols-3
                        "
                      >
                        {(group.resources || []).map(
                          (
                            resource,
                            index
                          ) => (
                            <ResourceCard
                              key={`${resource.provider}-${index}`}
                              resource={resource}
                            />
                          )
                        )}
                      </div>
                    </article>
                  )
                )
              ) : (
                <div className="state-container">
                  <FaSearch
                    className="
                      text-4xl
                      text-[var(--primary)]
                    "
                  />

                  <p className="state-title">
                    No matching resources found
                  </p>

                  <p className="state-message">
                    Try searching with a different skill,
                    course name or provider.
                  </p>
                </div>
              )}
            </section>
          </>
        )}
      </div>
    </main>
  );
}


function SummaryBadge({
  label,
  value
}) {
  return (
    <div
      className="
        min-w-[120px]
        rounded-2xl
        border border-[var(--border)]
        bg-[var(--surface)]
        px-5 py-3
        shadow-[var(--shadow-sm)]
      "
    >
      <p
        className="
          text-xs font-semibold
          uppercase tracking-[0.08em]
          text-[var(--text-muted)]
        "
      >
        {label}
      </p>

      <p
        className="
          mt-1 text-xl font-bold
          text-[var(--text-primary)]
        "
      >
        {value}
      </p>
    </div>
  );
}
function formatFrontendViews(
  value
) {
  const views = Number(value);

  if (
    !Number.isFinite(views) ||
    views <= 0
  ) {
    return null;
  }

  if (views >= 10_000_000) {
    return `${(
      views / 10_000_000
    ).toFixed(1)}Cr`;
  }

  if (views >= 100_000) {
    return `${(
      views / 100_000
    ).toFixed(1)}L`;
  }

  if (views >= 1_000) {
    return `${(
      views / 1_000
    ).toFixed(1)}K`;
  }

  return String(views);
}

function ResourceCard({
  resource
}) {
  const publishedDate =
    resource.published_at
      ? new Date(
          resource.published_at
        ).toLocaleDateString(
          "en-IN",
          {
            day: "2-digit",
            month: "short",
            year: "numeric"
          }
        )
      : null;

  const isYouTube =
    resource.platform === "YouTube";

  const isTrusted =
    Boolean(
      resource.is_trusted_channel
    );

  const isFree =
    resource.free === true;

  const formattedViews =
    resource.formatted_views ||
    formatFrontendViews(
      resource.view_count
    );

  const resourceType =
    resource.resource_type ||
    resource.platform ||
    "Learning Resource";

  return (
    <a
      href={resource.url}
      target="_blank"
      rel="noreferrer"
      className="
        group flex h-full flex-col
        overflow-hidden
        rounded-2xl
        border border-[var(--border)]
        bg-[var(--surface)]
        shadow-[var(--shadow-sm)]
        transition duration-300

        hover:-translate-y-1.5
        hover:border-[var(--primary)]
        hover:shadow-[var(--shadow-md)]
      "
    >
      {/* Thumbnail */}
      <div
        className="
          relative overflow-hidden
          bg-[var(--surface-muted)]
        "
      >
        {resource.thumbnail ? (
          <img
            src={resource.thumbnail}
            alt={
              resource.title ||
              "Learning resource"
            }
            loading="lazy"
            className="
              h-48 w-full
              object-cover
              transition duration-300

              group-hover:scale-[1.04]
            "
          />
        ) : (
          <div
            className="
              flex h-48 items-center
              justify-center
              bg-gradient-to-br
              from-teal-50 to-emerald-100
              text-5xl text-teal-700

              dark:from-teal-950/40
              dark:to-emerald-950/30
              dark:text-teal-300
            "
          >
            {resource.platform ===
            "Coursera" ? (
              <FaGraduationCap />
            ) : (
              <FaBookOpen />
            )}
          </div>
        )}

        {/* YouTube icon */}
        {isYouTube && (
          <div
            className="
              absolute right-3 top-3
              flex h-9 w-9
              items-center justify-center
              rounded-full
              bg-red-600
              text-white
              shadow-lg
            "
            title="YouTube video"
          >
            <FaYoutube />
          </div>
        )}

        {/* Trusted badge */}
        {isTrusted && (
          <span
            className="
              absolute left-3 top-3
              inline-flex items-center gap-1.5
              rounded-full
              border border-emerald-300
              bg-emerald-50/95
              px-2.5 py-1
              text-[11px] font-bold
              text-emerald-800
              shadow-sm
              backdrop-blur

              dark:border-emerald-800
              dark:bg-emerald-950/90
              dark:text-emerald-300
            "
          >
            <FaCheckCircle />
            Trusted
          </span>
        )}

        {/* Duration badge */}
        {resource.duration && (
          <span
            className="
              absolute bottom-3 right-3
              inline-flex items-center gap-1.5
              rounded-md
              bg-slate-950/90
              px-2 py-1
              text-xs font-semibold
              text-white
            "
          >
            <FaClock />
            {resource.duration}
          </span>
        )}
      </div>

      {/* Card body */}
      <div
        className="
          flex flex-1 flex-col p-5
        "
      >
        {/* Provider and platform */}
        <div
          className="
            flex flex-wrap
            items-center gap-2
          "
        >
          <span
            className="
              rounded-full
              border border-teal-300
              bg-teal-50
              px-3 py-1
              text-xs font-bold
              text-teal-800

              dark:border-teal-900/70
              dark:bg-teal-950/40
              dark:text-teal-300
            "
          >
            {resource.provider ||
              "Learning Resource"}
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
            {resourceType}
          </span>

          <span
            className={`
              rounded-full
              border px-3 py-1
              text-xs font-bold

              ${
                isFree
                  ? `
                    border-emerald-300
                    bg-emerald-50
                    text-emerald-800

                    dark:border-emerald-900/70
                    dark:bg-emerald-950/40
                    dark:text-emerald-300
                  `
                  : `
                    border-amber-300
                    bg-amber-50
                    text-amber-800

                    dark:border-amber-900/70
                    dark:bg-amber-950/40
                    dark:text-amber-300
                  `
              }
            `}
          >
            {isFree
              ? "Free"
              : "May be paid"}
          </span>
        </div>

        {/* Title */}
        <h3
          className="
            mt-4 line-clamp-2
            text-lg font-bold
            leading-6
            text-[var(--text-primary)]
          "
        >
          {resource.title}
        </h3>

        {/* Description */}
        {resource.description && (
          <p
            className="
              mt-3 line-clamp-3
              text-sm leading-6
              text-[var(--text-secondary)]
            "
          >
            {resource.description}
          </p>
        )}

        {/* Video information */}
        <div
          className="
            mt-4 flex flex-wrap
            items-center gap-x-4 gap-y-2
            text-xs
            text-[var(--text-muted)]
          "
        >
          {isYouTube &&
            formattedViews && (
              <span
                className="
                  inline-flex
                  items-center gap-1.5
                "
              >
                <FaEye />
                {formattedViews} views
              </span>
            )}

          {resource.duration && (
            <span
              className="
                inline-flex
                items-center gap-1.5
              "
            >
              <FaClock />
              {resource.duration}
            </span>
          )}

          {publishedDate && (
            <span>
              Published: {publishedDate}
            </span>
          )}
        </div>

        {/* Open link */}
        <span
          className="
            mt-auto flex items-center
            gap-2 pt-5
            text-sm font-bold
            text-[var(--primary)]
          "
        >
          {isYouTube
            ? "Watch Course"
            : "Open Resource"}

          <FaExternalLinkAlt
            className="
              transition
              group-hover:translate-x-1
            "
          />
        </span>
      </div>
    </a>
  );
}


export default LearningRecommendations;