/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      gridTemplateColumns: {
        "sidebar": "200px auto",
        "sidebar-collapsed": "64px auto"
    },
  },
  plugins: []
}}
