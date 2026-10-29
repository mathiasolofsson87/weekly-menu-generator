import { describe, expect, it } from "vitest";
import { readFamily, readShopping } from "../src/data";
import { FAMILY, SHOPPING, makeHass } from "./fixtures";

describe("readShopping", () => {
  it("reads the counts, the lists, the targets and the errors", () => {
    const shop = readShopping(makeHass({ shopping: { state: "3", attrs: SHOPPING } }));
    expect(shop.hasResult).toBe(true);
    expect(shop.counts).toEqual({ added: 3, review: 1, failed: 2, skipped: 2, pending: 0 });
    expect(shop.added).toHaveLength(3);
    expect(shop.review).toEqual(["1 kg okänd vara"]);
    expect(shop.targets).toEqual(["todo.groceries", "ICA: Veckomeny vecka 45"]);
    expect(shop.errors).toEqual(["ica: auth_failed", "reauth_required"]);
    expect(shop.weekStart).toBe("2026-11-02");
  });

  it("has no result before anything was bought", () => {
    const shop = readShopping(makeHass());
    expect(shop.hasResult).toBe(false);
    expect(shop.counts).toEqual({ added: 0, review: 0, failed: 0, skipped: 0, pending: 0 });
    expect(shop.added).toEqual([]);
  });

  it("survives malformed attributes", () => {
    const shop = readShopping(makeHass({ shopping: { state: "1", attrs: { counts: "x", added: [1, "ok"], errors: null } } }));
    expect(shop.counts.added).toBe(0);
    expect(shop.added).toEqual(["ok"]);
    expect(shop.errors).toEqual([]);
  });
});

describe("readFamily", () => {
  it("reads the members", () => {
    const family = readFamily(makeHass({ family: { members: FAMILY } }));
    expect(family.available).toBe(true);
    expect(family.dinnerDays).toEqual(["mon", "tue", "wed", "thu", "fri"]);
    expect(family.members[0]).toEqual({
      id: "1",
      name: "Anna",
      person: undefined,
      allergies: ["milk", "kiwi"],
      dislikes: ["svamp"],
      likes: [],
      diet: "vegetarian",
      portion: "small",
      attends: ["mon", "tue", "wed", "thu", "fri"],
      cookSeparately: false,
    });
    expect(family.members[1].cookSeparately).toBe(true);
  });

  it("is unavailable while the entry reloads", () => {
    expect(readFamily(makeHass()).available).toBe(false);
  });

  it("fills in defaults and skips entries without an id or a name", () => {
    const family = readFamily(makeHass({ family: { members: [{ id: "9", name: "Kim" }, { id: "", name: "x" }, { id: "8", name: "" }] } }));
    expect(family.members).toHaveLength(1);
    expect(family.members[0]).toMatchObject({ diet: "omnivore", portion: "normal", attends: [], cookSeparately: true });
  });
});
