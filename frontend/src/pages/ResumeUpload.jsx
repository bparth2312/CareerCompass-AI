import { useNavigate } from "react-router-dom";
import {
  FaArrowLeft,
  FaFileAlt,
  FaLightbulb,
  FaShieldAlt
} from "react-icons/fa";

import ResumeUploader from "../components/ResumeUploader";
import ThemeToggle from "../components/ThemeToggle/ThemeToggle";

function ResumeUpload() {
  const navigate = useNavigate();

  return (
    <main className="app-page">
      <div className="mx-auto w-full max-w-[1600px] px-4 py-6 sm:px-6 lg:px-8">
        <header className="flex flex-col gap-4 border-b border-[var(--border)] pb-6 sm:flex-row sm:items-center sm:justify-between">
          <button
            type="button"
            onClick={() => navigate("/dashboard")}
            className="btn-ghost w-fit"
          >
            <FaArrowLeft />
            Back to Dashboard
          </button>

          <ThemeToggle />
        </header>

        <section className="mt-8">
          <div className="page-header text-center">
            <span className="badge badge-primary">
              <FaFileAlt />
              Resume Analysis
            </span>

            <h1 className="page-title mt-5">Upload your resume</h1>

            <p className="page-subtitle mx-auto">
              Upload your resume to check its ATS score, identify important
              skills and receive career recommendations based on your profile.
            </p>
          </div>

          <div className="mt-7 grid gap-4 md:grid-cols-3">
            <InfoCard
              icon={<FaShieldAlt />}
              title="Your file is protected"
              description="Your resume is used only for analysis and personalized career recommendations."
            />

            <InfoCard
              icon={<FaLightbulb />}
              title="Use your latest resume"
              description="Include recent skills, projects, education and work experience for accurate results."
            />

            <div className="rounded-2xl border border-[var(--border)] bg-[var(--primary-soft)] p-5">
              <p className="font-semibold text-[var(--primary)]">
                Analysis process
              </p>
              <p className="mt-2 text-sm leading-6 text-[var(--text-secondary)]">
                Upload → ATS analysis → career prediction → skill gap → learning
                roadmap → job recommendations.
              </p>
            </div>
          </div>

          <section className="app-card mt-6 w-full overflow-hidden p-4 sm:p-6 lg:p-8">
            <ResumeUploader />
          </section>
        </section>

        <footer className="mt-12 border-t border-[var(--border)] py-6 text-center text-sm text-[var(--text-muted)]">
          CareerCompass · Resume analysis and career guidance
        </footer>
      </div>
    </main>
  );
}

function InfoCard({ icon, title, description }) {
  return (
    <article className="rounded-2xl border border-[var(--border)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]">
      <div className="flex items-start gap-4">
        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-[var(--primary-soft)] text-lg text-[var(--primary)]">
          {icon}
        </div>

        <div>
          <h2 className="font-bold text-[var(--text-primary)]">{title}</h2>
          <p className="mt-1 text-sm leading-6 text-[var(--text-secondary)]">
            {description}
          </p>
        </div>
      </div>
    </article>
  );
}

export default ResumeUpload;