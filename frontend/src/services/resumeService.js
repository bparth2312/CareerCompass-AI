import api from "./api";

export const uploadResume = async (file) => {
  const formData = new FormData();

  // Must match FastAPI: file: UploadFile = File(...)
  formData.append("file", file);

  const response = await api.post(
    "/resume/upload",
    formData
  );

  return response.data;
};

export const getMyResumes = async () => {
  const response = await api.get(
    "/resume/my-resumes"
  );

  return response.data;
};

export const parseResume = async (resumeId) => {
  const response = await api.post(
    `/resume/${resumeId}/parse`
  );

  return response.data;
};

export const extractResumeSkills = async (resumeId) => {
  const response = await api.post(
    `/resume/${resumeId}/extract-skills`
  );

  return response.data;
};

export const analyzeResumeATS = async (resumeId) => {
  const response = await api.post(
    `/resume/${resumeId}/ats-analysis`
  );

  return response.data;
};

export const predictResumeCareer = async (resumeId) => {
  const response = await api.post(
    `/resume/${resumeId}/predict-career`
  );

  return response.data;
};

export const analyzeResumeSkillGap = async (resumeId) => {
  const response = await api.post(
    `/resume/${resumeId}/skill-gap-analysis`
  );

  return response.data;
};

export const generateLearningRoadmap = async (resumeId) => {
  const response = await api.post(
    `/resume/${resumeId}/learning-roadmap`
  );

  return response.data;
};

export const generateJobRecommendations = async (
  resumeId
) => {
  const response = await api.post(
    `/resume/${resumeId}/job-recommendations`
  );

  return response.data;
};

export const downloadResumeReport = async (resumeId) => {
  const response = await api.get(
    `/resume/${resumeId}/download-report`,
    {
      responseType: "blob"
    }
  );

  return response;
};

export const getResumeHistory = async () => {
  const response = await api.get(
    "/resumes/history"
  );

  return response.data;
};

export const getDashboardStatistics = async () => {
  const response = await api.get(
    "/dashboard/statistics"
  );

  return response.data;
};

export const deleteResume = async (resumeId) => {
  const response = await api.delete(
    `/resume/${resumeId}`
  );

  return response.data;
};

export const getLatestResumeAnalysis = async () => {
  const response = await api.get(
    "/resume/latest-analysis"
  );

  return response.data;
};

export const getLatestLearningResources =
  async () => {
    const response = await api.get(
      "/resume/latest-learning-resources"
    );

    return response.data;
  };

export const analyzeJobDescription = async (
  jobTitle,
  jobDescription
) => {
  const response = await api.post(
    "/resume/job-description-analysis",
    {
      job_title: jobTitle,
      job_description: jobDescription
    }
  );

  return response.data;
};

export const getResumeImprovementSuggestions =
  async () => {
    const response = await api.get(
      "/resume/latest-improvement-suggestions"
    );

    return response.data;
  };

export const getResumeImprovementByCareer =
  async (targetCareer) => {
    const response = await api.post(
      "/resume/improvement-by-career",
      {
        target_career: targetCareer
      }
    );

    return response.data;
  };

export const rewriteResumeByCareer =
  async (targetCareer) => {
    const response = await api.post(
      "/resume/rewrite-by-career",
      {
        target_career: targetCareer
      }
    );

    return response.data;
  };

export const downloadRewrittenResumeDocx =
  async (targetCareer) => {
    const response = await api.post(
      "/resume/download-rewritten-docx",
      {
        target_career: targetCareer
      },
      {
        responseType: "blob"
      }
    );

    return response;
  };

export const downloadRewrittenResumePdf =
  async (targetCareer) => {
    const response = await api.post(
      "/resume/download-rewritten-pdf",
      {
        target_career: targetCareer
      },
      {
        responseType: "blob"
      }
    );

    return response;
  };