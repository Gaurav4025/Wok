'use client';

import Image from 'next/image';
import Link from 'next/link';
import { lineItemTotal, useCartStore } from '@/store/cart-store';

export default function CartPage() {
  const { items, updateQuantity, removeItem, couponCode, setCoupon } = useCartStore();

  const subTotal = items.reduce((sum, item) => sum + lineItemTotal(item.unitPrice, item.quantity, item.selectedCustomizations), 0);
  const deliveryFee = subTotal > 499 ? 0 : 49;
  const gst = Math.round(subTotal * 0.05);
  const total = subTotal + deliveryFee + gst;

  return (
    <section className="mx-auto grid max-w-7xl gap-8 px-4 py-12 lg:grid-cols-[1.6fr_1fr] sm:px-6 lg:px-8">
      <div>
        <h1 className="font-heading text-6xl">Your Cart</h1>
        <div className="mt-6 space-y-4">
          {items.map((item) => (
            <div key={item.menuId} className="flex gap-4 rounded-2xl border border-slate-700 bg-[#111827] p-4">
              <div className="relative h-20 w-20 overflow-hidden rounded-xl">
                <Image src={item.imageUrl} alt={item.name} fill className="object-cover" />
              </div>
              <div className="flex flex-1 items-center justify-between">
                <div>
                  <p className="font-semibold">{item.name}</p>
                  <p className="text-slate-300">₹{item.unitPrice}</p>
                </div>
                <div className="flex items-center gap-2">
                  <button className="rounded bg-slate-700 px-3 py-1" onClick={() => updateQuantity(item.menuId, item.quantity - 1)}>
                    -
                  </button>
                  <span>{item.quantity}</span>
                  <button className="rounded bg-slate-700 px-3 py-1" onClick={() => updateQuantity(item.menuId, item.quantity + 1)}>
                    +
                  </button>
                </div>
                <button className="text-red-400" onClick={() => removeItem(item.menuId)}>
                  Remove
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
      <aside className="h-fit rounded-2xl border border-slate-700 bg-[#111827] p-6">
        <h2 className="font-heading text-4xl">Summary</h2>
        <div className="mt-6 space-y-3 text-slate-300">
          <div className="flex justify-between"><span>Subtotal</span><span>₹{subTotal}</span></div>
          <div className="flex justify-between"><span>Delivery Fee</span><span>₹{deliveryFee}</span></div>
          <div className="flex justify-between"><span>GST (5%)</span><span>₹{gst}</span></div>
        </div>
        <input
          className="mt-5 w-full rounded-xl border border-slate-700 bg-[#0b1220] px-3 py-2"
          placeholder="Coupon code"
          value={couponCode || ''}
          onChange={(e) => setCoupon(e.target.value || null)}
        />
        <div className="mt-6 flex items-center justify-between border-t border-slate-700 pt-4">
          <span className="text-xl">Total</span>
          <span className="text-3xl font-semibold text-[#f59e0b]">₹{total}</span>
        </div>
        <Link href="/checkout" className="mt-6 block rounded-full bg-[#b91c1c] px-6 py-3 text-center font-semibold hover:bg-[#991b1b]">
          Checkout
        </Link>
      </aside>
    </section>
  );
}
