# Little Wok Story Deployment

## Architecture
- Frontend: Next.js 14 (Vercel)
- Backend: FastAPI (Railway or Render)
- Database: Neon or Supabase PostgreSQL

## 1. Database (Neon/Supabase)
1. Create a PostgreSQL project.
2. Copy connection URI.
3. Set `DATABASE_URL` in backend env.

## 2. Backend (Railway/Render)
1. Create new web service from `backend/`.
2. Runtime: Python 3.11+
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add env vars from `backend/.env.example`.
6. Run seed once: `python seed.py`

## 3. Frontend (Vercel)
1. Import repository.
2. Set root to `/`.
3. Add env vars from `.env.example`.
4. Set `NEXT_PUBLIC_API_BASE_URL` to deployed backend URL + `/api/v1`.
5. Deploy.

## 4. Payments
- Razorpay: configure `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`
- Stripe: configure `STRIPE_SECRET_KEY`, `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`
- Verify callbacks via `/api/v1/payments/*/verify/*`

## 5. Production Hardening Checklist
- Use managed Postgres + backups
- Rotate JWT secrets
- Enable HTTPS only and secure cookies
- Restrict CORS to production domain
- Configure SMTP credentials for order confirmations
- Add observability (Sentry, logs, uptime)
