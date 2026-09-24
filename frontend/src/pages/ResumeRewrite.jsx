import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import {
  FaArrowLeft,
  FaBriefcase,
  FaCheckCircle,
  FaCopy,
  FaExclamationTriangle,
  FaFileAlt,
  FaMagic,
  FaRedo,
  FaDownload,
  FaSpinner
} from "react-icons/fa";

import ThemeToggle from
  "../components/ThemeToggle/ThemeToggle";

import {
    downloadRewrittenResumeDocx,
    downloadRewrittenResumePdf,
  rewriteResumeByCareer
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


function ResumeRewrite() {
  const navigate = useNavigate();
  const location = useLocation();
   
  const initialCareer =
    location.state?.targetCareer ||
    "";

  const [targetCareer, setTargetCareer] =
    useState(initialCareer);

  const [data, setData] =
    useState(null);

  const [isLoading, setIsLoading] =
    useState(false);
  
  const [
  isDownloadingDocx,
  setIsDownloadingDocx
 ] = useState(false);
 
   const [
  isDownloadingPdf,
  setIsDownloadingPdf
  ] = useState(false);
  const [
    errorMessage,
    setErrorMessage
  ] = useState("");

  const [
    copiedSection,
    setCopiedSection
  ] = useState("");


  useEffect(() => {
    if (initialCareer) {
      handleRewrite(initialCareer);
    }
  }, []);


  const handleRewrite = async (
    careerName = targetCareer
  ) => {
    const cleanCareer =
      String(careerName || "").trim();

    if (!cleanCareer) {
      setErrorMessage(
        "Please enter or select a target career."
      );

      return;
    }

    setIsLoading(true);
    setErrorMessage("");
    setData(null);

    try {
      const response =
        await rewriteResumeByCareer(
          cleanCareer
        );

      setData(response);
      setTargetCareer(
        response.target_career ||
        cleanCareer
      );
    } catch (error) {
      console.error(
        "Resume rewrite error:",
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
          "Unable to rewrite the resume."
        )
      );
    } finally {
      setIsLoading(false);
    }
  };
    const handleDownloadDocx = async () => {
  const cleanCareer =
    String(
      data?.target_career ||
      targetCareer ||
      ""
    ).trim();

  if (!cleanCareer) {
    setErrorMessage(
      "Please select a target career before downloading."
    );

    return;
  }

  setIsDownloadingDocx(true);
  setErrorMessage("");

  try {
    const response =
      await downloadRewrittenResumeDocx(
        cleanCareer
      );

    const contentDisposition =
      response.headers[
        "content-disposition"
      ];

    let fileName =
      "Improved_Resume.docx";

    if (contentDisposition) {
      const fileNameMatch =
        contentDisposition.match(
          /filename="?([^"]+)"?/i
        );

      if (fileNameMatch?.[1]) {
        fileName =
          fileNameMatch[1];
      }
    }

    const blobUrl =
      window.URL.createObjectURL(
        new Blob(
          [response.data],
          {
            type:
              "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          }
        )
      );

    const link =
      document.createElement("a");

    link.href = blobUrl;
    link.download = fileName;

    document.body.appendChild(
      link
    );

    link.click();

    document.body.removeChild(
      link
    );

    window.URL.revokeObjectURL(
      blobUrl
    );
  } catch (error) {
    console.error(
      "DOCX download error:",
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
        "Unable to download the improved resume."
      )
    );
  } finally {
    setIsDownloadingDocx(false);
  }
};
   
   const handleDownloadPdf = async () => {
  const cleanCareer = String(
    data?.target_career ||
    targetCareer ||
    ""
  ).trim();

  if (!cleanCareer) {
    setErrorMessage(
      "Please select a target career before downloading."
    );

    return;
  }

  setIsDownloadingPdf(true);
  setErrorMessage("");

  try {
    const response =
      await downloadRewrittenResumePdf(
        cleanCareer
      );

    const contentDisposition =
      response.headers[
        "content-disposition"
      ];

    let fileName =
      "Improved_Resume.pdf";

    if (contentDisposition) {
      const fileNameMatch =
        contentDisposition.match(
          /filename="?([^"]+)"?/i
        );

      if (fileNameMatch?.[1]) {
        fileName =
          fileNameMatch[1];
      }
    }

    const blobUrl =
      window.URL.createObjectURL(
        new Blob(
          [response.data],
          {
            type: "application/pdf"
          }
        )
      );

    const link =
      document.createElement("a");

    link.href = blobUrl;
    link.download = fileName;

    document.body.appendChild(
      link
    );

    link.click();

    document.body.removeChild(
      link
    );

    window.URL.revokeObjectURL(
      blobUrl
    );
  } catch (error) {
    console.error(
      "PDF download error:",
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
        "Unable to download the improved resume PDF."
      )
    );
  } finally {
    setIsDownloadingPdf(false);
  }
};
  const copyText = async (
    value,
    sectionName
  ) => {
    try {
      await navigator.clipboard.writeText(
        value
      );

      setCopiedSection(
        sectionName
      );

      window.setTimeout(() => {
        setCopiedSection("");
      }, 1800);
    } catch (error) {
      console.error(
        "Copy failed:",
        error
      );
    }
  };


  return (
    <main className="app-page">
      <div
        className="
          page-container
          max-w-[1500px]
        "
      >
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
              AI Resume Rewrite
            </h1>

            <p
              className="
                mt-3 max-w-3xl
                leading-7
                text-[var(--text-secondary)]
              "
            >
              Rewrite your professional summary,
              experience bullets and project
              descriptions for a selected career.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <ThemeToggle />

            <button
              type="button"
              onClick={() =>
                navigate(
                  "/resume-improvement"
                )
              }
              className="btn-outline"
            >
              <FaArrowLeft />
              Back
            </button>
          </div>
        </header>


        <section
          className="
            mt-8 rounded-3xl
            border border-[var(--border)]
            bg-[var(--surface)]
            p-7
            shadow-[var(--shadow-sm)]
          "
        >
          <div
            className="
              flex items-start gap-4
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
              <FaBriefcase />
            </div>

            <div>
              <h2
                className="
                  text-2xl font-bold
                  text-[var(--text-primary)]
                "
              >
                Select Target Career
              </h2>

              <p
                className="
                  mt-1 text-sm
                  text-[var(--text-secondary)]
                "
              >
                Enter the career for which you
                want to rewrite your latest resume.
              </p>
            </div>
          </div>

          <div
            className="
              mt-6 flex flex-col gap-3

              sm:flex-row
            "
          >
            <input
              type="text"
              value={targetCareer}
              onChange={(event) =>
                setTargetCareer(
                  event.target.value
                )
              }
              placeholder="Example: Full Stack Developer"
              className="form-input flex-1"
              maxLength={150}
            />

            <button
              type="button"
              onClick={() =>
                handleRewrite()
              }
              disabled={isLoading}
              className="
                btn-primary
                justify-center
                disabled:cursor-not-allowed
                disabled:opacity-60
              "
            >
              {isLoading ? (
                <>
                  <FaSpinner className="animate-spin" />
                  Rewriting...
                </>
              ) : data ? (
                <>
                  <FaRedo />
                  Rewrite Again
                </>
              ) : (
                <>
                  <FaMagic />
                  Rewrite Resume
                </>
              )}
            </button>
          </div>
        </section>


        {errorMessage && (
          <section
            className="
              mt-6 rounded-2xl
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


        {isLoading && (
          <section
            className="
              mt-8 flex min-h-[300px]
              items-center justify-center
              rounded-3xl
              border border-[var(--border)]
              bg-[var(--surface)]
            "
          >
            <div className="text-center">
              <FaSpinner
                className="
                  mx-auto animate-spin
                  text-4xl
                  text-[var(--primary)]
                "
              />

              <h2
                className="
                  mt-5 text-xl font-bold
                  text-[var(--text-primary)]
                "
              >
                Rewriting Your Resume
              </h2>

              <p
                className="
                  mt-2
                  text-[var(--text-secondary)]
                "
              >
                Improving content for{" "}
                {targetCareer}.
              </p>
            </div>
          </section>
        )}


        {!isLoading && data && (
          <>
            <section
              className="
                mt-8 rounded-3xl
                border border-[var(--primary)]
                bg-[var(--primary-soft)]
                p-6
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
                    Resume Rewrite Complete
                  </p>

                  <h2
                    className="
                      mt-1 text-2xl font-bold
                      text-[var(--text-primary)]
                    "
                  >
                    {data.target_career}
                  </h2>

                  <p
                    className="
                      mt-2 text-sm
                      text-[var(--text-secondary)]
                    "
                  >
                    Resume: {data.file_name}
                  </p>
                </div>

                <div
                  className="
                 flex flex-wrap
                  items-center
                   gap-3
                 "
            >
  {/* DOCX Button */}
  <button
    type="button"
    onClick={handleDownloadDocx}
    disabled={
      isDownloadingDocx ||
      isDownloadingPdf ||
      isLoading
    }
    className="
      inline-flex
      items-center
      gap-2
      rounded-xl
      bg-emerald-600
      px-5
      py-3
      text-sm
      font-semibold
      text-white
      hover:bg-emerald-700
      disabled:opacity-60
    "
  >
    {isDownloadingDocx ? (
      <>
        <FaSpinner className="animate-spin" />
        Preparing DOCX...
      </>
    ) : (
      <>
        <FaDownload />
        Download DOCX
      </>
    )}
  </button>

  {/* PDF Button */}
  <button
    type="button"
    onClick={handleDownloadPdf}
    disabled={
      isDownloadingPdf ||
      isDownloadingDocx ||
      isLoading
    }
    className="
      inline-flex
      items-center
      gap-2
      rounded-xl
      bg-red-600
      px-5
      py-3
      text-sm
      font-semibold
      text-white
      hover:bg-red-700
      disabled:opacity-60
    "
  >
    {isDownloadingPdf ? (
      <>
        <FaSpinner className="animate-spin" />
        Preparing PDF...
      </>
    ) : (
      <>
        <FaDownload />
        Download PDF
      </>
    )}
  </button>

  <FaCheckCircle
    className="
      text-3xl
      text-emerald-500
    "
  />
</div>
              </div>
            </section>
            {data.quality_analysis && (
  <ResumeQualityDashboard
    analysis={data.quality_analysis}
  />
   )}

            <section className="mt-8">
              <h2 className="section-title">
                Professional Summary
              </h2>

              <div
                className="
                  mt-5 grid gap-6

                  lg:grid-cols-2
                "
              >
                <TextComparisonCard
                  title="Current Summary"
                  value={
                    data.original_content
                      ?.summary ||
                    "No summary was detected."
                  }
                  type="original"
                  onCopy={() =>
                    copyText(
                      data.original_content
                        ?.summary ||
                        "",
                      "original-summary"
                    )
                  }
                  copied={
                    copiedSection ===
                    "original-summary"
                  }
                />

                <TextComparisonCard
                  title="Improved Summary"
                  value={
                    data.rewritten_content
                      ?.summary ||
                    "No rewritten summary was generated."
                  }
                  type="improved"
                  onCopy={() =>
                    copyText(
                      data.rewritten_content
                        ?.summary ||
                        "",
                      "improved-summary"
                    )
                  }
                  copied={
                    copiedSection ===
                    "improved-summary"
                  }
                />
              </div>
            </section>


            <RewriteListSection
              title="Experience Rewrite"
              originalItems={
                data.original_content
                  ?.experience || []
              }
              rewrittenItems={
                data.rewritten_content
                  ?.experience || []
              }
              copiedSection={
                copiedSection
              }
              copyText={copyText}
              sectionKey="experience"
            />


            <RewriteListSection
              title="Project Rewrite"
              originalItems={
                data.original_content
                  ?.projects || []
              }
              rewrittenItems={
                data.rewritten_content
                  ?.projects || []
              }
              copiedSection={
                copiedSection
              }
              copyText={copyText}
              sectionKey="projects"
            />


            <section className="mt-8">
              <h2 className="section-title">
                Skills Review
              </h2>

              <div
                className="
                  mt-5 grid gap-6

                  lg:grid-cols-2
                "
              >
                <SkillCard
                  title="Verified Skills"
                  skills={
                    data.rewritten_content
                      ?.verified_skills || []
                  }
                  type="verified"
                />

                <SkillCard
                  title="Recommended Skills"
                  skills={
                    data.rewritten_content
                      ?.recommended_skills || []
                  }
                  type="recommended"
                />
              </div>
            </section>


            <section
              className="
                mt-8 rounded-3xl
                border border-[var(--border)]
                bg-[var(--surface)]
                p-6
                shadow-[var(--shadow-sm)]
              "
            >
              <h2
                className="
                  flex items-center gap-2
                  text-xl font-bold
                  text-[var(--text-primary)]
                "
              >
                <FaFileAlt
                  className="
                    text-[var(--primary)]
                  "
                />
                Rewrite Notes
              </h2>

              <div className="mt-5 space-y-3">
                {(data.rewrite_notes || [])
                  .map((note, index) => (
                    <div
                      key={`${note}-${index}`}
                      className="
                        flex items-start gap-3
                        rounded-2xl
                        bg-[var(--surface-soft)]
                        p-4
                      "
                    >
                      <FaCheckCircle
                        className="
                          mt-1 shrink-0
                          text-emerald-500
                        "
                      />

                      <p
                        className="
                          text-sm leading-6
                          text-[var(--text-secondary)]
                        "
                      >
                        {note}
                      </p>
                    </div>
                  ))}
              </div>
            </section>


            <section
              className="
                mb-10 mt-6 rounded-2xl
                border border-amber-300
                bg-amber-50 p-5
                text-amber-900

                dark:border-amber-900/70
                dark:bg-amber-950/30
                dark:text-amber-300
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

                <p className="leading-7">
                  {data.disclaimer}
                </p>
              </div>
            </section>
          </>
        )}
      </div>
    </main>
  );
}


function TextComparisonCard({
  title,
  value,
  type,
  onCopy,
  copied
}) {
  const improved =
    type === "improved";

  return (
    <article
      className={`
        rounded-3xl border
        p-6 shadow-[var(--shadow-sm)]

        ${
          improved
            ? `
              border-emerald-300
              bg-emerald-50

              dark:border-emerald-900/70
              dark:bg-emerald-950/20
            `
            : `
              border-[var(--border)]
              bg-[var(--surface)]
            `
        }
      `}
    >
      <div
        className="
          flex items-center
          justify-between gap-4
        "
      >
        <h3
          className="
            font-bold
            text-[var(--text-primary)]
          "
        >
          {title}
        </h3>

        <button
          type="button"
          onClick={onCopy}
          className="
            flex items-center gap-2
            rounded-xl
            border border-[var(--border)]
            bg-[var(--surface-soft)]
            px-3 py-2
            text-xs font-semibold
            text-[var(--text-secondary)]
          "
        >
          {copied ? (
            <FaCheckCircle />
          ) : (
            <FaCopy />
          )}

          {copied
            ? "Copied"
            : "Copy"}
        </button>
      </div>

      <p
        className="
          mt-5 whitespace-pre-line
          text-sm leading-7
          text-[var(--text-secondary)]
        "
      >
        {value}
      </p>
    </article>
  );
}


function RewriteListSection({
  title,
  originalItems,
  rewrittenItems,
  copiedSection,
  copyText,
  sectionKey
}) {
  return (
    <section className="mt-8">
      <h2 className="section-title">
        {title}
      </h2>

      <div
        className="
          mt-5 grid gap-6

          lg:grid-cols-2
        "
      >
        <ListRewriteCard
          title="Current Content"
          items={originalItems}
          type="original"
          copied={
            copiedSection ===
            `${sectionKey}-original`
          }
          onCopy={() =>
            copyText(
              originalItems.join("\n"),
              `${sectionKey}-original`
            )
          }
        />

        <ListRewriteCard
          title="Improved Content"
          items={rewrittenItems}
          type="improved"
          copied={
            copiedSection ===
            `${sectionKey}-improved`
          }
          onCopy={() =>
            copyText(
              rewrittenItems.join("\n"),
              `${sectionKey}-improved`
            )
          }
        />
      </div>
    </section>
  );
}


function ListRewriteCard({
  title,
  items,
  type,
  copied,
  onCopy
}) {
  const safeItems =
    Array.isArray(items)
      ? items
      : [];

  const improved =
    type === "improved";

  return (
    <article
      className={`
        rounded-3xl border
        p-6 shadow-[var(--shadow-sm)]

        ${
          improved
            ? `
              border-emerald-300
              bg-emerald-50

              dark:border-emerald-900/70
              dark:bg-emerald-950/20
            `
            : `
              border-[var(--border)]
              bg-[var(--surface)]
            `
        }
      `}
    >
      <div
        className="
          flex items-center
          justify-between gap-4
        "
      >
        <h3
          className="
            font-bold
            text-[var(--text-primary)]
          "
        >
          {title}
        </h3>

        <button
          type="button"
          onClick={onCopy}
          disabled={
            safeItems.length === 0
          }
          className="
            flex items-center gap-2
            rounded-xl
            border border-[var(--border)]
            bg-[var(--surface-soft)]
            px-3 py-2
            text-xs font-semibold
            text-[var(--text-secondary)]
            disabled:cursor-not-allowed
            disabled:opacity-50
          "
        >
          {copied ? (
            <FaCheckCircle />
          ) : (
            <FaCopy />
          )}

          {copied
            ? "Copied"
            : "Copy"}
        </button>
      </div>

      {safeItems.length > 0 ? (
        <div className="mt-5 space-y-3">
          {safeItems.map(
            (item, index) => (
              <div
                key={`${item}-${index}`}
                className="
                  rounded-2xl
                  bg-[var(--surface-soft)]
                  p-4
                "
              >
                <p
                  className="
                    text-sm leading-7
                    text-[var(--text-secondary)]
                  "
                >
                  {item}
                </p>
              </div>
            )
          )}
        </div>
      ) : (
        <p
          className="
            mt-5 text-sm
            text-[var(--text-muted)]
          "
        >
          No content was detected in this section.
        </p>
      )}
    </article>
  );
}


function SkillCard({
  title,
  skills,
  type
}) {
  const safeSkills =
    Array.isArray(skills)
      ? skills
      : [];

  const verified =
    type === "verified";

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
      <h3
        className="
          text-xl font-bold
          text-[var(--text-primary)]
        "
      >
        {title}
      </h3>

      {safeSkills.length > 0 ? (
        <div
          className="
            mt-5 flex flex-wrap
            gap-3
          "
        >
          {safeSkills.map(
            (skill, index) => (
              <span
                key={`${skill}-${index}`}
                className={`
                  rounded-full border
                  px-4 py-2
                  text-sm font-semibold

                  ${
                    verified
                      ? `
                        border-emerald-300
                        bg-emerald-50
                        text-emerald-700

                        dark:border-emerald-900/70
                        dark:bg-emerald-950/30
                        dark:text-emerald-300
                      `
                      : `
                        border-amber-300
                        bg-amber-50
                        text-amber-700

                        dark:border-amber-900/70
                        dark:bg-amber-950/30
                        dark:text-amber-300
                      `
                  }
                `}
              >
                {skill}
              </span>
            )
          )}
        </div>
      ) : (
        <p
          className="
            mt-5 text-sm
            text-[var(--text-muted)]
          "
        >
          No skills available.
        </p>
      )}

      {!verified && (
        <p
          className="
            mt-5 text-sm leading-6
            text-[var(--text-secondary)]
          "
        >
          Add these skills only after gaining
          practical knowledge or project experience.
        </p>
      )}
    </article>
  );
}


function ResumeQualityDashboard({
  analysis
}) {
  const safeScore = (value) =>
    Math.min(
      Math.max(
        Number(value) || 0,
        0
      ),
      100
    );

  const readability = safeScore(
    analysis?.readability
  );

  const professionalLanguage =
    safeScore(
      analysis?.professional_language
    );

  const atsOptimization = safeScore(
    analysis?.ats_optimization
  );

  const actionVerbs = safeScore(
    analysis?.action_verbs
  );

  const overallImprovement =
    Math.max(
      Number(
        analysis?.overall_improvement
      ) || 0,
      0
    );

  const originalWordCount =
    Math.max(
      Number(
        analysis?.original_word_count
      ) || 0,
      0
    );

  const rewrittenWordCount =
    Math.max(
      Number(
        analysis?.rewritten_word_count
      ) || 0,
      0
    );

  return (
    <section className="mt-8">
      <div>
        <h2 className="section-title">
          Resume Quality Analysis
        </h2>

        <p className="section-description">
          Review the estimated improvement in
          readability, professional writing and ATS
          compatibility.
        </p>
      </div>

      <div
        className="
          mt-5 grid gap-5
          sm:grid-cols-2
          xl:grid-cols-4
        "
      >
        <QualityMetricCard
          title="Readability"
          score={readability}
          description="Clarity and ease of reading"
        />

        <QualityMetricCard
          title="Professional Language"
          score={professionalLanguage}
          description="Strength of resume wording"
        />

        <QualityMetricCard
          title="ATS Optimization"
          score={atsOptimization}
          description="Keyword and format alignment"
        />

        <QualityMetricCard
          title="Action Verbs"
          score={actionVerbs}
          description="Strength of bullet openings"
        />
      </div>

      <div
        className="
          mt-5 grid gap-5
          lg:grid-cols-[0.75fr_1.25fr]
        "
      >
        <article
          className="
            rounded-3xl
            border border-emerald-300
            bg-emerald-50
            p-6
            shadow-[var(--shadow-sm)]

            dark:border-emerald-900/70
            dark:bg-emerald-950/20
          "
        >
          <p
            className="
              text-sm font-semibold
              text-emerald-700

              dark:text-emerald-300
            "
          >
            Overall Improvement
          </p>

          <p
            className="
              mt-3 text-4xl font-bold
              text-emerald-700

              dark:text-emerald-300
            "
          >
            +{overallImprovement}%
          </p>

          <p
            className="
              mt-3 text-sm leading-6
              text-emerald-700

              dark:text-emerald-400
            "
          >
            Estimated improvement after applying the
            rewritten content.
          </p>
        </article>

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
              flex flex-col gap-5

              sm:flex-row
              sm:items-center
              sm:justify-between
            "
          >
            <div>
              <p
                className="
                  text-sm font-semibold
                  text-[var(--text-secondary)]
                "
              >
                Resume Word Count
              </p>

              <h3
                className="
                  mt-2 text-xl font-bold
                  text-[var(--text-primary)]
                "
              >
                Content comparison
              </h3>
            </div>

            <div
              className="
                flex items-center gap-3
              "
            >
              <WordCountBadge
                label="Original"
                value={originalWordCount}
              />

              <span
                className="
                  text-xl font-bold
                  text-[var(--primary)]
                "
              >
                →
              </span>

              <WordCountBadge
                label="Rewritten"
                value={rewrittenWordCount}
              />
            </div>
          </div>

          <p
            className="
              mt-5 text-sm leading-6
              text-[var(--text-secondary)]
            "
          >
            The rewritten count includes the improved
            summary, experience and project content
            generated for the selected career.
          </p>
        </article>
      </div>
    </section>
  );
}


function QualityMetricCard({
  title,
  score,
  description
}) {
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
        <div>
          <p
            className="
              text-sm font-semibold
              text-[var(--text-secondary)]
            "
          >
            {title}
          </p>

          <p
            className="
              mt-3 text-3xl font-bold
              text-[var(--text-primary)]
            "
          >
            {score}%
          </p>
        </div>

        <div
          className="
            flex h-12 w-12
            items-center justify-center
            rounded-2xl
            bg-[var(--primary-soft)]
            font-bold
            text-[var(--primary)]
          "
        >
          {score}
        </div>
      </div>

      <div
        className="
          mt-5 h-2 overflow-hidden
          rounded-full
          bg-[var(--surface-soft)]
        "
      >
        <div
          className="
            h-full rounded-full
            bg-[var(--primary)]
            transition-all duration-500
          "
          style={{
            width: `${score}%`
          }}
        />
      </div>

      <p
        className="
          mt-4 text-sm
          text-[var(--text-muted)]
        "
      >
        {description}
      </p>
    </article>
  );
}


function WordCountBadge({
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
        text-center
      "
    >
      <p
        className="
          text-xs font-semibold
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


export default ResumeRewrite;