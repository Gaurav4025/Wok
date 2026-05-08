from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.models import MenuItem, Order, OrderItem, User, PaymentStatusEnum

router = APIRouter(prefix='/admin', tags=['admin'])


@router.get('/stats')
def stats(_: object = Depends(require_admin), db: Session = Depends(get_db)):
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)

    revenue = db.query(func.coalesce(func.sum(Order.total_amount), 0)).filter(Order.payment_status.in_([PaymentStatusEnum.paid, PaymentStatusEnum.cod])).scalar()
    orders_today = db.query(func.count(Order.id)).filter(Order.created_at >= today, Order.created_at < tomorrow).scalar()

    best = (
        db.query(MenuItem.name, func.sum(OrderItem.quantity).label('qty'))
        .join(OrderItem, MenuItem.id == OrderItem.menu_id)
        .group_by(MenuItem.name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
        .all()
    )

    return {
        'total_revenue': float(revenue or 0),
        'orders_today': int(orders_today or 0),
        'best_sellers': [{'name': row[0], 'qty': int(row[1])} for row in best]
    }


@router.get('/users')
def users(_: object = Depends(require_admin), db: Session = Depends(get_db)):
    rows = db.query(User).order_by(User.created_at.desc()).limit(200).all()
    return [{'id': u.id, 'name': u.name, 'email': u.email, 'role': u.role.value, 'created_at': u.created_at} for u in rows]
