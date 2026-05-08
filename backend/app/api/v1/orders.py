import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin, require_kitchen_or_admin
from app.core.rate_limit import limiter
from app.db.session import get_db
from app.models.models import Address, Coupon, MenuItem, Order, OrderItem, OrderStatusEnum, PaymentStatusEnum, User, PaymentMethodEnum
from app.schemas.schemas import CreateOrderIn, OrderOut
from app.services.email_service import send_order_email

router = APIRouter(prefix='/orders', tags=['orders'])


def _calc_discount(subtotal: float, coupon: Optional[Coupon]) -> float:
    if not coupon:
        return 0
    if coupon.discount_type.value == 'FLAT':
        return min(coupon.value, subtotal)
    return round(subtotal * (coupon.value / 100), 2)


@router.post('', response_model=OrderOut)
@limiter.limit('30/minute')
def create_order(request: Request, payload: CreateOrderIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    address = db.query(Address).filter(Address.id == payload.address_id, Address.user_id == user.id).first()
    if not address:
        raise HTTPException(status_code=404, detail='Address not found')

    menu_ids = [i.menu_id for i in payload.items]
    menu_rows = db.query(MenuItem).filter(MenuItem.id.in_(menu_ids), MenuItem.available.is_(True)).all()
    menu_map = {m.id: m for m in menu_rows}

    if len(menu_map) != len(menu_ids):
        raise HTTPException(status_code=400, detail='Some menu items unavailable')

    subtotal = 0.0
    order_items: list[OrderItem] = []
    for item in payload.items:
        m = menu_map[item.menu_id]
        line = m.price * item.quantity
        subtotal += line
        order_items.append(
            OrderItem(menu_id=m.id, quantity=item.quantity, price=m.price, customization_json=json.dumps(item.customizations))
        )

    coupon = None
    if payload.coupon_code:
        coupon = db.query(Coupon).filter(Coupon.code == payload.coupon_code.upper(), Coupon.active.is_(True)).first()

    discount = _calc_discount(subtotal, coupon)
    delivery_fee = 0 if subtotal >= 499 else 49
    gst = round(subtotal * 0.05, 2)
    total = round(subtotal - discount + delivery_fee + gst, 2)

    method = PaymentMethodEnum(payload.payment_method)
    payment_status = PaymentStatusEnum.pending if method != PaymentMethodEnum.cod else PaymentStatusEnum.cod

    order = Order(
        order_code=f'LWS-{int(datetime.utcnow().timestamp())}',
        user_id=user.id,
        address_id=address.id,
        total_amount=total,
        discount_amount=discount,
        delivery_fee=delivery_fee,
        gst_amount=gst,
        payment_status=payment_status,
        payment_method=method
    )
    db.add(order)
    db.flush()

    for oi in order_items:
        oi.order_id = order.id
        db.add(oi)

    db.commit()
    db.refresh(order)
    send_order_email(user.email, order.order_code)
    return order


@router.get('/me', response_model=list[OrderOut])
def my_orders(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.user_id == user.id).order_by(Order.created_at.desc()).all()


@router.get('/kitchen', response_model=list[OrderOut])
def kitchen_orders(_: object = Depends(require_kitchen_or_admin), db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.order_status.in_([OrderStatusEnum.placed, OrderStatusEnum.preparing])).all()


@router.patch('/{order_id}/status')
def update_order_status(order_id: int, status: str, _: object = Depends(require_admin), db: Session = Depends(get_db)):
    row = db.query(Order).filter(Order.id == order_id).first()
    if not row:
        raise HTTPException(status_code=404, detail='Order not found')
    row.order_status = OrderStatusEnum(status)
    db.commit()
    return {'ok': True}
