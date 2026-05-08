export default function DashboardPage() {
  return (
    <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <h1 className="font-heading text-6xl">My Dashboard</h1>
      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-slate-700 bg-[#111827] p-6">
          <h2 className="font-heading text-4xl">Order History</h2>
          <ul className="mt-4 space-y-3 text-slate-300">
            <li>#LWS-10021 - Delivered - ₹499</li>
            <li>#LWS-10004 - Out for Delivery - ₹699</li>
          </ul>
        </div>
        <div className="rounded-2xl border border-slate-700 bg-[#111827] p-6">
          <h2 className="font-heading text-4xl">Profile & Addresses</h2>
          <p className="mt-4 text-slate-300">Update profile, save multiple addresses, and reorder in one tap.</p>
        </div>
      </div>
    </section>
  );
}
