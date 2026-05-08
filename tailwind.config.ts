import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          red: '#B91C1C',
          charcoal: '#111827',
          gold: '#F59E0B'
        }
      },
      fontFamily: {
        heading: ['var(--font-playfair)', 'serif'],
        body: ['var(--font-inter)', 'sans-serif']
      },
      boxShadow: {
        soft: '0 12px 40px rgba(0,0,0,0.22)'
      },
      borderRadius: {
        '2xl': '1.25rem'
      },
      backgroundImage: {
        smoky:
          'radial-gradient(circle at 20% 20%, rgba(245,158,11,0.25), transparent 50%), radial-gradient(circle at 80% 0%, rgba(185,28,28,0.25), transparent 45%), linear-gradient(180deg,#111827 0%,#0B1220 100%)'
      }
    }
  },
  plugins: []
};

export default config;
