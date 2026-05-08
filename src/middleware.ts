import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get('lws_token')?.value;

  const protectedPaths = ['/admin', '/dashboard', '/checkout', '/kitchen'];
  const needsAuth = protectedPaths.some((p) => pathname === p || pathname.startsWith(`${p}/`));

  if (needsAuth && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/admin/:path*', '/dashboard/:path*', '/checkout/:path*', '/kitchen/:path*']
};
