import {
  UploadCloud,
  ScanSearch,
  BrainCircuit,
  BookOpenCheck,
  FileCheck2,
  ArrowDown,
} from "lucide-react";

const steps = [
  {
    icon: <UploadCloud size={42} />,
    title: "Upload Resume",
    desc: "Upload your PDF or DOCX resume securely."
  },
  {
    icon: <ScanSearch size={42} />,
    title: "AI Resume Analysis",
    desc: "Our AI extracts skills, education, experience and projects."
  },
  {
    icon: <BrainCircuit size={42} />,
    title: "Career Prediction",
    desc: "Machine Learning predicts your most suitable career path."
  },
  {
    icon: <BookOpenCheck size={42} />,
    title: "Learning Roadmap",
    desc: "Receive personalized courses to improve missing skills."
  },
  {
    icon: <FileCheck2 size={42} />,
    title: "Career Report",
    desc: "Download a detailed AI-generated career report."
  },
];

function HowItWorks() {
  return (
    <section className="bg-slate-950 py-24">

      <div className="max-w-7xl mx-auto px-6">

        <div className="text-center mb-20">

          <p className="text-indigo-400 uppercase tracking-[6px] mb-3">
            PROCESS
          </p>

          <h2 className="text-5xl font-bold text-white">
            How Career Compass AI Works
          </h2>

          <p className="text-slate-400 mt-6 text-lg max-w-3xl mx-auto">
            Our AI analyzes your resume, predicts your ideal career,
            identifies missing skills and creates a personalized learning roadmap.
          </p>

        </div>

        <div className="grid md:grid-cols-5 gap-8">

          {steps.map((step, index) => (

            <div
              key={index}
              className="relative text-center"
            >

              <div className="w-24 h-24 rounded-full bg-indigo-600/20 border border-indigo-500 flex items-center justify-center mx-auto text-indigo-400">

                {step.icon}

              </div>

              <h3 className="mt-8 text-xl font-semibold text-white">

                {step.title}

              </h3>

              <p className="text-slate-400 mt-4 leading-7">

                {step.desc}

              </p>

              {index !== steps.length - 1 && (
                <div className="hidden md:flex absolute top-12 -right-10 text-indigo-500">
                  <ArrowDown className="rotate-[-90deg]" />
                </div>
              )}

            </div>

          ))}

        </div>

      </div>

    </section>
  );
}

export default HowItWorks;