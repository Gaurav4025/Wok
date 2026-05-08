'use client';

import Link from 'next/link';
import { useCartStore } from '@/store/cart-store';

export function Navbar() {
  const count = useCartStore((s) => s.items.reduce((a, b) => a + b.quantity, 0));

  return (
    <header className="sticky top-0 z-40 border-b border-slate-800/60 bg-[#0b1220]/90 backdrop-blur">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <Link href="/" className="font-heading text-3xl font-semibold text-[#f59e0b]">
          Little Wok Story
        </Link>
        <div className="flex items-center gap-4">
          <Link href="/menu" className="text-slate-200 hover:text-[#f59e0b]">
            Menu
          </Link>
          <Link href="/dashboard" className="text-slate-200 hover:text-[#f59e0b]">
            My Orders
          </Link>
          <Link
            href="/cart"
            className="rounded-full bg-[#b91c1c] px-4 py-2 font-medium text-white transition hover:bg-[#991b1b]"
          >
            Cart ({count})
          </Link>
          <Link
            href="/login"
            className="rounded-full border border-[#f59e0b] px-4 py-2 font-medium text-[#f59e0b] transition hover:bg-[#f59e0b] hover:text-[#111827]"
          >
            Login
          </Link>
        </div>
      </nav>
    </header>
  );
}
