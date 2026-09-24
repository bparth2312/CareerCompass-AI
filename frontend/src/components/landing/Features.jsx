import {
  Brain,
  Target,
  BarChart3,
  BookOpen,
  Briefcase,
  FileText,
} from "lucide-react";

const features = [
  {
    icon: <Brain size={40} />,
    title: "AI Resume Analysis",
    description:
      "Analyze your resume instantly and extract skills, education, projects, and experience."
  },
  {
    icon: <Target size={40} />,
    title: "Career Prediction",
    description:
      "Predict the most suitable career path using Machine Learning algorithms."
  },
  {
    icon: <BarChart3 size={40} />,
    title: "Skill Gap Analysis",
    description:
      "Compare your current skills with industry requirements and identify missing skills."
  },
  {
    icon: <BookOpen size={40} />,
    title: "Learning Recommendation",
    description:
      "Receive personalized courses, certifications, and learning roadmaps."
  },
  {
    icon: <Briefcase size={40} />,
    title: "Job Market Insights",
    description:
      "Discover trending technologies, salary trends, and job demand."
  },
  {
    icon: <FileText size={40} />,
    title: "Career Report",
    description:
      "Generate a complete AI-powered career report with actionable insights."
  },
];

function Features() {
  return (
    <section className="bg-slate-950 py-24">

      <div className="max-w-7xl mx-auto px-6">

        <div className="text-center mb-16">

          <h2 className="text-5xl font-bold text-white">
            Powerful AI Features
          </h2>

          <p className="text-slate-400 mt-5 text-lg max-w-2xl mx-auto">
            Career Compass AI combines Artificial Intelligence,
            Machine Learning, and Data Analytics to guide your career journey.
          </p>

        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">

          {features.map((feature, index) => (

            <div
              key={index}
              className="bg-slate-900 border border-slate-800 rounded-3xl p-8 hover:border-indigo-500 hover:-translate-y-2 transition duration-300"
            >

              <div className="text-indigo-400 mb-6">

                {feature.icon}

              </div>

              <h3 className="text-2xl font-semibold text-white mb-4">

                {feature.title}

              </h3>

              <p className="text-slate-400 leading-8">

                {feature.description}

              </p>

            </div>

          ))}

        </div>

      </div>

    </section>
  );
}

export default Features;