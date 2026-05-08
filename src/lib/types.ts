export type VegType = 'VEG' | 'NON_VEG';
export type MenuCategory =
  | 'WOK_BOWLS'
  | 'NOODLES'
  | 'FRIED_RICE'
  | 'DIMSUMS'
  | 'STARTERS'
  | 'SAUCES_ADDONS'
  | 'COMBOS';

export interface CustomizationOption {
  key: string;
  label: string;
  price: number;
}

export interface MenuItem {
  id: string;
  name: string;
  description: string;
  price: number;
  category: MenuCategory;
  imageUrl: string;
  vegType: VegType;
  spiceLevel: number;
  available: boolean;
  customizations: CustomizationOption[];
}

export interface CartItem {
  menuId: string;
  name: string;
  imageUrl: string;
  unitPrice: number;
  quantity: number;
  selectedCustomizations: CustomizationOption[];
}

export interface Address {
  id: string;
  street: string;
  city: string;
  pincode: string;
  phone: string;
}
