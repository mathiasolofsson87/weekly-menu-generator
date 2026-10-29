import { afterEach, describe, expect, it } from "vitest";
import "../src/index";
import type { WeeklyMenuTodayCard } from "../src/today-card";
import { SPLIT, makeHass, settle, type HassOptions } from "./fixtures";

async function mount(options: HassOptions = {}, config: Record<string, unknown> = {}) {
  const hass = makeHass({ today: { title: "Tacos" }, ...options });
  const card = document.createElement("weeklymenu-today-card") as WeeklyMenuTodayCard;
  card.setConfig({ type: "custom:weeklymenu-today-card", ...config });
  card.hass = hass;
  document.body.append(card);
  await settle(card);
  return { card, hass };
}
const $ = (card: Element, selector: string) => card.shadowRoot!.querySelector<HTMLElement>(selector);
const header = (card: Element) => (card.shadowRoot!.querySelector("ha-card") as unknown as { header: string }).header;
const text = (card: Element) => card.shadowRoot!.textContent!.replace(/\s+/g, " ").trim();

afterEach(() => {
  document.body.innerHTML = "";
});

describe("today card", () => {
  it("shows tonight's dinner with its details", async () => {
    const { card } = await mount();
    expect(header(card)).toBe("Tonight's dinner");
    expect($(card, ".title")!.textContent!.trim()).toBe("Tacos");
    expect(($(card, ".title a") as HTMLAnchorElement).href).toContain("ica.se");
    expect($(card, ".meta")!.textContent).toContain("45 min");
  });

  it("is in Swedish for a Swedish user, with a custom title if asked", async () => {
    expect(header((await mount({ language: "sv" })).card)).toBe("Kvällens middag");
    expect(header((await mount({}, { title: "Middag" })).card)).toBe("Middag");
  });

  it("says so when nothing is planned", async () => {
    const { card } = await mount({ today: null });
    expect(text(card)).toContain("No dinner is planned for today.");
    expect($(card, ".title")).toBeNull();
  });

  it("shows the picture, and hides it on request", async () => {
    const attrs = { image: "https://example.com/t.jpg" };
    expect($((await mount({ today: { title: "Tacos", attrs } })).card, "img")).not.toBeNull();
    expect($((await mount({ today: { title: "Tacos", attrs } }, { show_image: false })).card, "img")).toBeNull();
  });

  it("lists the ingredients only when asked", async () => {
    expect(text((await mount()).card)).not.toContain("400 g pasta");
    expect(text((await mount({}, { show_ingredients: true })).card)).toContain("400 g pasta");
  });

  it("tells who gets a different version", async () => {
    const { card } = await mount({ today: { title: "Biff", attrs: { split: SPLIT } } });
    const note = text(card);
    expect(note).toContain("Anna (50 %): 600 g entrecote → 600 g tofu");
    expect(note).toContain("Use a clean pan and utensils.");
  });

  it("has no buttons: it only shows", async () => {
    const { card } = await mount();
    expect(card.shadowRoot!.querySelectorAll("button")).toHaveLength(0);
    expect(card.getCardSize()).toBe(3);
  });
});
