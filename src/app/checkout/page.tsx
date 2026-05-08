'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useCartStore } from '@/store/cart-store';
import { api } from '@/lib/api';
import { addressSchema } from '@/lib/validators';

export default function CheckoutPage() {
  const router = useRouter();
  const { items, clear } = useCartStore();
  const [method, setMethod] = useState<'RAZORPAY' | 'STRIPE' | 'COD'>('RAZORPAY');
  const [street, setStreet] = useState('');
  const [city, setCity] = useState('');
  const [pincode, setPincode] = useState('');
  const [phone, setPhone] = useState('');
  const [error, setError] = useState<string | null>(null);

  const total = items.reduce((sum, i) => sum + i.unitPrice * i.quantity, 0);

  async function placeOrder() {
    try {
      setError(null);
      addressSchema.parse({ street, city, pincode, phone });
      const address = await api<{ id: number }>('/addresses', {
        method: 'POST',
        body: JSON.stringify({ street, city, pincode, phone })
      });

      const order = await api<{ id: number; order_code: string }>('/orders', {
        method: 'POST',
        body: JSON.stringify({
          address_id: address.id,
          payment_method: method,
          items: items.map((i) => ({ menu_id: Number(i.menuId), quantity: i.quantity, customizations: i.selectedCustomizations }))
        })
      });

      if (method === 'RAZORPAY') {
        await api(`/payments/razorpay/create/${order.id}`, { method: 'POST' });
      } else if (method === 'STRIPE') {
        await api(`/payments/stripe/create/${order.id}`, { method: 'POST' });
      }

      clear();
      router.push(`/order-success?orderId=${order.order_code}&method=${method}`);
    } catch (e) {
      setError((e as Error).message || 'Unable to place order');
    }
  }

  return (
    <section className="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
      <h1 className="font-heading text-6xl">Checkout</h1>
      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-slate-700 bg-[#111827] p-6">
          <h2 className="font-heading text-4xl">Delivery Address</h2>
          <div className="mt-4 space-y-3">
            <input className="w-full rounded-xl border border-slate-700 bg-[#0b1220] px-3 py-2" placeholder="Street" value={street} onChange={(e) => setStreet(e.target.value)} />
            <input className="w-full rounded-xl border border-slate-700 bg-[#0b1220] px-3 py-2" placeholder="City" value={city} onChange={(e) => setCity(e.target.value)} />
            <input className="w-full rounded-xl border border-slate-700 bg-[#0b1220] px-3 py-2" placeholder="Pincode" value={pincode} onChange={(e) => setPincode(e.target.value)} />
            <input className="w-full rounded-xl border border-slate-700 bg-[#0b1220] px-3 py-2" placeholder="Phone" value={phone} onChange={(e) => setPhone(e.target.value)} />
          </div>
        </div>

        <div className="rounded-2xl border border-slate-700 bg-[#111827] p-6">
          <h2 className="font-heading text-4xl">Payment</h2>
          <div className="mt-4 space-y-3">
            {['RAZORPAY', 'STRIPE', 'COD'].map((m) => (
              <label key={m} className="flex cursor-pointer items-center gap-2 rounded-xl border border-slate-700 p-3">
                <input type="radio" checked={method === m} onChange={() => setMethod(m as typeof method)} />
                <span>{m === 'COD' ? 'Cash on Delivery' : m}</span>
              </label>
            ))}
          </div>
          <div className="mt-6 flex items-center justify-between">
            <span>Total</span>
            <span className="text-3xl text-[#f59e0b]">₹{total}</span>
          </div>
          {error ? <p className="mt-3 text-sm text-red-400">{error}</p> : null}
          <button onClick={placeOrder} className="mt-6 w-full rounded-full bg-[#b91c1c] px-6 py-3 font-semibold hover:bg-[#991b1b]">
            Place Order
          </button>
        </div>
      </div>
    </section>
  );
}
