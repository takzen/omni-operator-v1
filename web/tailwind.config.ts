import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: "#8B0000", // Dark Red
        background: "#050505", // Deep black
      },
      fontFamily: {
        mono: ["var(--font-geist-mono)", "monospace"],
      },
    },
  },
  plugins: [],
};
export default config;
