# Little Wok Story

Full-stack food ordering platform for a cloud kitchen (delivery + takeaway).

## Tech Stack
- Frontend: Next.js 14, TypeScript, Tailwind CSS, Framer Motion, Zustand
- Backend: Python FastAPI, SQLAlchemy, PostgreSQL, JWT auth
- Payments: Razorpay + Stripe fallback
- DB contract mirror: Prisma schema included at `prisma/schema.prisma`

## Run Locally

### Frontend
```bash
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python seed.py
uvicorn app.main:app --reload --port 8000
```

## Folder Structure
```text
.
├── backend
│   ├── app
│   │   ├── api/v1
│   │   ├── core
│   │   ├── db
│   │   ├── middleware
│   │   ├── models
│   │   ├── schemas
│   │   ├── services
│   │   └── utils
│   ├── requirements.txt
│   └── seed.py
├── prisma
│   ├── schema.prisma
│   └── seed.ts
├── src
│   ├── app
│   ├── components
│   ├── lib
│   └── store
└── docs
    ├── API.md
    └── DEPLOYMENT.md
```

## Default Seed Accounts
- `admin@littlewokstory.com` / `Admin@123`
- `kitchen@littlewokstory.com` / `Kitchen@123`

## Brand Tagline
Wok-tossed Stories, Delivered Hot.
