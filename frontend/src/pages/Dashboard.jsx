import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaArrowRight,
  FaBookOpen,
  FaBriefcase,
  FaChartLine,
  FaCheckCircle,
  FaFileAlt,
  FaGraduationCap,
  FaHistory,
  FaSearch,
  FaSignOutAlt,
  FaMagic,
  FaUpload,
  FaUser
} from "react-icons/fa";

import ThemeToggle from "../components/ThemeToggle/ThemeToggle";
import { getDashboardStatistics } from "../services/resumeService";


function Dashboard() {
  const navigate = useNavigate();

  const [statistics, setStatistics] = useState(null);
  const [isStatsLoading, setIsStatsLoading] = useState(true);
  const [statsError, setStatsError] = useState("");


  useEffect(() => {
    const loadDashboardStatistics = async () => {
      setIsStatsLoading(true);
      setStatsError("");

      try {
        const data = await getDashboardStatistics();
        setStatistics(data);
      } catch (error) {
        console.error(
          "Dashboard statistics error:",
          error
        );

        if (error.response?.status === 401) {
          localStorage.removeItem("token");

          navigate("/login", {
            replace: true
          });

          return;
        }

        const detail =
          error.response?.data?.detail;

        if (typeof detail === "string") {
          setStatsError(detail);
        } else {
          setStatsError(
            "Unable to load dashboard statistics."
          );
        }
      } finally {
        setIsStatsLoading(false);
      }
    };

    loadDashboardStatistics();
  }, [navigate]);


  const handleLogout = () => {
    localStorage.removeItem("token");

    navigate("/login", {
      replace: true
    });
  };


  const totalResumes =
    statistics?.total_resumes ?? 0;

  const averageAtsScore =
    statistics?.average_ats_score ?? 0;

  const bestAtsScore =
    statistics?.best_ats_score ?? 0;

  const averageReadiness =
    statistics?.average_readiness ?? 0;


  return (
    <main className="app-page">
      <div className="page-container">

        {/* Top navigation */}
        <header className="
          flex flex-col gap-5
          border-b border-[var(--border)]
          pb-6
          md:flex-row
          md:items-center
          md:justify-between
        ">
          <div>
            <div className="flex items-center gap-3">
              <div className="
                flex h-11 w-11 items-center justify-center
                rounded-2xl
                bg-[var(--primary-soft)]
                text-xl
                text-[var(--primary)]
              ">
                <FaGraduationCap />
              </div>

              <div>
                <p className="
                  text-lg font-bold
                  tracking-tight
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
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <ThemeToggle />

            <button
              type="button"
              onClick={() => navigate("/profile")}
              className="btn-outline"
            >
              <FaUser />
              My Profile
            </button>

            <button
              type="button"
              onClick={handleLogout}
              className="
                inline-flex min-h-11 items-center
                justify-center gap-2
                rounded-[14px]
                border border-red-200
                bg-white
                px-[18px]
                py-[10px]
                text-[0.95rem]
                font-semibold
                text-red-600
                hover:-translate-y-px
                hover:border-red-400
                hover:bg-red-50

                dark:border-red-900/70
                dark:bg-red-950/20
                dark:text-red-400
                dark:hover:bg-red-950/40
              "
            >
              <FaSignOutAlt />
              Logout
            </button>
          </div>
        </header>


        {/* Welcome section */}
        <section className="
          mt-8
          overflow-hidden
          rounded-[28px]
          border border-[var(--border)]
          bg-[var(--surface)]
          shadow-[var(--shadow-sm)]
        ">
          <div className="
            grid gap-8
            p-6
            md:p-9
            lg:grid-cols-[1.3fr_0.7fr]
            lg:items-center
          ">
            <div>
              <span className="badge badge-primary">
                <FaCheckCircle />
                Career workspace
              </span>

              <h1 className="
                mt-5
                max-w-3xl
                text-3xl
                font-bold
                leading-tight
                tracking-[-0.04em]
                text-[var(--text-primary)]
                md:text-5xl
              ">
                Build a career plan that matches your
                skills and goals.
              </h1>

              <p className="
                mt-5
                max-w-2xl
                text-base
                leading-7
                text-[var(--text-secondary)]
                md:text-lg
              ">
                Upload your resume, understand your ATS
                score, discover suitable careers and
                create a practical learning path.
              </p>

              <div className="
                mt-7
                flex flex-col gap-3
                sm:flex-row
              ">
                <button
                  type="button"
                  onClick={() => navigate("/resume")}
                  className="btn-primary"
                >
                  <FaUpload />
                  Upload Resume
                  <FaArrowRight />
                </button>

                <button
                  type="button"
                  onClick={() =>
                    navigate("/resume-history")
                  }
                  className="btn-outline"
                >
                  <FaHistory />
                  Resume History
                </button>
              </div>
            </div>

            <div className="
              rounded-[24px]
              border border-[var(--border)]
              bg-[var(--surface-soft)]
              p-6
            ">
              <p className="
                text-sm font-semibold
                text-[var(--text-secondary)]
              ">
                Your career progress
              </p>

              <div className="
                mt-5
                flex items-end
                justify-between
                gap-4
              ">
                <div>
                  <p className="
                    text-4xl font-bold
                    tracking-tight
                    text-[var(--text-primary)]
                  ">
                    {averageReadiness}%
                  </p>

                  <p className="
                    mt-1 text-sm
                    text-[var(--text-muted)]
                  ">
                    Average readiness
                  </p>
                </div>

                <div className="
                  flex h-14 w-14 items-center
                  justify-center
                  rounded-2xl
                  bg-[var(--primary-soft)]
                  text-2xl
                  text-[var(--primary)]
                ">
                  <FaChartLine />
                </div>
              </div>

              <div className="progress-track mt-5">
                <div
                  className="progress-value"
                  style={{
                    width: `${Math.min(
                      Math.max(averageReadiness, 0),
                      100
                    )}%`
                  }}
                />
              </div>

              <p className="
                mt-4 text-sm leading-6
                text-[var(--text-secondary)]
              ">
                Continue improving your skills and resume
                quality to increase your readiness score.
              </p>
            </div>
          </div>
        </section>


        {/* Error message */}
        {statsError && (
          <div className="
            mt-6
            rounded-2xl
            border border-red-200
            bg-red-50
            p-4
            text-sm
            text-red-700

            dark:border-red-900/60
            dark:bg-red-950/30
            dark:text-red-300
          ">
            {statsError}
          </div>
        )}


        {/* Statistics */}
        <section className="mt-9">
          <div className="
            flex flex-col gap-2
            sm:flex-row
            sm:items-end
            sm:justify-between
          ">
            <div>
              <h2 className="section-title">
                Career overview
              </h2>

              <p className="section-description">
                A quick summary of your resume and career
                analysis progress.
              </p>
            </div>
          </div>

          {isStatsLoading ? (
            <div className="state-container mt-5">
              <div className="spinner" />

              <p className="state-title">
                Loading your dashboard
              </p>

              <p className="state-message">
                We are preparing your latest resume and
                career statistics.
              </p>
            </div>
          ) : (
            <div className="
              mt-5
              grid gap-5
              sm:grid-cols-2
              xl:grid-cols-4
            ">
              <StatisticCard
                title="Total Resumes"
                value={totalResumes}
                description="Resumes analyzed"
                icon={<FaFileAlt />}
              />

              <StatisticCard
                title="Average ATS Score"
                value={`${averageAtsScore}%`}
                description="Overall resume quality"
                icon={<FaChartLine />}
              />

              <StatisticCard
                title="Best ATS Score"
                value={`${bestAtsScore}%`}
                description="Your highest score"
                icon={<FaCheckCircle />}
              />

              <StatisticCard
                title="Average Readiness"
                value={`${averageReadiness}%`}
                description="Career preparation level"
                icon={<FaGraduationCap />}
              />
            </div>
          )}
        </section>


        {/* Recommended career and latest resume */}
        {!isStatsLoading && statistics && (
          <section className="
            mt-6
            grid gap-6
            lg:grid-cols-[0.8fr_1.2fr]
          ">
            <div className="
              app-card
              app-card-padding
              relative
              overflow-hidden
            ">
              <div className="
                absolute -right-10 -top-10
                h-36 w-36
                rounded-full
                bg-[var(--primary-soft)]
              " />

              <div className="relative">
                <div className="
                  flex h-12 w-12 items-center
                  justify-center
                  rounded-2xl
                  bg-[var(--primary-soft)]
                  text-xl
                  text-[var(--primary)]
                ">
                  <FaBriefcase />
                </div>

                <p className="
                  mt-5 text-sm font-semibold
                  text-[var(--text-secondary)]
                ">
                  Most recommended career
                </p>

                <h2 className="
                  mt-2
                  text-2xl font-bold
                  tracking-tight
                  text-[var(--text-primary)]
                ">
                  {statistics.most_recommended_career ||
                    "Complete an analysis"}
                </h2>

                <p className="
                  mt-3 leading-6
                  text-[var(--text-secondary)]
                ">
                  This role is based on the skills and
                  information found in your analyzed
                  resumes.
                </p>

                <button
                  type="button"
                  onClick={() => navigate("/career")}
                  className="btn-ghost mt-5"
                >
                  View career details
                  <FaArrowRight />
                </button>
              </div>
            </div>

            <div className="app-card app-card-padding">
              <div className="
                flex flex-col gap-3
                sm:flex-row
                sm:items-center
                sm:justify-between
              ">
                <div>
                  <p className="
                    text-sm font-semibold
                    text-[var(--primary)]
                  ">
                    Latest resume
                  </p>

                  <h2 className="
                    mt-1 text-xl font-bold
                    text-[var(--text-primary)]
                  ">
                    Latest resume analysis
                  </h2>
                </div>

                <button
                  type="button"
                  onClick={() =>
                    navigate("/resume-history")
                  }
                  className="btn-ghost"
                >
                  View history
                  <FaArrowRight />
                </button>
              </div>

              {statistics.latest_resume ? (
                <div className="
                  mt-5
                  grid gap-4
                  rounded-2xl
                  border border-[var(--border)]
                  bg-[var(--surface-soft)]
                  p-5
                  sm:grid-cols-2
                ">
                  <ResumeDetail
                    label="File name"
                    value={
                      statistics.latest_resume.file_name ||
                      "Not available"
                    }
                  />

                  <ResumeDetail
                    label="ATS score"
                    value={`${
                      statistics.latest_resume.ats_score ??
                      0
                    }%`}
                  />

                  <ResumeDetail
                    label="Best career"
                    value={
                      statistics.latest_resume.best_career ||
                      "Not available"
                    }
                  />

                  <ResumeDetail
                    label="Best job"
                    value={
                      statistics.latest_resume.best_job ||
                      "Not available"
                    }
                  />
                </div>
              ) : (
                <div className="
                  mt-5
                  rounded-2xl
                  border border-dashed
                  border-[var(--border-strong)]
                  bg-[var(--surface-soft)]
                  p-6
                  text-center
                ">
                  <p className="
                    font-semibold
                    text-[var(--text-primary)]
                  ">
                    No resume analysis yet
                  </p>

                  <p className="
                    mt-2 text-sm
                    text-[var(--text-secondary)]
                  ">
                    Upload your first resume to view its
                    ATS score and career recommendations.
                  </p>

                  <button
                    type="button"
                    onClick={() => navigate("/resume")}
                    className="btn-primary mt-5"
                  >
                    <FaUpload />
                    Upload Resume
                  </button>
                </div>
              )}
            </div>
          </section>
        )}


        {/* Feature cards */}
        <section className="mt-10">
          <div>
            <h2 className="section-title">
              Continue your career journey
            </h2>

            <p className="section-description">
              Choose a tool to review your progress and
              take the next step.
            </p>
          </div>

          <div className="
            mt-5
            grid gap-5
            sm:grid-cols-2
            lg:grid-cols-3
          ">
            <DashboardCard
              icon={<FaFileAlt />}
              title="Resume Analysis"
              description="Upload a resume and review its ATS compatibility, skills and important details."
              actionText="Analyze resume"
              onClick={() => navigate("/resume")}
            />

            <DashboardCard
              icon={<FaHistory />}
              title="Resume History"
              description="Review, download or remove resumes that you previously analyzed."
              actionText="View history"
              onClick={() =>
                navigate("/resume-history")
              }
            />

            <DashboardCard
              icon={<FaChartLine />}
              title="Career Prediction"
              description="Discover career paths that match your current skills, strengths and experience."
              actionText="Explore careers"
              onClick={() => navigate("/career")}
            />

            <DashboardCard
              icon={<FaGraduationCap />}
              title="Skill Gap"
              description="Understand which important skills are missing for your selected career path."
              actionText="Check skill gaps"
              onClick={() => navigate("/skill-gap")}
            />

            <DashboardCard
              icon={<FaBriefcase />}
              title="Recommended Jobs"
              description="Explore suitable job roles based on your resume, skills and predicted career."
              actionText="View jobs"
              onClick={() => navigate("/jobs")}
            />

            <DashboardCard
              icon={<FaBookOpen />}
              title="Learning Recommendations"
              description="Find courses, learning resources and practical steps for developing missing skills."
              actionText="Start learning"
              onClick={() => navigate("/learning")}
            />
            <DashboardCard
             icon={<FaSearch />}
             title="Resume vs Job Description"
             description="Compare your latest analyzed resume with a job description. Check job match percentage, missing skills, important keywords and receive AI-powered improvement suggestions."
             actionText="Analyze Job Match"
             onClick={() => navigate("/job-description-analyzer")}
            />
            <DashboardCard
              icon={<FaMagic />}
              title="Resume Improvement"
              description="Receive AI-generated suggestions to improve your resume for ATS systems, recruiters and your target career."
              actionText="View Suggestions"
              onClick={() =>navigate("/resume-improvement")}
            />
          </div>
        </section>


        {/* Footer */}
        <footer className="
          mt-12
          border-t border-[var(--border)]
          py-6
          text-center
          text-sm
          text-[var(--text-muted)]
        ">
          CareerCompass · Your personal career development
          workspace
        </footer>
      </div>
    </main>
  );
}


function StatisticCard({
  title,
  value,
  description,
  icon
}) {
  return (
    <article className="
      app-card
      app-card-hover
      app-card-padding
    ">
      <div className="
        flex items-start
        justify-between
        gap-4
      ">
        <div>
          <p className="
            text-sm font-medium
            text-[var(--text-secondary)]
          ">
            {title}
          </p>

          <p className="
            mt-3
            text-3xl font-bold
            tracking-tight
            text-[var(--text-primary)]
          ">
            {value}
          </p>

          <p className="
            mt-2 text-sm
            text-[var(--text-muted)]
          ">
            {description}
          </p>
        </div>

        <div className="
          flex h-12 w-12 shrink-0
          items-center justify-center
          rounded-2xl
          bg-[var(--primary-soft)]
          text-xl
          text-[var(--primary)]
        ">
          {icon}
        </div>
      </div>
    </article>
  );
}


function ResumeDetail({
  label,
  value
}) {
  return (
    <div className="min-w-0">
      <p className="
        text-xs font-semibold
        uppercase tracking-[0.08em]
        text-[var(--text-muted)]
      ">
        {label}
      </p>

      <p className="
        mt-2
        truncate
        font-semibold
        text-[var(--text-primary)]
      ">
        {value}
      </p>
    </div>
  );
}


function DashboardCard({
  icon,
  title,
  description,
  actionText,
  onClick
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="
        app-card
        app-card-hover
        group
        flex h-full min-w-0
        flex-col
        p-6
        text-left
      "
    >
      <div className="
        flex h-14 w-14 shrink-0
        items-center justify-center
        rounded-2xl
        bg-[var(--primary-soft)]
        text-2xl
        text-[var(--primary)]

        transition-transform
        duration-300
        group-hover:scale-105
      ">
        {icon}
      </div>

      <h3 className="
        mt-5
        text-xl font-bold
        tracking-tight
        text-[var(--text-primary)]
      ">
        {title}
      </h3>

      <p className="
        mt-3
        flex-1
        leading-7
        text-[var(--text-secondary)]
      ">
        {description}
      </p>

      <span className="
        mt-6
        inline-flex items-center
        gap-2
        text-sm font-semibold
        text-[var(--primary)]
      ">
        {actionText}

        <FaArrowRight className="
          transition-transform
          duration-200
          group-hover:translate-x-1
        " />
      </span>
    </button>
  );
}


export default Dashboard;