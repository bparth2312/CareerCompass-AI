import {
  CheckCircle,
  TrendingUp,
  BookOpen,
  Briefcase,
} from "lucide-react";

function AIDashboardCard() {
  return (
    <div className="glass-card w-full max-w-md p-6 shadow-2xl">

      <div className="flex items-center justify-between mb-6">

        <h2 className="text-xl font-bold text-white">
          Resume Analysis
        </h2>

        <CheckCircle className="text-green-400" size={24} />

      </div>

      <div className="space-y-5">

        <div>

          <div className="flex justify-between mb-2">
            <span className="text-slate-400">
              ATS Score
            </span>

            <span className="text-green-400 font-bold">
              94%
            </span>
          </div>

          <div className="w-full bg-slate-800 rounded-full h-2">

            <div className="bg-green-400 h-2 rounded-full w-[94%]"></div>

          </div>

        </div>

        <div className="flex justify-between">

          <span className="text-slate-400">
            Career
          </span>

          <span className="text-indigo-400">
            Data Scientist
          </span>

        </div>

        <div className="flex justify-between">

          <span className="text-slate-400">
            Skills Detected
          </span>

          <span className="text-white">
            14
          </span>

        </div>

        <div className="flex justify-between">

          <span className="text-slate-400">
            Missing Skills
          </span>

          <span className="text-red-400">
            4
          </span>

        </div>

      </div>

      <div className="grid grid-cols-3 gap-4 mt-8">

        <div className="glass-card p-4 text-center">

          <TrendingUp className="mx-auto text-indigo-400" />

          <p className="text-xs text-slate-400 mt-2">

            Career Match

          </p>

          <h3 className="font-bold mt-1">
            96%
          </h3>

        </div>

        <div className="glass-card p-4 text-center">

          <BookOpen className="mx-auto text-purple-400" />

          <p className="text-xs text-slate-400 mt-2">

            Courses

          </p>

          <h3 className="font-bold mt-1">
            18
          </h3>

        </div>

        <div className="glass-card p-4 text-center">

          <Briefcase className="mx-auto text-orange-400" />

          <p className="text-xs text-slate-400 mt-2">

            Jobs

          </p>

          <h3 className="font-bold mt-1">
            48
          </h3>

        </div>

      </div>

    </div>
  );
}

export default AIDashboardCard;