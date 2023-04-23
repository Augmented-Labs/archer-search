/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",

    // Or if using `src` directory:
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      keyframes: {
        appear: {
          "0%": { opacity: 0 },
          "100%": { opacity: 1 },
        },
      },
      animation: {
        appear: "appear 0.75s cubic-bezier(0.4, 0, 0.6, 1)",
      },
      colors: {
        transparent: "transparent",
        primary: {
          DEFAULT: "#1B4B59",
          100: "rgb(26, 75, 88, 0.1)",
          200: "rgb(26, 75, 88, 0.2)",
          300: "rgb(26, 75, 88, 0.3)",
          400: "rgb(26, 75, 88, 0.4)",
          500: "rgb(26, 75, 88, 0.5)",
          600: "rgb(26, 75, 88, 0.6)",
          700: "rgb(26, 75, 88, 0.7)",
          800: "rgb(26, 75, 88, 0.8)",
          900: "rgb(26, 75, 88, 0.9)",
        },
        secondary: {
          DEFAULT: "#DDEAA3",
          100: "rgb(225, 234, 163, 0.1)",
          200: "rgb(225, 234, 163, 0.2)",
          300: "rgb(225, 234, 163, 0.3)",
          400: "rgb(225, 234, 163, 0.4)",
          500: "rgb(225, 234, 163, 0.5)",
          600: "rgb(225, 234, 163, 0.6)",
          700: "rgb(225, 234, 163, 0.7)",
          800: "rgb(225, 234, 163, 0.8)",
          900: "rgb(225, 234, 163, 0.9)",
        },
      },
      fontFamily: {
        playfair: ["Playfair Display", "serif"],
        inter: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
};
