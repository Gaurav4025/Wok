import Link from 'next/link';

export default function AdminHomePage() {
  return (
    <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <h1 className="font-heading text-6xl">Admin Panel</h1>
      <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[
          ['Menu', '/admin/menu'],
          ['Orders', '/admin/orders'],
          ['Users', '/admin/users'],
          ['Coupons', '/admin/coupons']
        ].map(([name, href]) => (
          <Link key={name} href={href} className="rounded-2xl border border-slate-700 bg-[#111827] p-6 text-center text-xl">
            {name}
          </Link>
        ))}
      </div>
    </section>
  );
}
