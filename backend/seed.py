from datetime import datetime, timedelta

from app.db.session import SessionLocal, engine, Base
from app.models.models import User, RoleEnum, MenuItem, VegTypeEnum, Coupon, DiscountTypeEnum
from app.utils.security import hash_password

Base.metadata.create_all(bind=engine)

db = SessionLocal()

if not db.query(User).filter(User.email == 'admin@littlewokstory.com').first():
    db.add(User(name='Admin', email='admin@littlewokstory.com', password=hash_password('Admin@123'), role=RoleEnum.admin))

if not db.query(User).filter(User.email == 'kitchen@littlewokstory.com').first():
    db.add(User(name='Kitchen', email='kitchen@littlewokstory.com', password=hash_password('Kitchen@123'), role=RoleEnum.kitchen))

if db.query(MenuItem).count() == 0:
    db.add_all([
        MenuItem(
            name='Szechuan Wok Bowl',
            description='Fiery wok tossed veggies, jasmine rice, chilli garlic glaze.',
            price=249,
            category='WOK_BOWLS',
            image_url='https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=1200&q=80',
            veg_type=VegTypeEnum.veg,
            spice_level=4,
            available=True
        ),
        MenuItem(
            name='Chicken Hakka Noodles',
            description='Street-style chicken noodles with wok smoke and crunch.',
            price=219,
            category='NOODLES',
            image_url='https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?auto=format&fit=crop&w=1200&q=80',
            veg_type=VegTypeEnum.non_veg,
            spice_level=3,
            available=True
        )
    ])

if not db.query(Coupon).filter(Coupon.code == 'WOK20').first():
    db.add(Coupon(code='WOK20', discount_type=DiscountTypeEnum.percent, value=20, expiry=datetime.utcnow() + timedelta(days=30), active=True))


db.commit()
print('Seed complete')
