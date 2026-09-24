import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaArrowLeft,
  FaBriefcase,
  FaDownload,
  FaFileAlt,
  FaGraduationCap,
  FaHistory,
  FaTrashAlt,
  FaUpload
} from "react-icons/fa";

import ThemeToggle from "../components/ThemeToggle/ThemeToggle";

import {
  deleteResume,
  downloadResumeReport,
  getResumeHistory
} from "../services/resumeService";

function ResumeHistory() {
  const navigate = useNavigate();

  const [resumes, setResumes] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [downloadingId, setDownloadingId] =
    useState(null);
  const [deletingId, setDeletingId] =
    useState(null);

  const [errorMessage, setErrorMessage] =
    useState("");
  const [successMessage, setSuccessMessage] =
    useState("");

  useEffect(() => {
    loadResumeHistory();
  }, []);

  const loadResumeHistory = async () => {
    setIsLoading(true);
    setErrorMessage("");

    try {
      const data = await getResumeHistory();
      setResumes(data);
    } catch (error) {
      console.error(
        "Resume history error:",
        error
      );

      if (error.response?.status === 401) {
        localStorage.removeItem("token");
        navigate("/login");
        return;
      }

      setErrorMessage(
        error.response?.data?.detail ||
        "Unable to load resume history."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = async (resumeId) => {
    setDownloadingId(resumeId);
    setErrorMessage("");

    try {
      const response =
        await downloadResumeReport(resumeId);

      const pdfBlob = new Blob(
        [response.data],
        {
          type: "application/pdf"
        }
      );

      const downloadUrl =
        window.URL.createObjectURL(pdfBlob);

      let fileName =
        "CareerCompass_Report.pdf";

      const contentDisposition =
        response.headers["content-disposition"];

      if (contentDisposition) {
        const fileNameMatch =
          contentDisposition.match(
            /filename="?([^"]+)"?/
          );

        if (fileNameMatch?.[1]) {
          fileName = fileNameMatch[1];
        }
      }

      const link =
        document.createElement("a");

      link.href = downloadUrl;
      link.download = fileName;

      document.body.appendChild(link);

      link.click();
      link.remove();

      window.URL.revokeObjectURL(
        downloadUrl
      );
    } catch (error) {
      console.error(
        "Report download error:",
        error
      );

      let errorDetail =
        "Unable to download the report.";

      if (
        error.response?.data instanceof Blob
      ) {
        try {
          const errorText =
            await error.response.data.text();

          const parsedError =
            JSON.parse(errorText);

          errorDetail =
            parsedError.detail ||
            errorDetail;
        } catch {
          errorDetail =
            "Unable to download the report.";
        }
      } else if (
        error.response?.data?.detail
      ) {
        errorDetail =
          error.response.data.detail;
      }

      setErrorMessage(errorDetail);
    } finally {
      setDownloadingId(null);
    }
  };

  const handleDelete = async (resumeId) => {
    const shouldDelete = window.confirm(
      "Are you sure you want to delete this resume?"
    );

    if (!shouldDelete) {
      return;
    }

    setDeletingId(resumeId);
    setErrorMessage("");
    setSuccessMessage("");

    try {
      await deleteResume(resumeId);

      setResumes((currentResumes) =>
        currentResumes.filter(
          (resume) => resume.id !== resumeId
        )
      );

      setSuccessMessage(
        "Resume deleted successfully."
      );
    } catch (error) {
      console.error(
        "Resume deletion error:",
        error
      );

      setErrorMessage(
        error.response?.data?.detail ||
        "Unable to delete the resume."
      );
    } finally {
      setDeletingId(null);
    }
  };

  const getScoreStyle = (score) => {
    if (score >= 80) {
      return "border-green-300 bg-green-50 text-green-800 dark:border-green-800 dark:bg-green-950/40 dark:text-green-300";
    }

    if (score >= 60) {
      return "border-amber-300 bg-amber-50 text-amber-800 dark:border-amber-800 dark:bg-amber-950/40 dark:text-amber-300";
    }

    return "border-red-300 bg-red-50 text-red-800 dark:border-red-800 dark:bg-red-950/40 dark:text-red-300";
  };

  return (
    <main className="app-page">
      <div className="page-container max-w-[1600px]">

        <header className="
          flex flex-col gap-4
          border-b border-[var(--border)]
          pb-6
          md:flex-row
          md:items-center
          md:justify-between
        ">
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => navigate("/dashboard")}
              className="btn-ghost"
            >
              <FaArrowLeft />
              Dashboard
            </button>

            <div className="
              hidden h-8 w-px
              bg-[var(--border)]
              md:block
            " />

            <div>
              <p className="
                text-sm font-semibold
                text-[var(--primary)]
              ">
                CareerCompass
              </p>

              <h1 className="
                mt-1 text-2xl font-bold
                tracking-tight
                text-[var(--text-primary)]
                md:text-3xl
              ">
                Resume History
              </h1>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <ThemeToggle />

            <button
              type="button"
              onClick={() => navigate("/resume")}
              className="btn-primary"
            >
              <FaUpload />
              Upload Resume
            </button>
          </div>
        </header>


        <section className="mt-8">
          <div className="
            flex flex-col gap-3
            lg:flex-row
            lg:items-end
            lg:justify-between
          ">
            <div>
              <span className="badge badge-primary">
                <FaHistory />
                Resume Library
              </span>

              <h2 className="page-title mt-4">
                Your analyzed resumes
              </h2>

              <p className="page-subtitle">
                Review your previous analyses, compare ATS
                scores, download reports and remove files
                you no longer need.
              </p>
            </div>

            {!isLoading && resumes.length > 0 && (
              <div className="
                rounded-2xl
                border border-[var(--border)]
                bg-[var(--surface)]
                px-5 py-4
                shadow-[var(--shadow-sm)]
              ">
                <p className="
                  text-sm
                  text-[var(--text-muted)]
                ">
                  Total analyzed resumes
                </p>

                <p className="
                  mt-1 text-2xl font-bold
                  text-[var(--text-primary)]
                ">
                  {resumes.length}
                </p>
              </div>
            )}
          </div>


          {errorMessage && (
            <div className="
              mt-6
              rounded-2xl
              border border-red-300
              bg-red-50
              p-4
              text-red-800

              dark:border-red-900/70
              dark:bg-red-950/30
              dark:text-red-300
            ">
              {errorMessage}
            </div>
          )}

          {successMessage && (
            <div className="
              mt-6
              rounded-2xl
              border border-green-300
              bg-green-50
              p-4
              text-green-800

              dark:border-green-900/70
              dark:bg-green-950/30
              dark:text-green-300
            ">
              {successMessage}
            </div>
          )}


          {isLoading ? (
            <div className="state-container mt-8">
              <div className="spinner" />

              <p className="state-title">
                Loading resume history
              </p>

              <p className="state-message">
                Please wait while we retrieve your previous
                analyses.
              </p>
            </div>
          ) : resumes.length === 0 ? (
            <div className="state-container mt-8">
              <div className="
                flex h-16 w-16 items-center
                justify-center rounded-2xl
                bg-[var(--primary-soft)]
                text-3xl
                text-[var(--primary)]
              ">
                <FaFileAlt />
              </div>

              <p className="state-title">
                No resumes found
              </p>

              <p className="state-message">
                Upload and analyze your first resume to
                start building your career history.
              </p>

              <button
                type="button"
                onClick={() => navigate("/resume")}
                className="btn-primary mt-2"
              >
                <FaUpload />
                Upload Resume
              </button>
            </div>
          ) : (
            <div className="mt-8 space-y-5">
              {resumes.map((resume) => {
                const readiness =
                  resume.career_readiness || 0;

                return (
                  <article
                    key={resume.id}
                    className="
                      app-card
                      app-card-hover
                      overflow-hidden
                    "
                  >
                    <div className="
                      grid gap-6
                      p-6
                      lg:grid-cols-[1.1fr_1fr_auto]
                      lg:items-center
                      xl:p-7
                    ">
                      <div className="
                        flex min-w-0
                        items-start gap-4
                      ">
                        <div className="
                          flex h-14 w-14
                          shrink-0 items-center
                          justify-center
                          rounded-2xl
                          bg-[var(--primary-soft)]
                          text-2xl
                          text-[var(--primary)]
                        ">
                          <FaFileAlt />
                        </div>

                        <div className="min-w-0">
                          <div className="
                            flex flex-wrap
                            items-center gap-3
                          ">
                            <h2 className="
                              truncate
                              text-xl font-bold
                              tracking-tight
                              text-[var(--text-primary)]
                            ">
                              {resume.file_name}
                            </h2>

                            <span
                              className={`
                                rounded-full
                                border px-3 py-1
                                text-sm font-bold
                                ${getScoreStyle(
                                  resume.ats_score || 0
                                )}
                              `}
                            >
                              ATS {resume.ats_score || 0}%
                            </span>
                          </div>

                          <p className="
                            mt-2 text-sm
                            text-[var(--text-muted)]
                          ">
                            Resume ID: {resume.id}
                          </p>

                          <div className="
                            mt-5 grid gap-4
                            sm:grid-cols-2
                          ">
                            <ResumeInfo
                              icon={<FaGraduationCap />}
                              label="Best Career"
                              value={
                                resume.best_career ||
                                "Not analyzed"
                              }
                            />

                            <ResumeInfo
                              icon={<FaBriefcase />}
                              label="Best Job"
                              value={
                                resume.best_job ||
                                "Not analyzed"
                              }
                            />
                          </div>
                        </div>
                      </div>


                      <div className="
                        rounded-2xl
                        border border-[var(--border)]
                        bg-[var(--surface-soft)]
                        p-5
                      ">
                        <div className="
                          flex items-center
                          justify-between gap-4
                        ">
                          <div>
                            <p className="
                              text-sm font-medium
                              text-[var(--text-secondary)]
                            ">
                              Career readiness
                            </p>

                            <p className="
                              mt-1 text-3xl font-bold
                              text-[var(--text-primary)]
                            ">
                              {readiness}%
                            </p>
                          </div>

                          <div className="
                            flex h-12 w-12
                            items-center justify-center
                            rounded-2xl
                            bg-[var(--primary-soft)]
                            text-xl
                            text-[var(--primary)]
                          ">
                            <FaGraduationCap />
                          </div>
                        </div>

                        <div className="progress-track mt-5">
                          <div
                            className="progress-value"
                            style={{
                              width: `${Math.min(
                                Math.max(readiness, 0),
                                100
                              )}%`
                            }}
                          />
                        </div>
                      </div>


                      <div className="
                        flex flex-col gap-3
                        sm:flex-row
                        lg:min-w-[210px]
                        lg:flex-col
                      ">
                        <button
                          type="button"
                          onClick={() =>
                            handleDownload(resume.id)
                          }
                          disabled={
                            downloadingId === resume.id
                          }
                          className="
                            btn-primary
                            w-full
                            disabled:cursor-not-allowed
                            disabled:opacity-50
                          "
                        >
                          <FaDownload />

                          {downloadingId === resume.id
                            ? "Downloading..."
                            : "Download Report"}
                        </button>

                        <button
                          type="button"
                          onClick={() =>
                            handleDelete(resume.id)
                          }
                          disabled={
                            deletingId === resume.id
                          }
                          className="
                            inline-flex min-h-11 w-full
                            items-center justify-center
                            gap-2 rounded-[14px]
                            border border-red-300
                            bg-red-50
                            px-[18px] py-[10px]
                            text-[0.95rem]
                            font-semibold
                            text-red-700
                            transition

                            hover:-translate-y-px
                            hover:border-red-500
                            hover:bg-red-100

                            disabled:cursor-not-allowed
                            disabled:opacity-50

                            dark:border-red-900/70
                            dark:bg-red-950/30
                            dark:text-red-300
                            dark:hover:bg-red-950/50
                          "
                        >
                          <FaTrashAlt />

                          {deletingId === resume.id
                            ? "Deleting..."
                            : "Delete"}
                        </button>
                      </div>
                    </div>
                  </article>
                );
              })}
            </div>
          )}
        </section>


        <footer className="
          mt-12
          border-t border-[var(--border)]
          py-6
          text-center
          text-sm
          text-[var(--text-muted)]
        ">
          CareerCompass · Resume history and reports
        </footer>
      </div>
    </main>
  );
}


function ResumeInfo({
  icon,
  label,
  value
}) {
  return (
    <div className="
      min-w-0 rounded-xl
      border border-[var(--border)]
      bg-[var(--surface-soft)]
      p-4
    ">
      <div className="
        flex items-center gap-2
        text-[var(--primary)]
      ">
        {icon}

        <span className="
          text-sm font-semibold
        ">
          {label}
        </span>
      </div>

      <p className="
        mt-2 truncate
        font-semibold
        text-[var(--text-primary)]
      ">
        {value}
      </p>
    </div>
  );
}

export default ResumeHistory;