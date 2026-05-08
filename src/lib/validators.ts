import { z } from 'zod';

export const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(6).max(64)
});

export const addressSchema = z.object({
  street: z.string().min(3),
  city: z.string().min(2),
  pincode: z.string().min(4),
  phone: z.string().min(8)
});
