/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./tutorial.html'],
  theme: {
    extend: {
      container: {
        center: true,
      },
    },
    fontFamily: {
      display: ['Montserrat', 'sans-serif'],
      body: ['Open Sans', 'sans-serif'],
    },
  },
  plugins: [],
}
