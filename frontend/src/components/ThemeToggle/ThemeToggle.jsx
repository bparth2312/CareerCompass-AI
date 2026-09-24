import { FaMoon, FaSun } from "react-icons/fa";
import { useTheme } from "../../context/ThemeContext";

function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  const isDark = theme === "dark";

  return (
    <button
      type="button"
      onClick={toggleTheme}
      aria-label={
        isDark
          ? "Switch to Light Mode"
          : "Switch to Dark Mode"
      }
      title={
        isDark
          ? "Light Mode"
          : "Dark Mode"
      }
      className="
        group
        relative
        flex
        h-12
        w-12
        items-center
        justify-center
        rounded-2xl

        border
        border-slate-200

        bg-white
        text-amber-500

        shadow-sm

        transition-all
        duration-300

        hover:-translate-y-0.5
        hover:border-teal-400
        hover:shadow-lg

        active:scale-95

        dark:border-slate-700
        dark:bg-slate-900
        dark:text-yellow-300
        dark:hover:border-teal-400
      "
    >
      {isDark ? (
        <FaSun
          size={20}
          className="transition-transform duration-300 group-hover:rotate-180"
        />
      ) : (
        <FaMoon
          size={18}
          className="text-slate-700 transition-transform duration-300 group-hover:-rotate-12"
        />
      )}
    </button>
  );
}

export default ThemeToggle;