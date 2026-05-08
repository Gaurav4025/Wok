import type { Metadata } from 'next';
import { Inter, Playfair_Display } from 'next/font/google';
import './globals.css';
import { Navbar } from '@/components/layout/navbar';
import { Footer } from '@/components/layout/footer';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter', display: 'swap' });
const playfair = Playfair_Display({ subsets: ['latin'], variable: '--font-playfair', display: 'swap' });

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'),
  title: 'Little Wok Story | Wok-tossed Stories, Delivered Hot',
  description:
    'Order Indo-Chinese and Pan-Asian favorites online. Wok bowls, noodles, dim sums and more from Little Wok Story.',
  keywords: ['Best Indo-Chinese food near me', 'Online wok delivery', 'Order Chinese food online'],
  openGraph: {
    title: 'Little Wok Story',
    description: 'Every bowl tells a tale of fire, flavor, and finesse.',
    type: 'website'
  }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${playfair.variable}`}>
      <body className="min-h-screen bg-[#0b1220] text-slate-100">
        <Navbar />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
