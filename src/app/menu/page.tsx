'use client';

import { useEffect, useMemo, useState } from 'react';
import { MenuCard } from '@/components/menu/menu-card';
import { categoryLabels, fallbackMenu } from '@/lib/constants';
import type { MenuItem } from '@/lib/types';
import { api } from '@/lib/api';

const categories = ['ALL', 'WOK_BOWLS', 'NOODLES', 'FRIED_RICE', 'DIMSUMS', 'STARTERS', 'SAUCES_ADDONS', 'COMBOS'] as const;

export default function MenuPage() {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState<(typeof categories)[number]>('ALL');
  const [menu, setMenu] = useState<MenuItem[]>(fallbackMenu);

  useEffect(() => {
    api<any[]>('/menu')
      .then((rows) =>
        setMenu(
          rows.map((r) => ({
            id: String(r.id),
            name: r.name,
            description: r.description,
            price: r.price,
            category: r.category,
            imageUrl: r.image_url,
            vegType: r.veg_type,
            spiceLevel: r.spice_level,
            available: r.available,
            customizations: []
          }))
        )
      )
      .catch(() => null);
  }, []);

  const filtered = useMemo(() => {
    return menu.filter((item) => {
      const categoryOk = category === 'ALL' ? true : item.category === category;
      const searchOk = `${item.name} ${item.description}`.toLowerCase().includes(search.toLowerCase());
      return categoryOk && searchOk;
    });
  }, [category, menu, search]);

  return (
    <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <h1 className="font-heading text-6xl">Menu</h1>
      <p className="mt-3 text-slate-300">Wok bowls, noodles, fried rice, dim sums and more.</p>

      <input
        className="mt-8 w-full rounded-2xl border border-slate-700 bg-[#111827] px-4 py-3 outline-none focus:border-[#f59e0b]"
        placeholder="Search dishes, sauces, combos..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <div className="mt-6 flex flex-wrap gap-2">
        {categories.map((c) => (
          <button
            key={c}
            onClick={() => setCategory(c)}
            className={`rounded-full px-4 py-2 text-sm ${
              category === c ? 'bg-[#b91c1c] text-white' : 'border border-slate-700 bg-[#111827] text-slate-300'
            }`}
          >
            {c === 'ALL' ? 'All' : categoryLabels[c]}
          </button>
        ))}
      </div>

      <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {filtered.map((item) => (
          <MenuCard key={item.id} item={item} />
        ))}
      </div>
    </section>
  );
}
