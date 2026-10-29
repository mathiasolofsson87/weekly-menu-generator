/** The small part of Home Assistant's frontend API the cards use. */

export interface HassEntity {
  entity_id: string;
  state: string;
  attributes: Record<string, unknown>;
}

/** The entity registry entry the frontend keeps for every entity (`hass.entities`). */
export interface HassEntityRegistryEntry {
  entity_id: string;
  platform?: string;
  translation_key?: string;
}

export interface HomeAssistant {
  states: Record<string, HassEntity>;
  entities?: Record<string, HassEntityRegistryEntry>;
  language: string;
  locale?: { language: string };
  callService(
    domain: string,
    service: string,
    data?: Record<string, unknown>,
  ): Promise<unknown>;
}

export interface LovelaceCardConfig {
  type: string;
  [key: string]: unknown;
}

/** One substitution inside a split dinner. */
export interface Swap {
  original: string;
  replacement: string;
}

/** Some members eat an adjusted version of the dinner. */
export interface SplitGroup {
  members: string[];
  swaps: Swap[];
  share: number;
  separatePans: boolean;
}

export interface Alternative {
  id: string;
  title: string;
}

/** One planned dinner, as read from a weekday (or today) sensor. */
export interface Dinner {
  entityId: string;
  weekday: string; // mon..sun, "" for the today sensor
  date: string; // ISO date
  title: string;
  recipeId: string;
  url?: string;
  image?: string;
  source?: string;
  totalTime?: number;
  servings?: number;
  tags: string[];
  ingredients: string[];
  locked: boolean;
  alternatives: Alternative[];
  split: SplitGroup[];
}

export interface MenuModel {
  status: "none" | "draft" | "confirmed";
  weekStart?: string;
  warnings: string[];
  days: Dinner[];
}

export const WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"] as const;
export type Weekday = (typeof WEEKDAYS)[number];

/** How the last confirmed menu's shopping went (from the shopping sensor). */
export interface ShoppingModel {
  hasResult: boolean;
  weekStart?: string;
  counts: { added: number; review: number; failed: number; skipped: number; pending: number };
  added: string[];
  review: string[];
  failed: string[];
  pending: string[];
  skipped: string[];
  targets: string[];
  errors: string[];
}

export interface Member {
  id: string;
  name: string;
  person?: string;
  allergies: string[];
  dislikes: string[];
  likes: string[];
  diet: string;
  portion: string;
  attends: string[];
  cookSeparately: boolean;
}

export interface FamilyModel {
  available: boolean;
  members: Member[];
  dinnerDays: string[];
}

export const ALLERGENS = [
  "gluten",
  "milk",
  "lactose",
  "egg",
  "fish",
  "crustaceans",
  "molluscs",
  "peanuts",
  "tree_nuts",
  "soy",
  "sesame",
  "celery",
  "mustard",
  "lupin",
  "sulphites",
] as const;
export const DIETS = ["omnivore", "vegetarian", "vegan", "pescatarian"] as const;
export const PORTIONS = ["small", "normal", "large"] as const;
