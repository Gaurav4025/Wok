from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.models import Coupon
from app.schemas.schemas import CouponIn, CouponOut

router = APIRouter(prefix='/coupons', tags=['coupons'])


@router.post('', response_model=CouponOut)
def create_coupon(payload: CouponIn, _: object = Depends(require_admin), db: Session = Depends(get_db)):
    row = Coupon(**payload.model_dump(), code=payload.code.upper())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get('/validate/{code}')
def validate_coupon(code: str, db: Session = Depends(get_db)):
    row = db.query(Coupon).filter(Coupon.code == code.upper(), Coupon.active.is_(True)).first()
    if not row or row.expiry < datetime.utcnow():
        raise HTTPException(status_code=404, detail='Invalid/expired coupon')
    return {'code': row.code, 'discount_type': row.discount_type.value, 'value': row.value}
