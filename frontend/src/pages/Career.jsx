import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaArrowLeft,
  FaChartLine,
  FaCheckCircle,
  FaExclamationTriangle
} from "react-icons/fa";

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
      .map((item) => item?.msg || "Validation error")
      .join(", ");
  }

  return fallbackMessage;
};


function Career() {
  const navigate = useNavigate();

  const [analysis, setAnalysis] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const loadLatestCareerAnalysis = async () => {
      setIsLoading(true);
      setErrorMessage("");

      try {
        const data =
          await getLatestResumeAnalysis();

        setAnalysis(data);
      } catch (error) {
        console.error(
          "Career analysis loading error:",
          error
        );

        if (error.response?.status === 401) {
          localStorage.removeItem("token");

          navigate("/login", {
            replace: true
          });

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

    loadLatestCareerAnalysis();
  }, [navigate]);

  if (isLoading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-950 px-5 text-white">
        <div className="rounded-2xl border border-slate-800 bg-slate-900 px-10 py-8 text-slate-400">
          Loading career prediction...
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 px-5 py-8 text-white">
      <div className="mx-auto max-w-6xl">

        <header className="flex flex-col gap-5 border-b border-slate-800 pb-7 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="font-semibold text-indigo-400">
              CareerCompass AI
            </p>

            <h1 className="mt-2 text-3xl font-bold">
              Career Prediction
            </h1>

            <p className="mt-2 text-slate-400">
              View career recommendations based on your latest analyzed resume.
            </p>
          </div>

          <button
            type="button"
            onClick={() => navigate("/dashboard")}
            className="flex w-fit items-center gap-2 rounded-xl border border-slate-700 px-5 py-3 text-slate-300 transition hover:border-indigo-500 hover:text-indigo-300"
          >
            <FaArrowLeft />
            Back to Dashboard
          </button>
        </header>

        {errorMessage ? (
          <section className="mt-8 rounded-2xl border border-red-500/30 bg-red-500/10 p-6">
            <div className="flex items-start gap-3">
              <FaExclamationTriangle className="mt-1 text-red-400" />

              <div>
                <h2 className="font-semibold text-red-300">
                  Career prediction unavailable
                </h2>

                <p className="mt-2 text-sm text-red-200">
                  {errorMessage}
                </p>

                <button
                  type="button"
                  onClick={() => navigate("/resume")}
                  className="mt-5 rounded-xl bg-indigo-600 px-5 py-3 font-semibold text-white transition hover:bg-indigo-700"
                >
                  Upload and Analyze Resume
                </button>
              </div>
            </div>
          </section>
        ) : analysis ? (
          <>
            <section className="mt-8 rounded-3xl border border-indigo-500/20 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 p-7">
              <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
                <div>
                  <p className="text-sm font-medium text-indigo-300">
                    Latest analyzed resume
                  </p>

                  <h2 className="mt-2 text-2xl font-bold">
                    {analysis.file_name}
                  </h2>

                  <p className="mt-2 text-slate-400">
                    Best career recommendation
                  </p>

                  <p className="mt-2 text-3xl font-bold text-indigo-400">
                    {analysis.best_career ||
                      "No recommendation available"}
                  </p>
                </div>

                <div className="flex h-28 w-28 items-center justify-center rounded-full border-8 border-indigo-500 bg-slate-900">
                  <FaChartLine className="text-4xl text-indigo-400" />
                </div>
              </div>
            </section>

            <section className="mt-8 space-y-5">
              {analysis.career_predictions?.length > 0 ? (
                analysis.career_predictions.map(
                  (prediction, index) => (
                    <article
                      key={`${prediction.career}-${index}`}
                      className="rounded-2xl border border-slate-800 bg-slate-900 p-6"
                    >
                      <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
                        <div>
                          <div className="flex items-center gap-3">
                            <span className="flex h-9 w-9 items-center justify-center rounded-full bg-indigo-500/10 text-sm font-bold text-indigo-300">
                              {index + 1}
                            </span>

                            <h2 className="text-xl font-semibold">
                              {prediction.career}
                            </h2>
                          </div>

                          <p className="mt-4 max-w-3xl leading-7 text-slate-400">
                            {prediction.description}
                          </p>
                        </div>

                        <div className="shrink-0 md:text-right">
                          <p className="text-3xl font-bold text-indigo-400">
                            {prediction.match_percentage ?? 0}%
                          </p>

                          <p className="text-xs text-slate-500">
                            career match
                          </p>
                        </div>
                      </div>

                      <div className="mt-5 h-3 overflow-hidden rounded-full bg-slate-800">
                        <div
                          className="h-full rounded-full bg-indigo-500 transition-all duration-500"
                          style={{
                            width: `${
                              prediction.match_percentage ?? 0
                            }%`
                          }}
                        />
                      </div>

                      <div className="mt-6 grid gap-6 md:grid-cols-2">
                        <div className="rounded-xl border border-green-500/20 bg-green-500/5 p-5">
                          <h3 className="flex items-center gap-2 font-semibold text-green-300">
                            <FaCheckCircle />
                            Matched Skills
                          </h3>

                          <div className="mt-4 flex flex-wrap gap-2">
                            {prediction.matched_skills?.length > 0 ? (
                              prediction.matched_skills.map(
                                (skill) => (
                                  <span
                                    key={skill}
                                    className="rounded-full border border-green-500/20 bg-green-500/10 px-3 py-1.5 text-xs text-green-300"
                                  >
                                    {skill}
                                  </span>
                                )
                              )
                            ) : (
                              <p className="text-sm text-slate-400">
                                No matching skills found.
                              </p>
                            )}
                          </div>
                        </div>

                        <div className="rounded-xl border border-yellow-500/20 bg-yellow-500/5 p-5">
                          <h3 className="font-semibold text-yellow-300">
                            Skills to Learn
                          </h3>

                          <div className="mt-4 flex flex-wrap gap-2">
                            {prediction.missing_skills?.length > 0 ? (
                              prediction.missing_skills.map(
                                (skill) => (
                                  <span
                                    key={skill}
                                    className="rounded-full border border-yellow-500/20 bg-yellow-500/10 px-3 py-1.5 text-xs text-yellow-300"
                                  >
                                    {skill}
                                  </span>
                                )
                              )
                            ) : (
                              <p className="text-sm text-slate-400">
                                No major missing skills.
                              </p>
                            )}
                          </div>
                        </div>
                      </div>
                    </article>
                  )
                )
              ) : (
                <section className="rounded-2xl border border-yellow-500/20 bg-yellow-500/5 p-6 text-yellow-300">
                  No career predictions were found for your latest resume.
                </section>
              )}
            </section>
          </>
        ) : null}
      </div>
    </main>
  );
}


export default Career;