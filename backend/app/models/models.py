import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class RoleEnum(str, enum.Enum):
    user = 'user'
    admin = 'admin'
    kitchen = 'kitchen'


class VegTypeEnum(str, enum.Enum):
    veg = 'VEG'
    non_veg = 'NON_VEG'


class DiscountTypeEnum(str, enum.Enum):
    flat = 'FLAT'
    percent = 'PERCENT'


class PaymentStatusEnum(str, enum.Enum):
    pending = 'PENDING'
    paid = 'PAID'
    failed = 'FAILED'
    cod = 'COD'


class OrderStatusEnum(str, enum.Enum):
    placed = 'PLACED'
    preparing = 'PREPARING'
    out_for_delivery = 'OUT_FOR_DELIVERY'
    delivered = 'DELIVERED'
    cancelled = 'CANCELLED'


class PaymentMethodEnum(str, enum.Enum):
    razorpay = 'RAZORPAY'
    stripe = 'STRIPE'
    cod = 'COD'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.user, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    addresses = relationship('Address', back_populates='user', cascade='all,delete-orphan')
    orders = relationship('Order', back_populates='user')


class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    street: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(120), nullable=False)
    pincode: Mapped[str] = mapped_column(String(20), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)

    user = relationship('User', back_populates='addresses')


class MenuItem(Base):
    __tablename__ = 'menu'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    veg_type: Mapped[VegTypeEnum] = mapped_column(Enum(VegTypeEnum), nullable=False)
    spice_level: Mapped[int] = mapped_column(Integer, default=1)
    available: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Coupon(Base):
    __tablename__ = 'coupons'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    discount_type: Mapped[DiscountTypeEnum] = mapped_column(Enum(DiscountTypeEnum), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    expiry: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_code: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    address_id: Mapped[int] = mapped_column(ForeignKey('addresses.id'), index=True)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    discount_amount: Mapped[float] = mapped_column(Float, default=0)
    delivery_fee: Mapped[float] = mapped_column(Float, default=0)
    gst_amount: Mapped[float] = mapped_column(Float, default=0)
    payment_status: Mapped[PaymentStatusEnum] = mapped_column(Enum(PaymentStatusEnum), default=PaymentStatusEnum.pending)
    order_status: Mapped[OrderStatusEnum] = mapped_column(Enum(OrderStatusEnum), default=OrderStatusEnum.placed)
    payment_method: Mapped[PaymentMethodEnum] = mapped_column(Enum(PaymentMethodEnum), default=PaymentMethodEnum.cod)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='orders')
    items = relationship('OrderItem', back_populates='order', cascade='all,delete-orphan')


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'), index=True)
    menu_id: Mapped[int] = mapped_column(ForeignKey('menu.id'), index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    customization_json: Mapped[str] = mapped_column(Text, default='[]')

    order = relationship('Order', back_populates='items')
