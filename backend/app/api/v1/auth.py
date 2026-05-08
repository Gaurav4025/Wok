from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.rate_limit import limiter
from app.db.session import get_db
from app.models.models import User, RoleEnum
from app.schemas.schemas import LoginIn, RegisterIn, TokenOut
from app.utils.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=TokenOut)
@limiter.limit('10/minute')
def register(request: Request, payload: RegisterIn, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing:
        raise HTTPException(status_code=409, detail='Email already exists')

    user = User(
        name=payload.name,
        email=payload.email.lower(),
        password=hash_password(payload.password),
        role=RoleEnum.user
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(str(user.id), user.role.value)
    return TokenOut(access_token=token)


@router.post('/login', response_model=TokenOut)
@limiter.limit('20/minute')
def login(request: Request, payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail='Invalid credentials')

    token = create_access_token(str(user.id), user.role.value)
    return TokenOut(access_token=token)


@router.get('/me')
def me(user: User = Depends(get_current_user)):
    return {'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role.value}
