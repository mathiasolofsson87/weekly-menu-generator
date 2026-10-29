import { afterEach, describe, expect, it } from "vitest";
import "../src/index";
import type { WeeklyMenuShoppingCard } from "../src/shopping-card";
import { SHOPPING, makeHass, settle, type HassOptions } from "./fixtures";

async function mount(options: HassOptions = {}, config: Record<string, unknown> = {}) {
  const hass = makeHass({ shopping: { state: "3", attrs: SHOPPING }, ...options });
  const card = document.createElement("weeklymenu-shopping-card") as WeeklyMenuShoppingCard;
  card.setConfig({ type: "custom:weeklymenu-shopping-card", ...config });
  card.hass = hass;
  document.body.append(card);
  await settle(card);
  return { card, hass };
}
const $ = (card: Element, selector: string) => card.shadowRoot!.querySelector<HTMLElement>(selector);
const $$ = (card: Element, selector: string) => [...card.shadowRoot!.querySelectorAll<HTMLElement>(selector)];
const text = (card: Element) => card.shadowRoot!.textContent!.replace(/\s+/g, " ").trim();
const header = (card: Element) => (card.shadowRoot!.querySelector("ha-card") as unknown as { header: string }).header;

afterEach(() => {
  document.body.innerHTML = "";
});

describe("shopping card", () => {
  it("summarises the week and where it went", async () => {
    const { card } = await mount();
    expect(header(card)).toBe("Shopping");
    expect(text(card)).toContain("Week 45 · To: todo.groceries, ICA: Veckomeny vecka 45");
    const chips = $$(card, ".chip").map((c) => c.textContent!.trim());
    expect(chips).toEqual(["Needs a look: 1", "Not delivered: 2", "Added: 3", "Pantry (not bought): 2"]);
  });

  it("opens what needs attention and folds the rest away", async () => {
    const { card } = await mount();
    const groups = Object.fromEntries(
      $$(card, "details").map((d) => [d.querySelector("summary")!.textContent!.trim(), (d as HTMLDetailsElement).open]),
    );
    expect(groups).toEqual({ "Needs a look (1)": true, "Not delivered (2)": true, "Added (3)": false });
    expect($$(card, "details li").map((li) => li.textContent)).toContain("230 g nötfärs");
  });

  it("can hide the added items, and lists the pantry skips on request", async () => {
    const hidden = (await mount({}, { show_added: false })).card;
    expect(text(hidden)).not.toContain("230 g nötfärs");
    expect(text(hidden)).not.toContain("olivolja");
    expect(text((await mount({}, { show_skipped: true })).card)).toContain("olivolja");
  });

  it("explains problems in plain language, once each", async () => {
    const { card } = await mount();
    const banners = $$(card, ".banner.warning").map((b) => b.textContent!.trim());
    // the generic "a sign-in failed" is left out because the store is already named
    expect(banners).toEqual(["The sign-in to ICA no longer works. Sign in again under Settings."]);
  });

  it("keeps the generic sign-in message when no store is named", async () => {
    const { card } = await mount({ shopping: { state: "0", attrs: { ...SHOPPING, errors: ["reauth_required", "no_targets"] } } });
    expect($$(card, ".banner.warning").map((b) => b.textContent!.trim())).toEqual([
      "A sign-in no longer works. Sign in again under Settings.",
      "No shopping list is set up.",
    ]);
  });

  it("is in Swedish for a Swedish user", async () => {
    const { card } = await mount({ language: "sv" });
    expect(header(card)).toBe("Inköp");
    expect(text(card)).toContain("Vecka 45");
    expect($$(card, ".chip")[0].textContent!.trim()).toBe("Behöver granskas: 1");
  });

  it("offers to try again when something failed, and does so", async () => {
    const { card, hass } = await mount();
    $(card, ".foot button")!.click();
    await settle(card);
    expect(hass.callService).toHaveBeenCalledWith("weeklymenu", "add_to_shopping", {});
  });

  it("has nothing to retry when everything went well", async () => {
    const attrs = { ...SHOPPING, counts: { ...SHOPPING.counts, failed: 0, review: 0 }, failed: [], review: [], errors: [] };
    const { card } = await mount({ shopping: { state: "3", attrs } });
    expect($(card, ".foot")).toBeNull();
    expect($$(card, ".banner")).toHaveLength(0);
  });

  it("shows the error if trying again fails", async () => {
    const { card, hass } = await mount();
    hass.callService.mockRejectedValueOnce(new Error("There is no confirmed menu to shop for."));
    $(card, ".foot button")!.click();
    await settle(card);
    await settle(card);
    expect(text(card)).toContain("Something went wrong: There is no confirmed menu to shop for.");
  });

  it("says so before any shopping", async () => {
    const { card } = await mount({ shopping: null });
    expect(text(card)).toContain("Nothing has been bought yet.");
    expect($$(card, "details")).toHaveLength(0);
  });

  it("is a custom element with an editor", () => {
    expect(customElements.get("weeklymenu-shopping-card")).toBeDefined();
    const editor = (customElements.get("weeklymenu-shopping-card") as unknown as typeof WeeklyMenuShoppingCard).getConfigElement();
    expect(editor.tagName.toLowerCase()).toBe("weeklymenu-shopping-card-editor");
  });
});
