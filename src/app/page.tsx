import Script from 'next/script';
import { Hero } from '@/components/home/hero';
import { MenuCard } from '@/components/menu/menu-card';
import { fallbackMenu } from '@/lib/constants';

export default function HomePage() {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Restaurant',
    name: 'Little Wok Story',
    servesCuisine: ['Indo-Chinese', 'Pan-Asian'],
    hasMenu: '/menu',
    acceptsReservations: 'False',
    slogan: 'Wok-tossed Stories, Delivered Hot'
  };

  return (
    <div>
      <Script id="lws-jsonld" type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <Hero />
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="mb-10 flex items-end justify-between">
          <h2 className="font-heading text-5xl">Featured Dishes</h2>
          <a href="/menu" className="text-[#f59e0b]">Explore Full Menu</a>
        </div>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {fallbackMenu.map((dish) => (
            <MenuCard key={dish.id} item={dish} />
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <h2 className="font-heading text-5xl">Why Choose Us</h2>
        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {['Fresh Ingredients', 'Made to Order', '30-minute delivery', 'Hygienic kitchen'].map((item) => (
            <div key={item} className="rounded-2xl border border-slate-700 bg-[#111827] p-6">
              <h3 className="font-heading text-3xl text-[#f59e0b]">{item}</h3>
              <p className="mt-3 text-slate-300">Flavor-first process to keep every box hot, crisp, and balanced.</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <h2 className="font-heading text-5xl">What Our Customers Say</h2>
        <div className="mt-8 grid gap-6 lg:grid-cols-3">
          {[
            { n: 'Priya Sharma', q: 'Best Indo-Chinese food in Kolkata. The wok bowls are absolutely delicious.' },
            { n: 'Rahul Verma', q: 'Authentic flavors and always delivered hot. My go-to for late-night cravings.' },
            { n: 'Ananya Das', q: 'The dim sums are heavenly. Great quality at affordable prices.' }
          ].map((r) => (
            <div key={r.n} className="rounded-2xl border border-slate-700 bg-[#111827] p-6">
              <p className="font-semibold">{r.n}</p>
              <p className="mt-1 text-[#f59e0b]">★★★★★</p>
              <p className="mt-4 text-slate-300">“{r.q}”</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
