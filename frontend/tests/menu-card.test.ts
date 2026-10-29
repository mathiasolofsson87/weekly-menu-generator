import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import "../src/index";
import type { WeeklyMenuCard } from "../src/menu-card";
import { SPLIT, WEEK, makeHass, settle, type HassOptions } from "./fixtures";

async function mount(options: HassOptions = {}, config: Record<string, unknown> = {}) {
  const hass = makeHass({ days: WEEK, ...options });
  const card = document.createElement("weeklymenu-menu-card") as WeeklyMenuCard;
  card.setConfig({ type: "custom:weeklymenu-menu-card", ...config });
  card.hass = hass;
  document.body.append(card);
  await settle(card);
  return { card, hass };
}

const $ = (card: Element, selector: string) => card.shadowRoot!.querySelector<HTMLElement>(selector);
const $$ = (card: Element, selector: string) => [...card.shadowRoot!.querySelectorAll<HTMLElement>(selector)];
const text = (card: Element) => card.shadowRoot!.textContent!.replace(/\s+/g, " ").trim();
const button = (card: Element, label: string) =>
  $$(card, "button").find((b) => b.getAttribute("aria-label") === label || b.textContent!.trim() === label)!;

beforeEach(() => {
  vi.spyOn(window, "confirm").mockReturnValue(true);
});
afterEach(() => {
  document.body.innerHTML = "";
  vi.restoreAllMocks();
});

describe("what it shows", () => {
  it("shows the week, the status and one row per planned day", async () => {
    const { card } = await mount();
    expect((card.shadowRoot!.querySelector("ha-card") as unknown as { header: string }).header).toBe("Weekly menu");
    expect(text(card)).toContain("Week 45");
    expect($(card, ".chip")!.className).toContain("draft");
    expect($(card, ".chip")!.textContent).toBe("Draft");
    expect($$(card, ".day").map((d) => d.querySelector(".title")!.textContent!.trim())).toEqual([
      "Pasta carbonara",
      "Chili con carne",
      "Linsgryta",
    ]);
    expect($$(card, ".day .wd").map((e) => e.textContent)).toEqual(["Mon", "Tue", "Wed"]);
  });

  it("uses the configured title and the user's language", async () => {
    const { card } = await mount({ language: "sv" }, { title: "Matplan" });
    expect((card.shadowRoot!.querySelector("ha-card") as unknown as { header: string }).header).toBe("Matplan");
    expect(text(card)).toContain("Vecka 45");
    expect($(card, ".chip")!.textContent).toBe("Utkast");
  });

  it("links to the recipe and shows time, tags and source", async () => {
    const { card } = await mount();
    const link = $(card, ".title a") as HTMLAnchorElement;
    expect(link.href).toBe("https://www.ica.se/recept/x-02/");
    expect(link.rel).toContain("noopener");
    const meta = $(card, ".meta")!.textContent!;
    expect(meta).toContain("45 min");
    expect(meta).toContain("Family friendly");
    expect(meta).toContain("ICA");
  });

  it("shows pictures unless switched off", async () => {
    const attrs = { image: "https://example.com/a.jpg" };
    const days = WEEK.map((d) => ({ ...d, attrs }));
    expect($((await mount({ days })).card, ".main img")).not.toBeNull();
    expect($((await mount({ days }, { show_images: false })).card, ".main img")).toBeNull();
  });

  it("explains backend warnings in plain language, once each", async () => {
    const { card } = await mount({ warnings: ["no_recipe:thu", "no_recipe:thu", "source_failed:ica"] });
    const banners = $$(card, ".banner.warning").map((b) => b.textContent!.trim());
    expect(banners).toEqual(["No recipe was found for Thursday.", "The recipe source ica did not work."]);
  });

  it("has an empty state that offers to generate", async () => {
    const { card, hass } = await mount({ days: [], status: "none" });
    expect(text(card)).toContain("There is no menu yet.");
    expect($(card, ".chip")!.textContent).toBe("No menu");
    button(card, "Generate menu").click();
    await settle(card);
    expect(hass.callService).toHaveBeenCalledWith("weeklymenu", "generate_menu", {});
  });

  it("shows nothing before it has a hass object", async () => {
    const card = document.createElement("weeklymenu-menu-card") as WeeklyMenuCard;
    card.setConfig({ type: "custom:weeklymenu-menu-card" });
    document.body.append(card);
    await card.updateComplete;
    expect(card.shadowRoot!.querySelector("ha-card")).toBeNull();
    expect(card.getCardSize()).toBe(4);
  });

  it("rejects a missing config", () => {
    const card = document.createElement("weeklymenu-menu-card") as WeeklyMenuCard;
    expect(() => card.setConfig(undefined as never)).toThrow("Invalid configuration");
  });
});

describe("details", () => {
  it("expands a day to show ingredients, and collapses again", async () => {
    const { card } = await mount();
    expect($(card, ".more")).toBeNull();
    const toggle = button(card, "Show details");
    expect(toggle.getAttribute("aria-expanded")).toBe("false");
    toggle.click();
    await settle(card);
    expect($(card, ".more")!.textContent).toContain("400 g pasta");
    expect($$(card, ".more li").map((li) => li.textContent)).toEqual(["400 g pasta", "2 dl grädde"]);
    button(card, "Hide details").click();
    await settle(card);
    expect($(card, ".more")).toBeNull();
  });

  it("shows who eats a different version, with the clean-pan reminder", async () => {
    const days = [{ ...WEEK[0], attrs: { split: SPLIT } }];
    const { card } = await mount({ days });
    expect($(card, ".badge.split")).not.toBeNull();
    button(card, "Show details").click();
    await settle(card);
    const note = $(card, ".split-note")!.textContent!.replace(/\s+/g, " ");
    expect(note).toContain("Anna (50 %): 600 g entrecote → 600 g tofu");
    expect(note).toContain("Use a clean pan and utensils.");
  });
});

describe("changing the menu", () => {
  it("locks and unlocks a day", async () => {
    const days = [WEEK[0], { ...WEEK[1], attrs: { locked: true } }];
    const { card, hass } = await mount({ days });
    const [lock, unlock] = $$(card, "button.icon[aria-pressed]");
    expect(lock.getAttribute("aria-pressed")).toBe("false");
    expect(unlock.getAttribute("aria-pressed")).toBe("true");
    lock.click();
    await settle(card);
    unlock.click();
    await settle(card);
    expect(hass.callService).toHaveBeenNthCalledWith(1, "weeklymenu", "lock_day", { date: "2026-11-02", locked: true });
    expect(hass.callService).toHaveBeenNthCalledWith(2, "weeklymenu", "lock_day", { date: "2026-11-03", locked: false });
  });

  it("asks for a new dinner for one day, with or without a wish", async () => {
    const { card, hass } = await mount();
    button(card, "Show details").click();
    await settle(card);
    button(card, "New dinner").click();
    await settle(card);
    const input = $(card, ".more input") as HTMLInputElement;
    input.value = " something with fish ";
    input.dispatchEvent(new Event("input"));
    await settle(card);
    button(card, "New dinner").click();
    await settle(card);
    expect(hass.callService).toHaveBeenNthCalledWith(1, "weeklymenu", "regenerate_day", { date: "2026-11-02" });
    expect(hass.callService).toHaveBeenNthCalledWith(2, "weeklymenu", "regenerate_day", {
      date: "2026-11-02",
      hint: "something with fish",
    });
  });

  it("cannot regenerate a locked day, and offers no swap for it", async () => {
    const { card } = await mount({ days: [{ ...WEEK[0], attrs: { locked: true } }, WEEK[1]] });
    button(card, "Show details").click();
    await settle(card);
    expect((button(card, "New dinner") as HTMLButtonElement).disabled).toBe(true);
    expect(card.shadowRoot!.querySelector('select[aria-label="Swap with…"]')).toBeNull();
  });

  it("picks one of the alternatives", async () => {
    const { card, hass } = await mount();
    button(card, "Show details").click();
    await settle(card);
    const select = $(card, 'select[aria-label="Other options"]') as HTMLSelectElement;
    expect([...select.options].map((o) => o.textContent!.trim())).toEqual([
      "Other options: Choose…",
      "Alternativ 2026-11-02",
    ]);
    select.value = "alt:2026-11-02";
    select.dispatchEvent(new Event("change"));
    await settle(card);
    expect(hass.callService).toHaveBeenCalledWith("weeklymenu", "set_recipe", {
      date: "2026-11-02",
      recipe_id: "alt:2026-11-02",
    });
    expect(select.value).toBe("");
  });

  it("swaps with another unlocked day", async () => {
    const days = [WEEK[0], WEEK[1], { ...WEEK[2], attrs: { locked: true } }];
    const { card, hass } = await mount({ days });
    button(card, "Show details").click();
    await settle(card);
    const select = $(card, 'select[aria-label="Swap with…"]') as HTMLSelectElement;
    expect([...select.options].map((o) => o.value)).toEqual(["", "2026-11-03"]); // not itself, not the locked day
    select.value = "2026-11-03";
    select.dispatchEvent(new Event("change"));
    await settle(card);
    expect(hass.callService).toHaveBeenCalledWith("weeklymenu", "swap_days", {
      date: "2026-11-02",
      other_date: "2026-11-03",
    });
  });

  it("regenerates the whole week and confirms it after asking", async () => {
    const { card, hass } = await mount();
    button(card, "Regenerate all").click();
    await settle(card);
    expect(hass.callService).toHaveBeenLastCalledWith("weeklymenu", "generate_menu", { week_start: "2026-11-02" });

    button(card, "Confirm").click();
    await settle(card);
    expect(window.confirm).toHaveBeenCalledWith("Confirm this menu? It can't be changed afterwards.");
    expect(hass.callService).toHaveBeenLastCalledWith("weeklymenu", "confirm_menu", { week_start: "2026-11-02" });
  });

  it("does not confirm when the user says no", async () => {
    vi.spyOn(window, "confirm").mockReturnValue(false);
    const { card, hass } = await mount();
    button(card, "Confirm").click();
    await settle(card);
    expect(hass.callService).not.toHaveBeenCalled();
  });

  it("is busy while a service runs, and shows the error if it fails", async () => {
    const { card, hass } = await mount();
    let fail!: (err: Error) => void;
    hass.callService.mockReturnValueOnce(new Promise((_, reject) => (fail = reject)));
    button(card, "Regenerate all").click();
    await settle(card);
    expect(text(card)).toContain("Working…");
    // everything that changes the menu is off; only looking at details stays available
    const changing = $$(card, "button").filter((b) => b.getAttribute("aria-expanded") === null);
    expect(changing.length).toBeGreaterThan(2);
    expect(changing.every((b) => (b as HTMLButtonElement).disabled)).toBe(true);

    fail(new Error("No other recipe was found"));
    await vi.waitFor(() => expect(text(card)).toContain("Something went wrong: No other recipe was found"));
    expect(text(card)).not.toContain("Working…");
    expect((button(card, "Regenerate all") as HTMLButtonElement).disabled).toBe(false);
  });
});

describe("a confirmed menu and read-only dashboards", () => {
  it("cannot be changed once confirmed", async () => {
    const { card } = await mount({ status: "confirmed" });
    expect($(card, ".chip")!.className).toContain("confirmed");
    expect(text(card)).toContain("The menu is confirmed and can't be changed.");
    expect($$(card, "button.icon[aria-pressed]")).toHaveLength(0);
    expect($(card, ".foot")).toBeNull();
    button(card, "Show details").click();
    await settle(card);
    expect($(card, ".more input")).toBeNull();
    expect($(card, ".more li")).not.toBeNull(); // still readable
  });

  it("hides every control when show_actions is off", async () => {
    const { card } = await mount({}, { show_actions: false });
    expect($$(card, "button.icon[aria-pressed]")).toHaveLength(0);
    expect($(card, ".foot")).toBeNull();
    expect(text(card)).not.toContain("can't be changed");
  });
});

describe("registration", () => {
  it("is a custom element and lists itself for the card picker", () => {
    expect(customElements.get("weeklymenu-menu-card")).toBeDefined();
    expect(window.customCards?.map((c) => c.type)).toEqual(["weeklymenu-menu-card", "weeklymenu-today-card"]);
    expect(document.createElement("weeklymenu-menu-card").constructor).toHaveProperty("getStubConfig");
    const editor = (customElements.get("weeklymenu-menu-card") as unknown as typeof WeeklyMenuCard).getConfigElement();
    expect(editor.tagName.toLowerCase()).toBe("weeklymenu-menu-card-editor");
  });
});
