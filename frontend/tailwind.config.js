/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'canvas-base': '#07080A',
        'surface-primary': '#0D0F13',
        'surface-secondary': '#11141A',
        'surface-elevated': '#161A21',
        'border-color': '#252A33',
        'border-elevated': '#343A46',
        
        'accent-cyan': '#22D3EE',
        'accent-purple': '#8B5CF6',
        'accent-blue': '#60A5FA',
        'accent-green': '#34D399',
        'accent-orange': '#FB923C',
        'accent-red': '#F87171',
      },
      fontFamily: {
        display: ['Syne', 'sans-serif'],
        sans: ['Hanken Grotesk', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
