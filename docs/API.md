# Key Backend APIs

Base URL: `/api/v1`

## Auth
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

## Menu
- `GET /menu?q=&category=`
- `POST /menu` (admin)
- `PUT /menu/{menu_id}` (admin)
- `DELETE /menu/{menu_id}` (admin)

## Addresses
- `GET /addresses`
- `POST /addresses`

## Coupons
- `POST /coupons` (admin)
- `GET /coupons/validate/{code}`

## Orders
- `POST /orders`
- `GET /orders/me`
- `GET /orders/kitchen` (kitchen/admin)
- `PATCH /orders/{order_id}/status?status=PREPARING` (admin)

## Payments
- `POST /payments/razorpay/create/{order_id}`
- `POST /payments/razorpay/verify/{order_id}`
- `POST /payments/stripe/create/{order_id}`
- `POST /payments/stripe/verify/{order_id}`

## Admin
- `GET /admin/stats`
- `GET /admin/users`
