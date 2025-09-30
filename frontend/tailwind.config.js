/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          50: '#f0f8ff',
          100: '#e0f0fe',
          200: '#bae2fd',
          300: '#7cc8fc',
          400: '#36abf8',
          500: '#0d66bb',
          600: '#0952a3',
          700: '#0a4284',
          800: '#0e376e',
          900: '#122f5c',
          950: '#0c1d3d',
        }
      },
      animation: {
        'slideIn': 'slideIn 0.3s ease-out',
      },
      keyframes: {
        slideIn: {
          '0%': { transform: 'translateX(-100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        }
      }
    },
  },
  plugins: [],
}

