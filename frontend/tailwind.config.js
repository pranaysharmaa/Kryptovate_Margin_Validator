/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0b0e14",
        card: "#121826",
        border: "#1f2937",
        muted: "#9ca3af",
        primary: "#3b82f6",
        success: "#10b981",
        error: "#ef4444",
      },
    },
  },
  plugins: [],
};
