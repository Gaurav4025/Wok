from fastapi import APIRouter

from app.api.v1 import auth, menu, addresses, coupons, orders, payments, admin

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(menu.router)
api_router.include_router(addresses.router)
api_router.include_router(coupons.router)
api_router.include_router(orders.router)
api_router.include_router(payments.router)
api_router.include_router(admin.router)
