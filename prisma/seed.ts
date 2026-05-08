import { PrismaClient, Role, VegType, DiscountType } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  const password = await bcrypt.hash('Admin@123', 10);

  await prisma.user.upsert({
    where: { email: 'admin@littlewokstory.com' },
    update: {},
    create: {
      name: 'Admin',
      email: 'admin@littlewokstory.com',
      password,
      role: Role.ADMIN
    }
  });

  await prisma.menu.createMany({
    data: [
      {
        name: 'Szechuan Wok Bowl',
        description: 'Fiery wok-tossed veggies, jasmine rice, chili garlic glaze.',
        price: 249,
        category: 'WOK_BOWLS',
        imageUrl: 'https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=1200&q=80',
        vegType: VegType.VEG,
        spiceLevel: 4,
        available: true
      },
      {
        name: 'Chicken Hakka Noodles',
        description: 'Street-style noodles with wok smoke and crisp vegetables.',
        price: 219,
        category: 'NOODLES',
        imageUrl: 'https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?auto=format&fit=crop&w=1200&q=80',
        vegType: VegType.NON_VEG,
        spiceLevel: 3,
        available: true
      }
    ],
    skipDuplicates: true
  });

  await prisma.coupon.upsert({
    where: { code: 'WOK20' },
    update: {},
    create: {
      code: 'WOK20',
      discountType: DiscountType.PERCENT,
      value: 20,
      expiry: new Date(Date.now() + 1000 * 60 * 60 * 24 * 30),
      active: true
    }
  });
}

main().finally(async () => prisma.$disconnect());
