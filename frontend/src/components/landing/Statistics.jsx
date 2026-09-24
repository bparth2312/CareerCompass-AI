import {
  Users,
  Target,
  Briefcase,
  BookOpen,
  Award,
} from "lucide-react";

const stats = [
  {
    icon: <Users size={38} />,
    value: "5,000+",
    title: "Students Guided",
  },
  {
    icon: <Target size={38} />,
    value: "96%",
    title: "Prediction Accuracy",
  },
  {
    icon: <Briefcase size={38} />,
    value: "150+",
    title: "Career Paths",
  },
  {
    icon: <BookOpen size={38} />,
    value: "250+",
    title: "Learning Resources",
  },
  {
    icon: <Award size={38} />,
    value: "24/7",
    title: "AI Assistance",
  },
];

function Statistics() {
  return (
    <section className="bg-slate-950 py-24">

      <div className="max-w-7xl mx-auto px-6">

        <div className="text-center mb-16">

          <p className="uppercase tracking-[6px] text-indigo-400 mb-3">
            OUR IMPACT
          </p>

          <h2 className="text-5xl font-bold text-white">
            Helping Students Build Better Careers
          </h2>

          <p className="text-slate-400 mt-5 max-w-3xl mx-auto text-lg">
            Career Compass AI combines Artificial Intelligence,
            Machine Learning and Data Analytics to help students
            make smarter career decisions.
          </p>

        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-8">

          {stats.map((item, index) => (

            <div
              key={index}
              className="bg-slate-900 border border-slate-800 rounded-3xl p-8 text-center hover:border-indigo-500 hover:-translate-y-2 transition-all duration-300"
            >

              <div className="text-indigo-400 flex justify-center mb-5">

                {item.icon}

              </div>

              <h2 className="text-4xl font-bold text-white">

                {item.value}

              </h2>

              <p className="text-slate-400 mt-3">

                {item.title}

              </p>

            </div>

          ))}

        </div>

      </div>

    </section>
  );
}

export default Statistics;