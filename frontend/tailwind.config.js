/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"]
      },
      boxShadow: {
        glow: "0 0 40px rgba(20, 184, 166, 0.22)",
        violet: "0 0 45px rgba(168, 85, 247, 0.2)"
      }
    }
  },
  plugins: []
};
