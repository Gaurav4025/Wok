import hashlib
import hmac

import razorpay
import stripe
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.models.models import Order, PaymentStatusEnum, User

router = APIRouter(prefix='/payments', tags=['payments'])


@router.post('/razorpay/create/{order_id}')
def create_razorpay_order(order_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')

    if not settings.razorpay_key_id or not settings.razorpay_key_secret:
        return {'provider': 'razorpay', 'mock': True, 'order_id': f'mock_rzp_{order.id}', 'amount': int(order.total_amount * 100)}

    client = razorpay.Client(auth=(settings.razorpay_key_id, settings.razorpay_key_secret))
    rzp_order = client.order.create({'amount': int(order.total_amount * 100), 'currency': 'INR', 'receipt': order.order_code})
    return {'provider': 'razorpay', 'order': rzp_order, 'key_id': settings.razorpay_key_id}


@router.post('/razorpay/verify/{order_id}')
def verify_razorpay_payment(order_id: int, razorpay_order_id: str, razorpay_payment_id: str, razorpay_signature: str, db: Session = Depends(get_db)):
    payload = f'{razorpay_order_id}|{razorpay_payment_id}'.encode('utf-8')
    generated = hmac.new(settings.razorpay_key_secret.encode('utf-8'), payload, hashlib.sha256).hexdigest()
    if generated != razorpay_signature:
        raise HTTPException(status_code=400, detail='Invalid signature')

    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        order.payment_status = PaymentStatusEnum.paid
        db.commit()
    return {'verified': True}


@router.post('/stripe/create/{order_id}')
def create_stripe_session(order_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')

    if not settings.stripe_secret_key:
        return {'provider': 'stripe', 'mock': True, 'session_id': f'mock_stripe_{order.id}'}

    stripe.api_key = settings.stripe_secret_key
    session = stripe.checkout.Session.create(
        mode='payment',
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'unit_amount': int(order.total_amount * 100),
                'product_data': {'name': f'Little Wok Story Order {order.order_code}'}
            },
            'quantity': 1
        }],
        success_url=f'{settings.frontend_url}/order-success?orderId={order.order_code}&method=STRIPE',
        cancel_url=f'{settings.frontend_url}/checkout'
    )
    return {'provider': 'stripe', 'session_id': session.id, 'url': session.url}


@router.post('/stripe/verify/{order_id}')
def verify_stripe_payment(order_id: int, payment_intent: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')

    if settings.stripe_secret_key:
        stripe.api_key = settings.stripe_secret_key
        intent = stripe.PaymentIntent.retrieve(payment_intent)
        if intent.status != 'succeeded':
            raise HTTPException(status_code=400, detail='Payment not successful')

    order.payment_status = PaymentStatusEnum.paid
    db.commit()
    return {'verified': True}
