import type { MenuItem } from './types';

export const categoryLabels: Record<string, string> = {
  WOK_BOWLS: 'Wok Bowls',
  NOODLES: 'Noodles',
  FRIED_RICE: 'Fried Rice',
  DIMSUMS: 'Dimsums',
  STARTERS: 'Starters',
  SAUCES_ADDONS: 'Sauces & Add-ons',
  COMBOS: 'Combos'
};

export const fallbackMenu: MenuItem[] = [
  {
    id: '1',
    name: 'Szechuan Wok Bowl',
    description: 'Fiery vegetables, jasmine rice, wok-seared sauce.',
    price: 249,
    category: 'WOK_BOWLS',
    imageUrl:
      'https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=1200&q=80',
    vegType: 'VEG',
    spiceLevel: 4,
    available: true,
    customizations: [
      { key: 'extra_sauce', label: 'Extra Chilli Garlic Sauce', price: 25 },
      { key: 'add_paneer', label: 'Add Paneer', price: 49 }
    ]
  },
  {
    id: '2',
    name: 'Chicken Hakka Noodles',
    description: 'Classic street-style tossed noodles with chicken strips.',
    price: 219,
    category: 'NOODLES',
    imageUrl:
      'https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?auto=format&fit=crop&w=1200&q=80',
    vegType: 'NON_VEG',
    spiceLevel: 3,
    available: true,
    customizations: [
      { key: 'add_egg', label: 'Add Egg', price: 29 },
      { key: 'extra_protein', label: 'Extra Chicken', price: 69 }
    ]
  }
];
