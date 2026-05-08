'use client';

import { motion } from 'framer-motion';
import Image from 'next/image';
import Link from 'next/link';

export function Hero() {
  return (
    <section className="smoky-bg relative overflow-hidden px-4 py-16 sm:px-6 lg:px-8 lg:py-24">
      <div className="steam left-[58%] top-[48%]" />
      <div className="steam left-[62%] top-[48%] [animation-delay:1s]" />
      <div className="steam left-[65%] top-[48%] [animation-delay:1.8s]" />
      <div className="mx-auto grid max-w-7xl items-center gap-12 lg:grid-cols-2">
        <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7 }}>
          <p className="mb-2 text-sm uppercase tracking-[0.24em] text-[#f59e0b]">Little Wok Story</p>
          <h1 className="font-heading text-5xl leading-tight text-white sm:text-6xl">
            Wok-tossed Stories, <span className="text-[#f59e0b]">Delivered Hot</span>
          </h1>
          <p className="mt-6 max-w-2xl text-lg text-slate-200">
            Every bowl at Little Wok Story tells a tale of fire, flavor, and finesse. Indo-Chinese comfort, crafted fresh,
            delivered in 30 minutes.
          </p>
          <div className="mt-8 flex flex-wrap gap-4">
            <Link href="/menu" className="rounded-full bg-[#b91c1c] px-8 py-3 font-semibold text-white hover:bg-[#991b1b]">
              Order Now
            </Link>
            <Link
              href="/menu"
              className="rounded-full border border-[#f59e0b] px-8 py-3 font-semibold text-[#f59e0b] hover:bg-[#f59e0b] hover:text-[#111827]"
            >
              View Menu
            </Link>
          </div>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="relative"
        >
          <Image
            src="https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=1400&q=80"
            alt="Wok tossed noodles"
            width={760}
            height={560}
            className="rounded-2xl shadow-soft"
            priority
          />
          <div className="absolute -bottom-6 left-4 rounded-2xl bg-[#111827] px-6 py-4 shadow-soft">
            <p className="font-heading text-3xl text-[#f59e0b]">30 min</p>
            <p className="text-slate-300">Quick delivery, always hot</p>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
