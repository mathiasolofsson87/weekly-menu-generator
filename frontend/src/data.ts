import {
  type Alternative,
  type Dinner,
  type FamilyModel,
  type HomeAssistant,
  type Member,
  type MenuModel,
  type ShoppingModel,
  type SplitGroup,
  WEEKDAYS,
} from "./types";

export const DOMAIN = "weeklymenu";

/** Entities of the integration by their translation key ("status", "today", "weekday_mon"...). */
export function discover(hass: HomeAssistant): Map<string, string> {
  const found = new Map<string, string>();
  for (const entry of Object.values(hass.entities ?? {})) {
    if (entry.platform === DOMAIN && entry.translation_key) {
      found.set(entry.translation_key, entry.entity_id);
    }
  }
  return found;
}

const str = (v: unknown): string | undefined =>
  typeof v === "string" && v !== "" ? v : undefined;
const num = (v: unknown): number | undefined =>
  typeof v === "number" && Number.isFinite(v) ? v : undefined;
const strings = (v: unknown): string[] =>
  Array.isArray(v) ? v.filter((x): x is string => typeof x === "string") : [];

const isObject = (v: unknown): v is Record<string, unknown> => typeof v === "object" && v !== null;

function readSplit(raw: unknown): SplitGroup[] {
  const groups = isObject(raw) && Array.isArray(raw.groups) ? raw.groups : [];
  return groups.filter(isObject).map((group) => {
    const swaps = Array.isArray(group.substitutions) ? group.substitutions : [];
    const text = (ingredient: unknown): string =>
      isObject(ingredient) ? (str(ingredient.raw) ?? str(ingredient.name) ?? "") : "";
    return {
      members: strings(group.members),
      share: num(group.share) ?? 0,
      separatePans: group.separate_pans === true,
      swaps: swaps.filter(isObject).map((swap) => ({
        original: text(swap.original),
        replacement: text(swap.replacement),
      })),
    };
  });
}

function readAlternatives(raw: unknown): Alternative[] {
  if (!Array.isArray(raw)) return [];
  return raw
    .filter(isObject)
    .filter((a) => typeof a.id === "string" && typeof a.title === "string")
    .map((a) => ({ id: a.id as string, title: a.title as string }));
}

/** A dinner from a sensor. Returns undefined when nothing is planned for it. */
export function readDinner(
  hass: HomeAssistant,
  entityId: string | undefined,
  weekday = "",
): Dinner | undefined {
  const state = entityId ? hass.states[entityId] : undefined;
  if (!state || ["unknown", "unavailable", ""].includes(state.state)) return undefined;
  const a = state.attributes;
  const date = str(a.date);
  if (!date) return undefined;
  return {
    entityId: state.entity_id,
    weekday,
    date,
    title: state.state,
    recipeId: str(a.recipe_id) ?? "",
    url: str(a.url),
    image: str(a.image),
    source: str(a.source),
    totalTime: num(a.total_time),
    servings: num(a.servings),
    tags: strings(a.tags),
    ingredients: strings(a.ingredients),
    locked: a.locked === true,
    alternatives: readAlternatives(a.alternatives),
    split: readSplit(a.split),
  };
}

/** The whole menu: the status sensor plus one sensor per planned weekday. */
export function readMenu(hass: HomeAssistant): MenuModel {
  const entities = discover(hass);
  const status = hass.states[entities.get("status") ?? ""];
  const raw = status?.state;
  const attrs = status?.attributes ?? {};
  const days: Dinner[] = [];
  for (const weekday of WEEKDAYS) {
    const dinner = readDinner(hass, entities.get(`weekday_${weekday}`), weekday);
    if (dinner) days.push(dinner);
  }
  return {
    status: raw === "draft" || raw === "confirmed" ? raw : "none",
    weekStart: str(attrs.week_start),
    warnings: strings(attrs.warnings),
    days,
  };
}

export function readToday(hass: HomeAssistant): Dinner | undefined {
  return readDinner(hass, discover(hass).get("today"));
}

/** ISO week number of an ISO date ("2026-11-02" is week 45). */
export function isoWeek(isoDate: string): number {
  const [y, m, d] = isoDate.split("-").map(Number);
  const date = new Date(Date.UTC(y, m - 1, d));
  const day = date.getUTCDay() || 7;
  date.setUTCDate(date.getUTCDate() + 4 - day);
  const yearStart = Date.UTC(date.getUTCFullYear(), 0, 1);
  return Math.ceil(((date.getTime() - yearStart) / 86400000 + 1) / 7);
}

/** Share as a whole-percent label: 0.333333 -> "33 %". */
export function percent(share: number): string {
  return `${Math.round(share * 100)} %`;
}

const EMPTY_COUNTS = { added: 0, review: 0, failed: 0, skipped: 0, pending: 0 };

/** The shopping result of the last confirmed menu. `hasResult` is false before any shopping. */
export function readShopping(hass: HomeAssistant): ShoppingModel {
  const state = hass.states[discover(hass).get("shopping") ?? ""];
  const a = state?.attributes ?? {};
  const counts = isObject(a.counts) ? a.counts : {};
  return {
    hasResult: !!state && !["unknown", "unavailable", ""].includes(state.state),
    weekStart: str(a.week_start),
    counts: {
      added: num(counts.added) ?? 0,
      review: num(counts.review) ?? 0,
      failed: num(counts.failed) ?? 0,
      skipped: num(counts.skipped) ?? 0,
      pending: num(counts.pending) ?? 0,
    },
    added: strings(a.added),
    review: strings(a.review),
    failed: strings(a.failed),
    pending: strings(a.pending),
    skipped: strings(a.skipped),
    targets: strings(a.targets),
    errors: strings(a.errors),
  };
}

export { EMPTY_COUNTS };

/** The family from the family sensor. */
export function readFamily(hass: HomeAssistant): FamilyModel {
  const state = hass.states[discover(hass).get("family") ?? ""];
  if (!state || ["unknown", "unavailable", ""].includes(state.state)) {
    return { available: false, members: [], dinnerDays: [] };
  }
  const raw = Array.isArray(state.attributes.members) ? state.attributes.members : [];
  const members: Member[] = raw.filter(isObject).map((m) => ({
    id: str(m.id) ?? "",
    name: str(m.name) ?? "",
    person: str(m.person),
    allergies: strings(m.allergies),
    dislikes: strings(m.dislikes),
    likes: strings(m.likes),
    diet: str(m.diet) ?? "omnivore",
    portion: str(m.portion) ?? "normal",
    attends: strings(m.attends),
    cookSeparately: m.cook_separately !== false,
  }));
  return {
    available: true,
    members: members.filter((m) => m.id && m.name),
    dinnerDays: strings(state.attributes.dinner_days),
  };
}
