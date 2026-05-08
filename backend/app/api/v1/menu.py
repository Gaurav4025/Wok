from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import Optional

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.models import MenuItem
from app.schemas.schemas import MenuIn, MenuOut

router = APIRouter(prefix='/menu', tags=['menu'])


@router.get('', response_model=list[MenuOut])
def list_menu(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None)
):
    query = db.query(MenuItem).filter(MenuItem.available.is_(True))

    if q:
        search = f'%{q.lower()}%'
        query = query.filter(or_(MenuItem.name.ilike(search), MenuItem.description.ilike(search)))

    if category:
        query = query.filter(MenuItem.category == category)

    return query.order_by(MenuItem.created_at.desc()).all()


@router.post('', response_model=MenuOut)
def create_menu(payload: MenuIn, _: object = Depends(require_admin), db: Session = Depends(get_db)):
    row = MenuItem(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.put('/{menu_id}', response_model=MenuOut)
def update_menu(menu_id: int, payload: MenuIn, _: object = Depends(require_admin), db: Session = Depends(get_db)):
    row = db.query(MenuItem).filter(MenuItem.id == menu_id).first()
    if not row:
        raise HTTPException(status_code=404, detail='Menu item not found')
    for k, v in payload.model_dump().items():
        setattr(row, k, v)
    db.commit()
    db.refresh(row)
    return row


@router.delete('/{menu_id}')
def delete_menu(menu_id: int, _: object = Depends(require_admin), db: Session = Depends(get_db)):
    row = db.query(MenuItem).filter(MenuItem.id == menu_id).first()
    if not row:
        return {'ok': True}
    db.delete(row)
    db.commit()
    return {'ok': True}
