/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          950: "#0B0D14",
          900: "#12151F",
          800: "#1A1E2B",
          700: "#252A3B",
          600: "#343B52",
        },
        mist: {
          400: "#8891A8",
          300: "#AAB2C5",
          200: "#CBD1E0",
          100: "#E7EAF2",
        },
        signal: {
          teal: "#37D6B8",
          amber: "#F0A94E",
          violet: "#8C7EF2",
        },
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Inter'", "sans-serif"],
      },
      boxShadow: {
        node: "0 0 0 1px rgba(255,255,255,0.06), 0 8px 24px -8px rgba(0,0,0,0.5)",
      },
    },
  },
  plugins: [],
};
