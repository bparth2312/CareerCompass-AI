import AIDashboardCard from "../cards/AIDashboardCard";
import { motion } from "framer-motion";
import { ArrowRight, Upload, Sparkles } from "lucide-react";

function Hero() {
  return (
    <section className="relative min-h-screen bg-slate-950 overflow-hidden pt-24">

      {/* Background Glow */}
      <div className="absolute w-[500px] h-[500px] bg-indigo-600/20 rounded-full blur-[120px] -top-32 -left-32"></div>

      <div className="absolute w-[450px] h-[450px] bg-purple-600/20 rounded-full blur-[120px] bottom-0 right-0"></div>

      <div className="max-w-7xl mx-auto px-6 lg:px-8 grid lg:grid-cols-2 items-center gap-12">

        {/* Left */}

        <motion.div
          initial={{ opacity: 0, x: -70 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8 }}
        >

          <span className="inline-flex items-center gap-2 bg-indigo-600/20 text-indigo-300 px-4 py-2 rounded-full text-sm">

            <Sparkles size={18} />

            AI Powered Career Guidance

          </span>

          <h1 className="mt-8 text-6xl font-extrabold leading-tight">

            Discover Your

            <span className="text-indigo-500">

              {" "}Perfect Career{" "}

            </span>

            Using AI

          </h1>

          <p className="mt-8 text-slate-400 text-xl leading-9">

            Upload your resume and let AI analyze your skills,
            identify career opportunities, detect skill gaps,
            recommend learning resources and prepare you for
            your dream job.

          </p>

          <div className="mt-10 flex gap-5">

            <button className="bg-indigo-600 hover:bg-indigo-700 transition px-8 py-4 rounded-xl flex items-center gap-2">

              Get Started

              <ArrowRight size={20} />

            </button>

            <button className="border border-slate-700 px-8 py-4 rounded-xl hover:bg-slate-900 transition">

              Watch Demo

            </button>

          </div>

        </motion.div>

        {/* Right */}

        <motion.div
          initial={{ opacity: 0, x: 70 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8 }}
          className="flex justify-center"
        >

          <div className="relative">

            <AIDashboardCard />

            <div className="absolute -left-12 top-20 bg-slate-900 border border-slate-700 rounded-2xl p-5 shadow-xl">

              <Upload className="text-indigo-400" />

              <p className="mt-2 text-white font-semibold">

                Resume Uploaded

              </p>

            </div>

            <div className="absolute -right-12 bottom-20 bg-slate-900 border border-slate-700 rounded-2xl p-5 shadow-xl">

              <h2 className="text-3xl font-bold text-indigo-400">

                96%

              </h2>

              <p className="text-slate-400">

                Career Match

              </p>

            </div>

          </div>

        </motion.div>

      </div>

    </section>
  );
}

export default Hero;