'use client';

import Image from 'next/image';
import { Flame } from 'lucide-react';
import type { MenuItem } from '@/lib/types';
import { useCartStore } from '@/store/cart-store';

export function MenuCard({ item }: { item: MenuItem }) {
  const add = useCartStore((s) => s.addItem);

  return (
    <article className="overflow-hidden rounded-2xl border border-slate-800 bg-[#111827] shadow-soft">
      <div className="relative h-52">
        <Image src={item.imageUrl} alt={item.name} fill className="object-cover" sizes="(max-width: 768px) 100vw, 33vw" />
      </div>
      <div className="space-y-3 p-4">
        <div className="flex items-center justify-between gap-2">
          <h3 className="font-heading text-3xl leading-none">{item.name}</h3>
          <span className={`rounded-full px-2 py-1 text-xs ${item.vegType === 'VEG' ? 'bg-green-700/30 text-green-300' : 'bg-red-700/30 text-red-300'}`}>
            {item.vegType === 'VEG' ? 'Veg' : 'Non-Veg'}
          </span>
        </div>
        <p className="line-clamp-2 text-slate-300">{item.description}</p>
        <div className="flex items-center gap-1 text-[#f59e0b]">
          {Array.from({ length: item.spiceLevel }).map((_, i) => (
            <Flame key={i} size={14} />
          ))}
        </div>
        <div className="flex items-center justify-between">
          <p className="text-3xl font-semibold text-[#f59e0b]">₹{item.price}</p>
          <button
            onClick={() =>
              add({
                menuId: item.id,
                name: item.name,
                imageUrl: item.imageUrl,
                unitPrice: item.price,
                selectedCustomizations: item.customizations
              })
            }
            className="rounded-full bg-[#b91c1c] px-5 py-2 font-semibold hover:bg-[#991b1b]"
          >
            Add to Cart
          </button>
        </div>
      </div>
    </article>
  );
}
