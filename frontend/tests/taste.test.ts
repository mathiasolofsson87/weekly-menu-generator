import { afterEach, describe, expect, it } from "vitest";
import "../src/index";
import type { WeeklyMenuTaste } from "../src/taste";
import { readToday } from "../src/data";
import { FAMILY, dinnerAttrs, makeHass, settle, type HassOptions } from "./fixtures";

const PEOPLE = [
  { id: "person.anna", name: "Anna", user_id: "u-anna" },
  { id: "person.olle", name: "Olle", user_id: "u-olle" },
];
const MEMBERS = [
  { ...FAMILY[0], person: "person.anna" },
  { ...FAMILY[1], person: "person.olle" },
];

async function mount(extra: Record<string, unknown> = {}, options: HassOptions = {}) {
  const hass = makeHass({
    family: { members: MEMBERS },
    persons: PEOPLE,
    today: { title: "Gryta", attrs: { recipe_id: "r1", ...extra } },
    ...options,
  });
  const el = document.createElement("weeklymenu-taste") as WeeklyMenuTaste;
  el.hass = hass;
  el.dinner = readToday(hass);
  document.body.append(el);
  await settle(el);
  return { el, hass };
}
const $$ = (el: Element, selector: string) => [...el.shadowRoot!.querySelectorAll<HTMLElement>(selector)];
const stars = (el: Element) => $$(el, ".stars button") as HTMLButtonElement[];

afterEach(() => {
  document.body.innerHTML = "";
});

describe("the rating bar", () => {
  it("shows five stars and a heart, with the current rating filled", async () => {
    const { el } = await mount({ ratings: { "1": 4 } });
    expect(stars(el)).toHaveLength(5);
    expect(stars(el).map((b) => b.getAttribute("aria-pressed"))).toEqual(["false", "false", "false", "true", "false"]);
    expect(stars(el).map((b) => b.classList.contains("on"))).toEqual([true, true, true, true, false]);
    expect(stars(el)[0].getAttribute("aria-label")).toBe("1 star");
    expect(stars(el)[2].getAttribute("aria-label")).toBe("3 stars");
  });

  it("rates for the selected member through rate_recipe", async () => {
    const { el, hass } = await mount();
    stars(el)[3].click();
    await settle(el);
    expect(hass.callService).toHaveBeenCalledWith("weeklymenu", "rate_recipe", { member: "1", recipe_id: "r1", rating: 4 });
  });

  it("takes a rating back when the same star is pressed again", async () => {
    const { el, hass } = await mount({ ratings: { "1": 4 } });
    stars(el)[3].click();
    await settle(el);
    expect(hass.callService).toHaveBeenCalledWith("weeklymenu", "rate_recipe", { member: "1", recipe_id: "r1", rating: 0 });
  });

  it("adds and removes a favorite", async () => {
    const { el, hass } = await mount();
    ($$(el, "button.heart")[0] as HTMLButtonElement).click();
    await settle(el);
    expect(hass.callService).toHaveBeenCalledWith("weeklymenu", "favorite_recipe", { member: "1", recipe_id: "r1", favorite: true });

    document.body.innerHTML = "";
    const again = await mount({ favorite_of: ["1"] });
    const heart = $$(again.el, "button.heart")[0] as HTMLButtonElement;
    expect(heart.getAttribute("aria-pressed")).toBe("true");
    heart.click();
    await settle(again.el);
    expect(again.hass.callService).toHaveBeenCalledWith("weeklymenu", "favorite_recipe", { member: "1", recipe_id: "r1", favorite: false });
  });

  it("acts as the member linked to the logged-in user", async () => {
    const { el, hass } = await mount({}, { userId: "u-olle" });
    stars(el)[1].click();
    await settle(el);
    expect(hass.callService).toHaveBeenCalledWith("weeklymenu", "rate_recipe", { member: "2", recipe_id: "r1", rating: 2 });
    expect(($$(el, "select")[0] as HTMLSelectElement).value).toBe("2");
  });

  it("lets someone rate for another member, such as a child", async () => {
    const { el, hass } = await mount({}, { userId: "u-anna" });
    const select = $$(el, "select")[0] as HTMLSelectElement;
    select.value = "2";
    select.dispatchEvent(new Event("change"));
    await settle(el);
    stars(el)[4].click();
    await settle(el);
    expect(hass.callService).toHaveBeenCalledWith("weeklymenu", "rate_recipe", { member: "2", recipe_id: "r1", rating: 5 });
  });

  it("shows each member's own rating when switching member", async () => {
    const { el } = await mount({ ratings: { "1": 5, "2": 2 } });
    expect(stars(el).filter((b) => b.classList.contains("on"))).toHaveLength(5);
    const select = $$(el, "select")[0] as HTMLSelectElement;
    select.value = "2";
    select.dispatchEvent(new Event("change"));
    await settle(el);
    expect(stars(el).filter((b) => b.classList.contains("on"))).toHaveLength(2);
  });

  it("says whose favorite the recipe is", async () => {
    const { el } = await mount({ favorite_of: ["1", "2"] });
    expect(el.shadowRoot!.querySelector(".liked")!.textContent).toBe("Favorite of Anna, Olle");
  });

  it("has no member menu for a family of one, and nothing without a family or a recipe", async () => {
    const one = await mount({}, { family: { members: [MEMBERS[0]] } });
    expect($$(one.el, "select")).toHaveLength(0);
    document.body.innerHTML = "";
    const none = await mount({}, { family: { members: [] } });
    expect(none.el.shadowRoot!.querySelector(".taste")).toBeNull();
  });

  it("shows the error when the service fails", async () => {
    const { el, hass } = await mount();
    hass.callService.mockRejectedValueOnce(new Error("There is no family member x."));
    stars(el)[0].click();
    await settle(el);
    expect(el.shadowRoot!.textContent).toContain("There is no family member x.");
  });

  it("speaks Swedish", async () => {
    const { el } = await mount({ ratings: {} }, { language: "sv" });
    expect(stars(el)[2].getAttribute("aria-label")).toBe("3 stjärnor");
    expect(($$(el, "select")[0] as HTMLSelectElement).getAttribute("aria-label")).toBe("Betyg som");
  });
});

describe("in the cards", () => {
  it("is on the today card", async () => {
    const { TodayHost } = { TodayHost: "weeklymenu-today-card" };
    const hass = makeHass({ family: { members: MEMBERS }, today: { title: "Gryta", attrs: { recipe_id: "r1" } } });
    const card = document.createElement(TodayHost) as HTMLElement & { hass: unknown; setConfig: (c: unknown) => void };
    card.setConfig({ type: "custom:weeklymenu-today-card" });
    card.hass = hass;
    document.body.append(card);
    await settle(card as never);
    expect(card.shadowRoot!.querySelector("weeklymenu-taste")).not.toBeNull();
  });

  it("is in an opened day of the menu card, also after the menu is confirmed", async () => {
    const hass = makeHass({
      family: { members: MEMBERS },
      status: "confirmed",
      days: [{ weekday: "mon", date: "2026-11-02", title: "Gryta", attrs: dinnerAttrs("2026-11-02") }],
    } as HassOptions);
    const card = document.createElement("weeklymenu-menu-card") as HTMLElement & { hass: unknown; setConfig: (c: unknown) => void };
    card.setConfig({ type: "custom:weeklymenu-menu-card" });
    card.hass = hass;
    document.body.append(card);
    await settle(card as never);
    (card.shadowRoot!.querySelector("button[aria-expanded]") as HTMLButtonElement).click();
    await settle(card as never);
    expect(card.shadowRoot!.querySelector("weeklymenu-taste")).not.toBeNull();
  });
});

describe("a child's view", () => {
  const FAMILY_WITH_CHILD = [
    { ...FAMILY[0], person: "person.anna" },
    { ...FAMILY[1], person: "person.olle", child: true, favorites: [{ id: "r1", title: "Gryta" }] },
  ];
  const WITH_FAVORITES_FOR_ANNA = [{ ...FAMILY_WITH_CHILD[0], favorites: [{ id: "r9", title: "Soppa" }] }, FAMILY_WITH_CHILD[1]];

  async function menuCard(userId: string) {
    const hass = makeHass({
      family: { members: FAMILY_WITH_CHILD },
      persons: PEOPLE,
      userId,
      days: [{ weekday: "mon", date: "2026-11-02", title: "Gryta", attrs: dinnerAttrs("2026-11-02") }],
    } as HassOptions);
    const card = document.createElement("weeklymenu-menu-card") as HTMLElement & { hass: unknown; setConfig: (c: unknown) => void };
    card.setConfig({ type: "custom:weeklymenu-menu-card" });
    card.hass = hass;
    document.body.append(card);
    await settle(card as never);
    (card.shadowRoot!.querySelector("button[aria-expanded]") as HTMLButtonElement).click();
    await settle(card as never);
    return card;
  }
  const labels = (card: Element) => $$(card, "button").map((b) => b.getAttribute("aria-label") ?? b.textContent!.trim());

  it("has no buttons to change the menu, but can still rate", async () => {
    const card = await menuCard("u-olle");
    expect(labels(card)).not.toContain("Lock");
    expect(labels(card)).not.toContain("New dinner");
    expect(labels(card)).not.toContain("Confirm menu");
    expect(card.shadowRoot!.querySelector("weeklymenu-taste")).not.toBeNull();
    expect(card.shadowRoot!.querySelector("input[type=text]")).toBeNull(); // no wish field
  });

  it("is unchanged for an adult", async () => {
    const card = await menuCard("u-anna");
    expect(labels(card)).toContain("Lock");
    expect(labels(card)).toContain("New dinner");
  });

  async function familyCard(userId: string, members = FAMILY_WITH_CHILD) {
    const hass = makeHass({ family: { members }, persons: PEOPLE, userId });
    const card = document.createElement("weeklymenu-family-card") as HTMLElement & { hass: unknown; setConfig: (c: unknown) => void };
    card.setConfig({ type: "custom:weeklymenu-family-card" });
    card.hass = hass;
    document.body.append(card);
    await settle(card as never);
    return { card, hass };
  }

  it("cannot edit or add people in the family card, but can take their own favorites off", async () => {
    const { card, hass } = await familyCard("u-olle", WITH_FAVORITES_FOR_ANNA);
    expect(labels(card)).not.toContain("Edit");
    expect(labels(card)).not.toContain("Add person");
    const own = $$(card, ".member")[1];
    (own.querySelector(".fav button") as HTMLButtonElement).click();
    await settle(card as never);
    expect(hass.callService).toHaveBeenCalledWith("weeklymenu", "favorite_recipe", { member: "2", recipe_id: "r1", favorite: false });
    // somebody else's favorites cannot be removed
    expect($$(card, ".member")[0].querySelector(".fav button")).toBeNull();
  });

  it("can edit the family as an adult", async () => {
    const { card } = await familyCard("u-anna");
    expect(labels(card)).toContain("Edit");
    expect(labels(card)).toContain("Add person");
  });
});
