import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaCheckCircle,
  FaCloudUploadAlt,
  FaCode,
  FaDownload,
  FaFileAlt,
  FaTimesCircle
} from "react-icons/fa";

import {
  analyzeResumeATS,
  analyzeResumeSkillGap,
  downloadResumeReport,
  extractResumeSkills,
  generateJobRecommendations,
  generateLearningRoadmap,
  parseResume,
  predictResumeCareer,
  uploadResume
} from "../services/resumeService";

function ResumeUploader() {
  const navigate = useNavigate();

  const [selectedFile, setSelectedFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);

  const [isUploading, setIsUploading] = useState(false);

  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const allowedExtensions = [".pdf", ".docx"];
  const maxFileSize = 5 * 1024 * 1024;
  const [isDownloading, setIsDownloading] = useState(false);

  const validateFile = (file) => {
    if (!file) {
      return "Please select a resume file.";
    }

    const fileName = file.name.toLowerCase();

    const isAllowed = allowedExtensions.some((extension) =>
      fileName.endsWith(extension)
    );

    if (!isAllowed) {
      return "Only PDF and DOCX files are currently supported.";
    }

    if (file.size > maxFileSize) {
      return "File size must be less than 5 MB.";
    }

    return "";
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    setErrorMessage("");
    setSuccessMessage("");
    setAnalysisResult(null);

    const validationError = validateFile(file);

    if (validationError) {
      setSelectedFile(null);
      setErrorMessage(validationError);
      event.target.value = "";
      return;
    }

    setSelectedFile(file);
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    setErrorMessage("");
    setSuccessMessage("");
    setAnalysisResult(null);
  };

  const handleUpload = async () => {
    const validationError = validateFile(selectedFile);

    if (validationError) {
      setErrorMessage(validationError);
      return;
    }

    setIsUploading(true);
    setErrorMessage("");
    setSuccessMessage("");
    setAnalysisResult(null);

    try {
      // Step 1: Upload resume file
      const uploadedData = await uploadResume(selectedFile);

      // Step 2: Parse resume text
      const parsedData = await parseResume(uploadedData.id);

      // Step 3: Extract technical skills
      const skillData = await extractResumeSkills(uploadedData.id);

      // Step 4: Calculate ATS score
      const atsData = await analyzeResumeATS(uploadedData.id);

      // Step 5: Predict suitable careers
      const careerData = await predictResumeCareer(uploadedData.id);

      // Step 6: Analyze career skill gap
      const skillGapData = await analyzeResumeSkillGap(uploadedData.id);

      // Step 7: Generate personalized learning roadmap
      const learningData = await generateLearningRoadmap(uploadedData.id);

      // Step 8: Generate job recommendations
      const jobData = await generateJobRecommendations(uploadedData.id);

      setAnalysisResult({
       resumeId: uploadedData.id,
       fileName: uploadedData.file_name,

       wordCount: parsedData.word_count,
       characterCount: parsedData.character_count,

       skills: skillData.skills,
       totalSkills: skillData.total_skills,

       atsScore: atsData.ats_score,
       atsRating: atsData.rating,
       strengths: atsData.strengths,
       missingSections: atsData.missing_sections,
       suggestions: atsData.suggestions,

       bestCareer: careerData.best_career,
       careerPredictions: careerData.predictions,

       targetCareer: skillGapData.target_career,
       careerDescription: skillGapData.career_description,
       readinessScore: skillGapData.readiness_score,
       readinessLevel: skillGapData.readiness_level,
       matchedCareerSkills: skillGapData.matched_skills,
       missingCareerSkills: skillGapData.missing_skills,
       prioritySkills: skillGapData.priority_skills,
       estimatedLearningTime:
        skillGapData.estimated_learning_time,
       skillGapSummary: skillGapData.summary,

       learningTargetCareer: learningData.target_career,
       totalRecommendations:
           learningData.total_recommendations,
            learningRoadmap: learningData.roadmap,
            learningMessage: learningData.message,

        bestJob: jobData.best_job,
        totalJobRecommendations:
          jobData.total_recommendations,
        jobRecommendations:
          jobData.recommendations
        });

      setSuccessMessage(
        "Resume uploaded and analyzed successfully."
      );

      setSelectedFile(null);
    } catch (error) {
      console.error("Resume analysis error:", error);

      if (error.response?.status === 401) {
        localStorage.removeItem("token");

        setErrorMessage(
          "Your login session has expired. Please login again."
        );

        setTimeout(() => {
          navigate("/login");
        }, 1500);

        return;
      }

      setErrorMessage(
        error.response?.data?.detail ||
        "Resume analysis failed. Please try again."
      );
    } finally {
      setIsUploading(false);
    }
  };
const handleDownloadReport = async () => {
  if (!analysisResult?.resumeId) {
    setErrorMessage(
      "Please analyze a resume before downloading the report."
    );
    return;
  }

  setIsDownloading(true);
  setErrorMessage("");

  try {
    const response = await downloadResumeReport(
      analysisResult.resumeId
    );

    const pdfBlob = new Blob(
      [response.data],
      {
        type: "application/pdf"
      }
    );

    const downloadUrl = window.URL.createObjectURL(
      pdfBlob
    );

    const contentDisposition =
      response.headers["content-disposition"];

    let fileName = "CareerCompass_Report.pdf";

    if (contentDisposition) {
      const fileNameMatch = contentDisposition.match(
        /filename="?([^"]+)"?/
      );

      if (fileNameMatch?.[1]) {
        fileName = fileNameMatch[1];
      }
    }

    const downloadLink = document.createElement("a");

    downloadLink.href = downloadUrl;
    downloadLink.download = fileName;

    document.body.appendChild(downloadLink);

    downloadLink.click();
    downloadLink.remove();

    window.URL.revokeObjectURL(downloadUrl);
  } catch (error) {
    console.error(
      "PDF report download error:",
      error
    );

    if (error.response?.status === 401) {
      localStorage.removeItem("token");

      setErrorMessage(
        "Your session has expired. Please login again."
      );

      setTimeout(() => {
        navigate("/login");
      }, 1500);

      return;
    }

    let errorDetail = "Unable to download the report.";

    if (error.response?.data instanceof Blob) {
      try {
        const errorText = await error.response.data.text();
        const parsedError = JSON.parse(errorText);

        errorDetail = parsedError.detail || errorDetail;
      } catch {
        errorDetail = "Unable to download the report.";
      }
    } else if (error.response?.data?.detail) {
      errorDetail = error.response.data.detail;
    }

    setErrorMessage(errorDetail);
  } finally {
    setIsDownloading(false);
  }
};
  const formatFileSize = (size) => {
    return `${(size / 1024 / 1024).toFixed(2)} MB`;
  };

  return (
    <div className="w-full">
      <div className="w-full">

        {/* Header */}
        <div className="rounded-3xl border border-[var(--border)] bg-[var(--surface-soft)] p-6 sm:p-8">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-[var(--primary-soft)]">
            <FaCloudUploadAlt className="text-2xl text-[var(--primary)]" />
          </div>

          <h2 className="mt-5 text-2xl font-bold text-[var(--text-primary)]">
            Upload Your Resume
          </h2>

          <p className="mt-3 max-w-2xl leading-7 text-[var(--text-secondary)]">
            Upload your resume to extract text, detect technical skills
            and calculate your ATS score.
          </p>
        </div>

        {/* File selection */}
        <label
          htmlFor="resume-file"
          className="mt-7 flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-[var(--border-strong)] bg-[var(--surface)] px-6 py-10 transition hover:-translate-y-0.5 hover:border-[var(--primary)] hover:bg-[var(--primary-soft)]"
        >
          <FaFileAlt className="text-4xl text-[var(--primary)]" />

          <span className="mt-4 font-semibold text-[var(--text-primary)]">
            Click to select your resume
          </span>

          <span className="mt-2 text-sm text-[var(--text-muted)]">
            PDF or DOCX — maximum 5 MB
          </span>

          <input
            id="resume-file"
            type="file"
            accept=".pdf,.docx"
            onChange={handleFileChange}
            className="hidden"
          />
        </label>

        {/* Selected file */}
        {selectedFile && (
          <div className="mt-6 flex items-center justify-between rounded-2xl border border-[var(--border)] bg-[var(--surface)] p-4">
            <div className="flex min-w-0 items-center gap-3">
              <FaFileAlt className="shrink-0 text-xl text-[var(--primary)]" />

              <div className="min-w-0">
                <p className="truncate font-semibold text-[var(--text-primary)]">
                  {selectedFile.name}
                </p>

                <p className="text-sm text-[var(--text-muted)]">
                  {formatFileSize(selectedFile.size)}
                </p>
              </div>
            </div>

            <button
              type="button"
              onClick={handleRemoveFile}
              className="ml-4 text-[var(--text-muted)] transition hover:text-red-500"
              aria-label="Remove selected file"
            >
              <FaTimesCircle className="text-xl" />
            </button>
          </div>
        )}

        {/* Error message */}
        {errorMessage && (
          <div className="mt-6 flex items-start gap-3 rounded-2xl border border-red-200 bg-red-50 p-4 text-red-700 dark:border-red-900/60 dark:bg-red-950/30 dark:text-red-700 dark:text-red-300">
            <FaTimesCircle className="mt-1 shrink-0" />

            <p>{errorMessage}</p>
          </div>
        )}

        {/* Success summary */}
        {successMessage && (
          <div className="mt-6 rounded-2xl border border-green-200 bg-green-50 p-5 text-green-700 dark:border-green-900/60 dark:bg-green-950/30 dark:text-green-700 dark:text-green-300">
            <div className="flex items-start gap-3">
              <FaCheckCircle className="mt-1 shrink-0" />

              <div>
                <p className="font-semibold">
                  {successMessage}
                </p>

                {analysisResult && (
                  <div className="mt-3 space-y-1 text-sm">
                    <p>
                      File: {analysisResult.fileName}
                    </p>

                    <p>
                      Words extracted: {analysisResult.wordCount}
                    </p>

                    <p>
                      Technical skills found:{" "}
                      {analysisResult.totalSkills}
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Extracted skills */}
        {analysisResult && (
          <div className="mt-7 rounded-3xl border border-[var(--border)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)] sm:p-6 lg:p-8">
            <div className="flex items-center gap-3">
              <FaCode className="text-2xl text-[var(--primary)]" />

              <div>
                <h2 className="text-xl font-bold text-[var(--text-primary)]">
                  Extracted Skills
                </h2>

                <p className="text-sm text-[var(--text-muted)]">
                  {analysisResult.totalSkills} technical skills detected
                </p>
              </div>
            </div>

            {analysisResult.skills.length > 0 ? (
              <div className="mt-5 flex flex-wrap gap-3">
                {analysisResult.skills.map((skill) => (
                  <span
                    key={skill}
                    className="rounded-full border border-[var(--border)] bg-[var(--primary-soft)] px-4 py-2 text-sm font-medium text-[var(--primary)]"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            ) : (
              <p className="mt-5 text-[var(--text-secondary)]">
                No known technical skills were detected.
              </p>
            )}
          </div>
        )}

        {/* ATS analysis */}
        {analysisResult && (
          <div className="mt-7 rounded-3xl border border-[var(--border)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)] sm:p-6 lg:p-8">

            <div className="grid gap-6 rounded-2xl bg-[var(--surface-soft)] p-5 sm:grid-cols-[1fr_auto] sm:items-center">
              <div>
                <p className="text-sm font-medium text-[var(--text-secondary)]">
                  ATS Resume Score
                </p>

                <h2 className="mt-2 text-4xl font-bold text-[var(--text-primary)]">
                  {analysisResult.atsScore}%
                </h2>

                <p className="mt-1 font-semibold text-[var(--primary)]">
                  {analysisResult.atsRating}
                </p>
              </div>

              <div className="flex h-24 w-24 items-center justify-center rounded-full border-8 border-[var(--primary)] bg-[var(--surface)] shadow-sm sm:h-28 sm:w-28">
                <span className="text-2xl font-bold text-[var(--text-primary)]">
                  {analysisResult.atsScore}
                </span>
              </div>
            </div>

            <div className="mt-6 grid gap-4 lg:grid-cols-[1.05fr_1fr_1.35fr]">

              {/* Strengths */}
              <div className="rounded-2xl border border-green-300 bg-green-50 p-5 dark:border-green-500/30 dark:bg-green-500/15">
                <h3 className="font-semibold text-green-700 dark:text-green-300">
                  Strengths
                </h3>

                <div className="mt-4 space-y-3">
                  {analysisResult.strengths.length > 0 ? (
                    analysisResult.strengths.map((strength) => (
                      <p
                        key={strength}
                        className="text-sm leading-6 text-[var(--text-secondary)]"
                      >
                        ✓ {strength}
                      </p>
                    ))
                  ) : (
                    <p className="text-sm text-[var(--text-muted)]">
                      No strengths detected.
                    </p>
                  )}
                </div>
              </div>

              {/* Missing sections */}
              <div className="rounded-2xl border border-red-300 bg-red-50 p-5 dark:border-red-500/30 dark:bg-red-500/15">
                <h3 className="font-semibold text-red-700 dark:text-red-300">
                  Missing Sections
                </h3>

                <div className="mt-4 space-y-3">
                  {analysisResult.missingSections.length > 0 ? (
                    analysisResult.missingSections.map((section) => (
                      <p
                        key={section}
                        className="text-sm leading-6 text-[var(--text-secondary)]"
                      >
                        ✕ {section}
                      </p>
                    ))
                  ) : (
                    <p className="text-sm text-[var(--text-secondary)]">
                      No major sections are missing.
                    </p>
                  )}
                </div>
              </div>

              {/* Suggestions */}
              <div className="rounded-2xl border border-amber-300 bg-amber-50 p-5 dark:border-amber-500/30 dark:bg-amber-500/10">
                <h3 className="font-semibold text-amber-700 dark:text-amber-300">
                  Suggestions
                </h3>

                <div className="mt-4 space-y-3">
                  {analysisResult.suggestions.length > 0 ? (
                    analysisResult.suggestions.map((suggestion) => (
                      <p
                        key={suggestion}
                        className="text-sm leading-6 text-[var(--text-secondary)]"
                      >
                        • {suggestion}
                      </p>
                    ))
                  ) : (
                    <p className="text-sm text-[var(--text-muted)]">
                      No major improvements required.
                    </p>
                  )}
                </div>
              </div>

            </div>
          </div>
        )}

        {/* Career predictions */}
        {analysisResult && (
           <div className="mt-7 rounded-3xl border border-[var(--border)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)] sm:p-6 lg:p-8">
          <div>
            <p className="text-sm font-medium text-[var(--primary)]">
               Recommended Career
            </p>

            <h2 className="mt-2 text-2xl font-bold text-[var(--text-primary)]">
             {analysisResult.bestCareer ||
               "No career recommendation available"}
             </h2>

          <p className="mt-2 text-sm text-[var(--text-secondary)]">
        Recommendations are calculated by comparing your
        extracted skills with the requirements of different
        career roles.
      </p>
    </div>

    <div className="mt-6 space-y-5">
      {analysisResult.careerPredictions?.length > 0 ? (
        analysisResult.careerPredictions.map(
          (prediction, index) => (
            <div
              key={prediction.career}
              className="rounded-2xl border border-[var(--border)] bg-[var(--surface-soft)] p-5"
            >
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <div className="flex items-center gap-3">
                    <span className="flex h-8 w-8 items-center justify-center rounded-full bg-[var(--primary-soft)] text-sm font-bold text-[var(--primary)]">
                      {index + 1}
                    </span>

                    <h3 className="font-semibold text-[var(--text-primary)]">
                      {prediction.career}
                    </h3>
                  </div>

                  <p className="mt-3 text-sm leading-6 text-[var(--text-secondary)]">
                    {prediction.description}
                  </p>
                </div>

                <div className="shrink-0">
                  <span className="text-2xl font-bold text-[var(--primary)]">
                    {prediction.match_percentage}%
                  </span>

                  <p className="text-xs text-[var(--text-muted)]">
                    career match
                  </p>
                </div>
              </div>

              <div className="progress-track mt-4">
                <div
                  className="progress-value"
                  style={{
                    width: `${prediction.match_percentage}%`
                  }}
                />
              </div>

              <div className="mt-5 grid gap-5 md:grid-cols-2">
                <div>
                  <h4 className="text-sm font-semibold text-green-700 dark:text-green-300">
                    Matched Skills
                  </h4>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {prediction.matched_skills.length > 0 ? (
                      prediction.matched_skills.map(
                        (skill) => (
                          <span
                            key={skill}
                            className="rounded-full border border-green-300 dark:border-green-500/30 bg-green-100 dark:bg-green-500/15 px-3 py-1 text-xs text-green-700 dark:text-green-300"
                          >
                            {skill}
                          </span>
                        )
                      )
                    ) : (
                      <p className="text-sm text-[var(--text-muted)]">
                        No matching skills found.
                      </p>
                    )}
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-semibold text-amber-700 dark:text-amber-300">
                    Skills to Learn
                  </h4>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {prediction.missing_skills.length > 0 ? (
                      prediction.missing_skills.map(
                        (skill) => (
                          <span
                            key={skill}
                            className="rounded-full border border-amber-300 dark:border-amber-500/30 bg-amber-100 dark:bg-amber-500/15 px-3 py-1 text-xs text-amber-700 dark:text-amber-300"
                          >
                            {skill}
                          </span>
                        )
                      )
                    ) : (
                      <p className="text-sm text-[var(--text-muted)]">
                        You have all listed skills.
                      </p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )
        )
      ) : (
        <p className="mt-5 text-[var(--text-secondary)]">
          No career predictions were generated.
        </p>
      )}
    </div>
  </div>
)} 

        {/* Skill gap analysis */}
{analysisResult && (
  <div className="mt-7 rounded-3xl border border-[var(--border)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)] sm:p-6 lg:p-8">
    <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
      <div>
        <p className="text-sm font-medium text-[var(--primary)]">
          Career Readiness
        </p>

        <h2 className="mt-2 text-2xl font-bold text-[var(--text-primary)]">
          {analysisResult.targetCareer}
        </h2>

        <p className="mt-2 max-w-2xl text-sm leading-6 text-[var(--text-secondary)]">
          {analysisResult.skillGapSummary}
        </p>
      </div>

      <div className="shrink-0 text-center">
        <div className="flex h-32 w-32 items-center justify-center rounded-full border-8 border-cyan-500 bg-[var(--surface)]">
          <div>
            <p className="text-3xl font-bold text-[var(--text-primary)]">
              {analysisResult.readinessScore}%
            </p>

            <p className="mt-1 text-xs text-[var(--text-secondary)]">
              readiness
            </p>
          </div>
        </div>

        <p className="mt-3 font-semibold text-[var(--primary)]">
          {analysisResult.readinessLevel}
        </p>
      </div>
    </div>

    <div className="mt-6">
      <div className="flex items-center justify-between text-sm">
        <span className="text-[var(--text-secondary)]">
          Career preparation progress
        </span>

        <span className="font-medium text-[var(--text-primary)]">
          {analysisResult.readinessScore}%
        </span>
      </div>

      <div className="progress-track mt-3">
        <div
          className="progress-value"
          style={{
            width: `${analysisResult.readinessScore}%`
          }}
        />
      </div>
    </div>

    <div className="mt-8 grid gap-6 md:grid-cols-2">
      <div className="rounded-xl border border-green-300 dark:border-green-500/30 bg-green-50 dark:bg-green-500/15 p-5">
        <h3 className="font-semibold text-green-700 dark:text-green-300">
          Skills You Already Have
        </h3>

        <div className="mt-4 flex flex-wrap gap-2">
          {analysisResult.matchedCareerSkills?.length > 0 ? (
            analysisResult.matchedCareerSkills.map(
              (skill) => (
                <span
                  key={skill}
                  className="rounded-full border border-green-300 dark:border-green-500/30 bg-green-100 dark:bg-green-500/15 px-3 py-1.5 text-xs text-green-700 dark:text-green-300"
                >
                  ✓ {skill}
                </span>
              )
            )
          ) : (
            <p className="text-sm text-[var(--text-secondary)]">
              No matching career skills were found.
            </p>
          )}
        </div>
      </div>

      <div className="rounded-xl border border-red-300 dark:border-red-500/30 bg-red-50 dark:bg-red-500/15 p-5">
        <h3 className="font-semibold text-red-700 dark:text-red-300">
          Missing Career Skills
        </h3>

        <div className="mt-4 flex flex-wrap gap-2">
          {analysisResult.missingCareerSkills?.length > 0 ? (
            analysisResult.missingCareerSkills.map(
              (skill) => (
                <span
                  key={skill}
                  className="rounded-full border border-red-300 dark:border-red-500/30 bg-red-100 dark:bg-red-500/15 px-3 py-1.5 text-xs text-red-700 dark:text-red-300"
                >
                  ✕ {skill}
                </span>
              )
            )
          ) : (
            <p className="text-sm text-[var(--text-secondary)]">
              No major skill gaps found.
            </p>
          )}
        </div>
      </div>
    </div>

    <div className="mt-6 grid gap-6 md:grid-cols-2">
      <div className="rounded-xl border border-amber-300 dark:border-amber-500/30 bg-amber-50 dark:bg-amber-500/10 p-5">
        <h3 className="font-semibold text-amber-700 dark:text-amber-300">
          Priority Skills to Learn
        </h3>

        <div className="mt-4 space-y-3">
          {analysisResult.prioritySkills?.length > 0 ? (
            analysisResult.prioritySkills.map(
              (skill, index) => (
                <div
                  key={skill}
                  className="flex items-center gap-3 rounded-lg border border-[var(--border)] bg-[var(--surface)] p-3"
                >
                  <span className="flex h-7 w-7 items-center justify-center rounded-full bg-amber-100 dark:bg-amber-500/15 text-xs font-bold text-amber-700 dark:text-amber-300">
                    {index + 1}
                  </span>

                  <span className="text-sm text-[var(--text-primary)]">
                    {skill}
                  </span>
                </div>
              )
            )
          ) : (
            <p className="text-sm text-[var(--text-secondary)]">
              No priority skills are currently required.
            </p>
          )}
        </div>
      </div>

      <div className="rounded-xl border border-[var(--border)] bg-[var(--primary)]/5 p-5">
        <h3 className="font-semibold text-[var(--primary)]">
          Estimated Learning Time
        </h3>

        <p className="mt-5 text-3xl font-bold text-[var(--text-primary)]">
          {analysisResult.estimatedLearningTime}
        </p>

        <p className="mt-3 text-sm leading-6 text-[var(--text-secondary)]">
          This estimate is based on the number of missing
          skills. Actual time may vary depending on your
          experience and daily study schedule.
        </p>
      </div>
    </div>
  </div>
)}

           {/* Learning roadmap */}
{analysisResult && (
  <div className="mt-7 rounded-3xl border border-[var(--border)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)] sm:p-6 lg:p-8">
    <div>
      <p className="text-sm font-medium text-[var(--primary)]">
        Personalized Learning Plan
      </p>

      <h2 className="mt-2 text-2xl font-bold text-[var(--text-primary)]">
        Learning Roadmap for{" "}
        {analysisResult.learningTargetCareer}
      </h2>

      <p className="mt-2 text-sm leading-6 text-[var(--text-secondary)]">
        {analysisResult.learningMessage}
      </p>

      <p className="mt-3 text-sm text-[var(--text-muted)]">
        {analysisResult.totalRecommendations} learning steps
        recommended
      </p>
    </div>

    <div className="mt-7 space-y-6">
      {analysisResult.learningRoadmap?.length > 0 ? (
        analysisResult.learningRoadmap.map((item) => (
          <div
            key={`${item.order}-${item.skill}`}
            className="rounded-2xl border border-[var(--border)] bg-[var(--surface-soft)] p-5"
          >
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
              <div className="flex items-start gap-4">
                <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[var(--primary-soft)] font-bold text-[var(--primary)]">
                  {item.order}
                </span>

                <div>
                  <div className="flex flex-wrap items-center gap-3">
                    <h3 className="text-lg font-semibold text-[var(--text-primary)]">
                      {item.skill}
                    </h3>

                    {item.is_priority && (
                      <span className="rounded-full border border-amber-300 dark:border-amber-500/40 bg-amber-100 dark:bg-amber-500/15 px-3 py-1 text-xs font-medium text-amber-700 dark:text-amber-300">
                        Priority
                      </span>
                    )}
                  </div>

                  <div className="mt-3 flex flex-wrap gap-3 text-xs">
                    <span className="rounded-full border border-[var(--border)] bg-[var(--primary-soft)] px-3 py-1.5 text-[var(--primary)]">
                      {item.difficulty}
                    </span>

                    <span className="rounded-full border border-[var(--border)] bg-[var(--primary)]/10 px-3 py-1.5 text-[var(--primary)]">
                      {item.duration}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-6 grid gap-6 md:grid-cols-2">
              <div>
                <h4 className="text-sm font-semibold text-slate-200">
                  Learning Resources
                </h4>

                <div className="mt-3 space-y-3">
                  {item.resources.map((resource) => (
                    <a
                      key={`${item.skill}-${resource.title}`}
                      href={resource.url || "#"}
                      target="_blank"
                      rel="noreferrer"
                      className="block rounded-lg border border-[var(--border)] bg-[var(--background)] p-3 transition hover:border-[var(--primary)]"
                    >
                      <p className="text-sm font-medium text-[var(--text-primary)]">
                        {resource.title}
                      </p>

                      <p className="mt-1 text-xs text-[var(--text-muted)]">
                        {resource.provider} · {resource.type}
                      </p>
                    </a>
                  ))}
                </div>
              </div>

              <div className="space-y-5">
                <div>
                  <h4 className="text-sm font-semibold text-green-700 dark:text-green-300">
                    Mini Project
                  </h4>

                  <p className="mt-2 text-sm leading-6 text-[var(--text-secondary)]">
                    {item.mini_project}
                  </p>
                </div>

                <div>
                  <h4 className="text-sm font-semibold text-amber-700 dark:text-amber-300">
                    Suggested Certification
                  </h4>

                  <p className="mt-2 text-sm leading-6 text-[var(--text-secondary)]">
                    {item.certification ||
                      "No specific certification required."}
                  </p>
                </div>
              </div>
            </div>
          </div>
        ))
      ) : (
        <div className="rounded-xl border border-green-300 dark:border-green-500/30 bg-green-50 dark:bg-green-500/15 p-5">
          <p className="text-sm text-green-700 dark:text-green-300">
            No major learning gaps were found. Focus on
            advanced projects and interview preparation.
          </p>
        </div>
      )}
    </div>
  </div>
)}

        {/* Job recommendations */}
{analysisResult && (
  <div className="mt-7 rounded-3xl border border-[var(--border)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)] sm:p-6 lg:p-8">
    <div>
      <p className="text-sm font-medium text-[var(--primary)]">
        Recommended Job Opportunities
      </p>

      <h2 className="mt-2 text-2xl font-bold text-[var(--text-primary)]">
        Best Job Match:{" "}
        {analysisResult.bestJob ||
          "No job recommendation available"}
      </h2>

      <p className="mt-2 text-sm leading-6 text-[var(--text-secondary)]">
        These roles are recommended by comparing your
        extracted skills, predicted career paths and
        career-readiness score.
      </p>

      <p className="mt-3 text-sm text-[var(--text-muted)]">
        {analysisResult.totalJobRecommendations} suitable
        roles found
      </p>
    </div>

    <div className="mt-7 space-y-6">
      {analysisResult.jobRecommendations?.length > 0 ? (
        analysisResult.jobRecommendations.map(
          (job, index) => (
            <div
              key={job.job_title}
              className="rounded-2xl border border-[var(--border)] bg-[var(--surface-soft)] p-5"
            >
              <div className="flex flex-col gap-5 md:flex-row md:items-start md:justify-between">
                <div className="flex items-start gap-4">
                  <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[var(--primary-soft)] font-bold text-[var(--primary)]">
                    {index + 1}
                  </span>

                  <div>
                    <h3 className="text-lg font-semibold text-[var(--text-primary)]">
                      {job.job_title}
                    </h3>

                    <div className="mt-2 flex flex-wrap gap-2">
                      <span className="rounded-full border border-[var(--border)] bg-[var(--primary-soft)] px-3 py-1 text-xs text-[var(--primary)]">
                        {job.career_category}
                      </span>

                      <span className="rounded-full border border-[var(--border)] bg-[var(--primary)]/10 px-3 py-1 text-xs text-[var(--primary)]">
                        {job.experience_level}
                      </span>

                      <span className="rounded-full border border-green-300 dark:border-green-500/30 bg-green-100 dark:bg-green-500/15 px-3 py-1 text-xs text-green-700 dark:text-green-300">
                        {job.application_status}
                      </span>
                    </div>

                    <p className="mt-4 max-w-2xl text-sm leading-6 text-[var(--text-secondary)]">
                      {job.description}
                    </p>
                  </div>
                </div>

                <div className="shrink-0 text-left md:text-right">
                  <p className="text-3xl font-bold text-[var(--primary)]">
                    {job.recommendation_score}%
                  </p>

                  <p className="text-xs text-[var(--text-muted)]">
                    recommendation score
                  </p>
                </div>
              </div>

              <div className="mt-5">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-[var(--text-secondary)]">
                    Skill match
                  </span>

                  <span className="font-medium text-[var(--text-primary)]">
                    {job.match_percentage}%
                  </span>
                </div>

                <div className="progress-track mt-2">
                  <div
                    className="progress-value"
                    style={{
                      width: `${job.match_percentage}%`
                    }}
                  />
                </div>
              </div>

              <div className="mt-6 grid gap-6 md:grid-cols-2">
                <div className="rounded-lg border border-green-300 dark:border-green-500/30 bg-green-50 dark:bg-green-500/15 p-4">
                  <h4 className="text-sm font-semibold text-green-700 dark:text-green-300">
                    Matched Skills
                  </h4>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {job.matched_skills.length > 0 ? (
                      job.matched_skills.map((skill) => (
                        <span
                          key={skill}
                          className="rounded-full border border-green-300 dark:border-green-500/30 bg-green-100 dark:bg-green-500/15 px-3 py-1 text-xs text-green-700 dark:text-green-300"
                        >
                          ✓ {skill}
                        </span>
                      ))
                    ) : (
                      <p className="text-sm text-[var(--text-muted)]">
                        No matching skills found.
                      </p>
                    )}
                  </div>
                </div>

                <div className="rounded-lg border border-amber-300 dark:border-amber-500/30 bg-amber-50 dark:bg-amber-500/10 p-4">
                  <h4 className="text-sm font-semibold text-amber-700 dark:text-amber-300">
                    Skills to Improve
                  </h4>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {job.missing_skills.length > 0 ? (
                      job.missing_skills.map((skill) => (
                        <span
                          key={skill}
                          className="rounded-full border border-amber-300 dark:border-amber-500/30 bg-amber-100 dark:bg-amber-500/15 px-3 py-1 text-xs text-amber-700 dark:text-amber-300"
                        >
                          {skill}
                        </span>
                      ))
                    ) : (
                      <p className="text-sm text-[var(--text-secondary)]">
                        No major missing skills.
                      </p>
                    )}
                  </div>
                </div>
              </div>

              <div className="mt-5 rounded-lg border border-[var(--border)] bg-[var(--primary)]/5 p-4">
                <h4 className="text-sm font-semibold text-[var(--primary)]">
                  Application Advice
                </h4>

                <p className="mt-2 text-sm leading-6 text-[var(--text-secondary)]">
                  {job.preparation_advice}
                </p>
              </div>
            </div>
          )
        )
      ) : (
        <div className="rounded-xl border border-amber-300 dark:border-amber-500/30 bg-amber-50 dark:bg-amber-500/10 p-5">
          <p className="text-sm text-amber-700 dark:text-amber-300">
            No job recommendations were generated.
          </p>
        </div>
      )}
    </div>
  </div>
)}
        {/* PDF report download */}
{analysisResult && (
  <div className="mt-7 rounded-2xl border border-teal-300 bg-teal-100 p-6 shadow-sm dark:border-teal-700 dark:bg-teal-950/40">
    <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="text-sm font-medium text-[var(--primary)]">
          Complete Career Analysis
        </p>

        <h2 className="mt-2 text-xl font-bold text-[var(--text-primary)]">
          Download Your PDF Report
        </h2>

        <p className="mt-2 max-w-2xl text-sm leading-6 text-[var(--text-secondary)]">
          Download a complete report containing your ATS
          score, extracted skills, career matches, skill
          gaps, learning roadmap and job recommendations.
        </p>
      </div>

      <button
        type="button"
        onClick={handleDownloadReport}
        disabled={isDownloading}
        className="flex shrink-0 items-center justify-center gap-2 rounded-xl bg-teal-700 px-6 py-3 font-semibold text-white shadow-sm transition hover:bg-teal-800 disabled:cursor-not-allowed disabled:opacity-60 dark:bg-teal-400 dark:text-slate-950 dark:hover:bg-teal-300"
      >
        <FaDownload />

        {isDownloading
          ? "Generating PDF..."
          : "Download PDF"}
      </button>
    </div>
  </div>
)}
        {/* Upload button */}
        <button
          type="button"
          onClick={handleUpload}
          disabled={!selectedFile || isUploading}
          className="mt-7 w-full rounded-xl bg-teal-700 px-6 py-4 font-semibold text-white shadow-sm transition hover:bg-teal-800 disabled:cursor-not-allowed disabled:bg-slate-500 disabled:text-white disabled:opacity-80 dark:bg-teal-400 dark:text-slate-950 dark:hover:bg-teal-300 dark:disabled:bg-slate-700 dark:disabled:text-slate-300"
        >
          {isUploading
            ? "Analyzing your resume..."
            : "Upload and Analyze Resume"}
        </button>

      </div>
    </div>
  );
}

export default ResumeUploader;