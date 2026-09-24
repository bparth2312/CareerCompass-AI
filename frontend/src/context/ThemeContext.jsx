import {
  createContext,
  useContext,
  useEffect,
  useState
} from "react";

const ThemeContext = createContext(null);

const THEME_STORAGE_KEY =
  "careercompass-theme";

export function ThemeProvider({
  children
}) {
  const [theme, setTheme] = useState(() => {
    const savedTheme =
      localStorage.getItem(
        THEME_STORAGE_KEY
      );

    if (
      savedTheme === "light" ||
      savedTheme === "dark"
    ) {
      return savedTheme;
    }

    // Every new visitor starts in light mode.
    return "light";
  });

  useEffect(() => {
    const root =
      document.documentElement;

    if (theme === "dark") {
      root.classList.add("dark");
      root.style.colorScheme = "dark";
    } else {
      root.classList.remove("dark");
      root.style.colorScheme = "light";
    }

    localStorage.setItem(
      THEME_STORAGE_KEY,
      theme
    );
  }, [theme]);

  const toggleTheme = () => {
    setTheme((currentTheme) =>
      currentTheme === "dark"
        ? "light"
        : "dark"
    );
  };

  const useLightTheme = () => {
    setTheme("light");
  };

  const useDarkTheme = () => {
    setTheme("dark");
  };

  return (
    <ThemeContext.Provider
      value={{
        theme,
        setTheme,
        toggleTheme,
        useLightTheme,
        useDarkTheme
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context =
    useContext(ThemeContext);

  if (!context) {
    throw new Error(
      "useTheme must be used inside ThemeProvider"
    );
  }

  return context;
}