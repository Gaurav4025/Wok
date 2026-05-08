from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import Address, User
from app.schemas.schemas import AddressIn, AddressOut

router = APIRouter(prefix='/addresses', tags=['addresses'])


@router.get('', response_model=list[AddressOut])
def list_addresses(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Address).filter(Address.user_id == user.id).all()


@router.post('', response_model=AddressOut)
def create_address(payload: AddressIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = Address(user_id=user.id, **payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
