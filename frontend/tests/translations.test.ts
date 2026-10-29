import { describe, expect, it } from "vitest";
import { STRINGS, shoppingError, tagLabel } from "../src/i18n";
import { ALLERGENS, DIETS, PORTIONS } from "../src/types";

const en = Object.keys(STRINGS.en).sort();
const sv = Object.keys(STRINGS.sv).sort();
const placeholders = (text: string) => [...text.matchAll(/\{(\w+)\}/g)].map((m) => m[1]).sort();

describe("English and Swedish stay in step", () => {
  it("have the same keys", () => {
    expect(sv.filter((k) => !en.includes(k))).toEqual([]);
    expect(en.filter((k) => !sv.includes(k))).toEqual([]);
  });

  it("have no empty text and the same placeholders", () => {
    for (const key of en) {
      const e = STRINGS.en[key as keyof typeof STRINGS.en];
      const s = STRINGS.sv[key as keyof typeof STRINGS.sv];
      expect(e.trim(), key).not.toBe("");
      expect(s.trim(), key).not.toBe("");
      expect(placeholders(s), key).toEqual(placeholders(e));
    }
  });

  it("translate every allergen, diet and portion the backend knows", () => {
    for (const a of ALLERGENS) expect(en).toContain(`allergen_${a}`);
    for (const d of DIETS) expect(en).toContain(`diet_${d}`);
    for (const p of PORTIONS) expect(en).toContain(`portion_${p}`);
    expect(en.filter((k) => k.startsWith("allergen_"))).toHaveLength(ALLERGENS.length);
  });

  it("translate every style tag the backend produces", () => {
    for (const tag of ["quick", "easy", "fancy", "family_friendly", "budget", "vegetarian", "fish"]) {
      expect(tagLabel({ language: "sv" }, tag)).not.toBe(tag.replace(/_/g, " "));
    }
  });
});

describe("shoppingError", () => {
  it("explains the errors the backend reports", () => {
    expect(shoppingError({ language: "en" }, "ica: auth_failed")).toBe(
      "The sign-in to ICA no longer works. Sign in again under Settings.",
    );
    expect(shoppingError({ language: "sv" }, "ica: geo_blocked")).toBe("ICA svarar bara på anslutningar från Sverige.");
    expect(shoppingError({ language: "en" }, "no_targets")).toBe("No shopping list is set up.");
    expect(shoppingError({ language: "en" }, "reauth_required")).toContain("Sign in again");
  });
  it("shows an unknown error as written", () => {
    expect(shoppingError({ language: "en" }, "todo.x: unavailable")).toBe("todo.x: unavailable");
  });
});
