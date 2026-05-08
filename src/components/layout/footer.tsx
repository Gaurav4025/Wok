import Link from 'next/link';

export function Footer() {
  return (
    <footer className="mt-20 border-t border-slate-800 bg-[#111827]">
      <div className="mx-auto grid max-w-7xl gap-10 px-4 py-14 sm:grid-cols-2 lg:grid-cols-4 sm:px-6 lg:px-8">
        <div>
          <h3 className="font-heading text-4xl text-[#f59e0b]">Little Wok Story</h3>
          <p className="mt-4 text-slate-300">
            Every bowl tells a tale of fire, flavor, and finesse. Cloud kitchen delivery crafted to order.
          </p>
        </div>
        <div>
          <h4 className="font-heading text-2xl">Quick Links</h4>
          <ul className="mt-4 space-y-2 text-slate-300">
            <li>
              <Link href="/menu">Menu</Link>
            </li>
            <li>
              <Link href="/dashboard">My Orders</Link>
            </li>
            <li>
              <Link href="/admin">Admin</Link>
            </li>
          </ul>
        </div>
        <div>
          <h4 className="font-heading text-2xl">Contact</h4>
          <p className="mt-4 text-slate-300">+91 96742 74487</p>
          <p className="text-slate-300">hello@littlewokstory.com</p>
          <p className="text-slate-300">Kolkata, India</p>
        </div>
        <div>
          <h4 className="font-heading text-2xl">Legal</h4>
          <ul className="mt-4 space-y-2 text-slate-300">
            <li>
              <Link href="/privacy-policy">Privacy Policy</Link>
            </li>
            <li>
              <Link href="/terms">Terms</Link>
            </li>
          </ul>
        </div>
      </div>
    </footer>
  );
}
