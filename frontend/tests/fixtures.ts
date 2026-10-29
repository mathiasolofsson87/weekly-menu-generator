import { vi } from "vitest";
import type { HassEntity, HomeAssistant } from "../src/types";
import { WEEKDAYS } from "../src/types";

export const MON = "2026-11-02";

export interface DinnerSpec {
  weekday: string;
  date: string;
  title: string;
  attrs?: Record<string, unknown>;
}

/** The attributes a weekday sensor has in the backend. */
export function dinnerAttrs(date: string, extra: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    date,
    recipe_id: `ica:${date}`,
    source: "ica",
    url: `https://www.ica.se/recept/x-${date.slice(-2)}/`,
    image: null,
    total_time: 45,
    servings: 4,
    tags: ["quick", "family_friendly"],
    ingredients: ["400 g pasta", "2 dl grädde"],
    locked: false,
    split: null,
    alternatives: [{ id: `alt:${date}`, title: `Alternativ ${date}` }],
    ...extra,
  };
}

export const SPLIT = {
  groups: [
    {
      members: ["Anna"],
      share: 0.5,
      separate_pans: true,
      substitutions: [
        { original: { raw: "600 g entrecote", name: "entrecote" }, replacement: { raw: "600 g tofu", name: "tofu" } },
      ],
    },
  ],
};

export interface HassOptions {
  status?: "none" | "draft" | "confirmed";
  weekStart?: string;
  warnings?: string[];
  days?: DinnerSpec[];
  today?: { title: string; attrs?: Record<string, unknown> } | null;
  language?: string;
}

/** A Home Assistant object with the integration's entities in it. */
export function makeHass(options: HassOptions = {}): HomeAssistant & { callService: ReturnType<typeof vi.fn> } {
  const states: Record<string, HassEntity> = {};
  const entities: NonNullable<HomeAssistant["entities"]> = {};
  const add = (key: string, state: string, attributes: Record<string, unknown> = {}) => {
    const entity_id = `sensor.weekly_menu_${key}`;
    entities[entity_id] = { entity_id, platform: "weeklymenu", translation_key: key };
    states[entity_id] = { entity_id, state, attributes };
  };
  const status = options.status ?? "draft";
  add("status", status, status === "none" ? {} : { week_start: options.weekStart ?? MON, warnings: options.warnings ?? [] });
  for (const weekday of WEEKDAYS) {
    const spec = options.days?.find((d) => d.weekday === weekday);
    if (spec) add(`weekday_${weekday}`, spec.title, dinnerAttrs(spec.date, spec.attrs));
    else add(`weekday_${weekday}`, "unknown");
  }
  if (options.today) add("today", options.today.title, dinnerAttrs(MON, options.today.attrs));
  else add("today", "unknown");
  // somebody else's entity that must be ignored
  entities["sensor.other"] = { entity_id: "sensor.other", platform: "other", translation_key: "status" };
  states["sensor.other"] = { entity_id: "sensor.other", state: "x", attributes: {} };

  return {
    states,
    entities,
    language: options.language ?? "en",
    callService: vi.fn().mockResolvedValue(undefined),
  };
}

export const WEEK: DinnerSpec[] = [
  { weekday: "mon", date: "2026-11-02", title: "Pasta carbonara" },
  { weekday: "tue", date: "2026-11-03", title: "Chili con carne" },
  { weekday: "wed", date: "2026-11-04", title: "Linsgryta" },
];

/** Wait for Lit to render, and for any pending promise from a click. */
export async function settle(element: { updateComplete: Promise<unknown> }): Promise<void> {
  await element.updateComplete;
  await Promise.resolve();
  await element.updateComplete;
}
