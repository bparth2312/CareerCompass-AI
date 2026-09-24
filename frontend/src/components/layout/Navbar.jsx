import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="fixed top-0 left-0 w-full z-50 bg-slate-950/70 backdrop-blur-lg border-b border-slate-800">

      <div className="max-w-7xl mx-auto px-8 h-20 flex justify-between items-center">

        <Link
          to="/"
          className="text-3xl font-bold text-indigo-500"
        >
          CareerCompass AI
        </Link>

        <div className="hidden md:flex gap-10 text-slate-300">

          <a href="#features">Features</a>

          <a href="#process">How It Works</a>

          <a href="#about">About</a>

          <a href="#footer">Contact</a>

        </div>

        <div className="flex gap-4">

          <Link
            to="/login"
            className="text-white px-5 py-3 rounded-xl hover:text-indigo-400 transition"
          >
            Login
          </Link>

          <Link
            to="/register"
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-xl transition"
          >
            Register
          </Link>

        </div>

      </div>

    </nav>
  );
}

export default Navbar;