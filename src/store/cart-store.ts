'use client';

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { CartItem, CustomizationOption } from '@/lib/types';

interface CartState {
  items: CartItem[];
  couponCode: string | null;
  addItem: (item: Omit<CartItem, 'quantity'>) => void;
  removeItem: (menuId: string) => void;
  updateQuantity: (menuId: string, quantity: number) => void;
  setCoupon: (code: string | null) => void;
  clear: () => void;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      couponCode: null,
      addItem: (item) => {
        const existing = get().items.find((i) => i.menuId === item.menuId);
        if (existing) {
          set({
            items: get().items.map((i) => (i.menuId === item.menuId ? { ...i, quantity: i.quantity + 1 } : i))
          });
          return;
        }
        set({ items: [...get().items, { ...item, quantity: 1 }] });
      },
      removeItem: (menuId) => set({ items: get().items.filter((i) => i.menuId !== menuId) }),
      updateQuantity: (menuId, quantity) => {
        if (quantity <= 0) {
          set({ items: get().items.filter((i) => i.menuId !== menuId) });
          return;
        }
        set({ items: get().items.map((i) => (i.menuId === menuId ? { ...i, quantity } : i)) });
      },
      setCoupon: (code) => set({ couponCode: code }),
      clear: () => set({ items: [], couponCode: null })
    }),
    { name: 'lws-cart-v1' }
  )
);

export function lineItemTotal(unitPrice: number, qty: number, selectedCustomizations: CustomizationOption[]) {
  const extra = selectedCustomizations.reduce((sum, c) => sum + c.price, 0);
  return (unitPrice + extra) * qty;
}
