export default function OrderSuccessPage({ searchParams }: { searchParams: { orderId?: string; method?: string } }) {
  return (
    <section className="mx-auto max-w-3xl px-4 py-20 text-center">
      <h1 className="font-heading text-6xl text-[#f59e0b]">Order Confirmed</h1>
      <p className="mt-6 text-xl text-slate-300">Your story is on the wok.</p>
      <p className="mt-4 text-lg">Order ID: <span className="font-semibold">{searchParams.orderId || 'N/A'}</span></p>
      <p className="text-slate-300">Payment Method: {searchParams.method || 'N/A'}</p>
    </section>
  );
}
