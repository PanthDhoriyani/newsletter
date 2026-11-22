import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      fontFamily: {
        headline: ["'Playfair Display'", "serif"],
        body: ["'Source Serif 4'", "serif"],
        sans: ["'Inter'", "sans-serif"],
      },
      colors: {
        paper: {
          light: "#faf8f5",
          DEFAULT: "#f5f2eb",
          dark: "#121214",
        },
        ink: {
          light: "#3a3a40",
          DEFAULT: "#18181b",
          dark: "#f4f4f5",
        },
        accent: {
          DEFAULT: "#0f3a60",
          hover: "#154c7d",
          burgundy: "#7a1a24",
          gold: "#b8860b",
        },
        critical: "#dc2626",
        high: "#d97706",
        moderate: "#2563eb",
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};

export default config;
