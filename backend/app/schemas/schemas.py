from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field


class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)


class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class AddressIn(BaseModel):
    street: str
    city: str
    pincode: str
    phone: str


class AddressOut(AddressIn):
    id: int

    class Config:
        from_attributes = True


class MenuIn(BaseModel):
    name: str
    description: str
    price: float
    category: str
    image_url: str
    veg_type: Literal['VEG', 'NON_VEG']
    spice_level: int = Field(ge=1, le=5)
    available: bool = True


class MenuOut(MenuIn):
    id: int

    class Config:
        from_attributes = True


class CouponIn(BaseModel):
    code: str
    discount_type: Literal['FLAT', 'PERCENT']
    value: float
    expiry: datetime


class CouponOut(CouponIn):
    id: int
    active: bool

    class Config:
        from_attributes = True


class OrderItemIn(BaseModel):
    menu_id: int
    quantity: int = Field(gt=0)
    customizations: list[dict] = []


class CreateOrderIn(BaseModel):
    address_id: int
    items: List[OrderItemIn]
    coupon_code: Optional[str] = None
    payment_method: Literal['RAZORPAY', 'STRIPE', 'COD']


class OrderItemOut(BaseModel):
    id: int
    menu_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    order_code: str
    total_amount: float
    payment_status: str
    order_status: str
    payment_method: str
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True
