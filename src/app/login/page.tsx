'use client';

import { useState } from 'react';
import { api } from '@/lib/api';
import { loginSchema } from '@/lib/validators';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  async function login() {
    try {
      setError(null);
      loginSchema.parse({ email, password });
      const res = await api<{ access_token: string }>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      });
      localStorage.setItem('lws_token', res.access_token);
      document.cookie = `lws_token=${res.access_token}; Path=/; Max-Age=86400; SameSite=Lax`;
      window.location.href = '/dashboard';
    } catch (e) {
      setError((e as Error).message || 'Invalid credentials');
    }
  }

  return (
    <section className="mx-auto max-w-xl px-4 py-16">
      <h1 className="font-heading text-6xl">Login</h1>
      <div className="mt-8 space-y-4 rounded-2xl border border-slate-700 bg-[#111827] p-6">
        <input
          className="w-full rounded-xl border border-slate-700 bg-[#0b1220] px-3 py-2"
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="w-full rounded-xl border border-slate-700 bg-[#0b1220] px-3 py-2"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error ? <p className="text-sm text-red-400">{error}</p> : null}
        <button onClick={login} className="w-full rounded-full bg-[#b91c1c] px-6 py-3 font-semibold hover:bg-[#991b1b]">
          Sign In
        </button>
      </div>
    </section>
  );
}
