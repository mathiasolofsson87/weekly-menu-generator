import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import "../src/index";
import type { WeeklyMenuFamilyCard } from "../src/family-card";
import { FAMILY, makeHass, settle, type HassOptions } from "./fixtures";

async function mount(options: HassOptions = {}, config: Record<string, unknown> = {}) {
  const hass = makeHass({ family: { members: FAMILY }, ...options });
  const card = document.createElement("weeklymenu-family-card") as WeeklyMenuFamilyCard;
  card.setConfig({ type: "custom:weeklymenu-family-card", ...config });
  card.hass = hass;
  document.body.append(card);
  await settle(card);
  return { card, hass };
}
const $ = (card: Element, selector: string) => card.shadowRoot!.querySelector<HTMLElement>(selector);
const $$ = (card: Element, selector: string) => [...card.shadowRoot!.querySelectorAll<HTMLElement>(selector)];
const text = (card: Element) => card.shadowRoot!.textContent!.replace(/\s+/g, " ").trim();
const button = (card: Element, label: string) => $$(card, "button").find((b) => b.textContent!.trim() === label)! as HTMLButtonElement;

async function type(card: Element, label: string, value: string) {
  const field = $$(card, "label.field").find((l) => l.querySelector("span")!.textContent!.trim().startsWith(label))!;
  const input = field.querySelector("input")!;
  input.value = value;
  input.dispatchEvent(new Event("input"));
  await settle(card as never);
}
async function tick(card: Element, label: string, on: boolean) {
  const box = $$(card, "label.check").find((l) => l.textContent!.trim() === label)!.querySelector("input")!;
  box.checked = on;
  box.dispatchEvent(new Event("change"));
  await settle(card as never);
}
async function choose(card: Element, label: string, value: string) {
  const field = $$(card, "label.field").find((l) => l.querySelector("span")!.textContent!.trim() === label)!;
  const select = field.querySelector("select")!;
  select.value = value;
  select.dispatchEvent(new Event("change"));
  await settle(card as never);
}

beforeEach(() => {
  vi.spyOn(window, "confirm").mockReturnValue(true);
});
afterEach(() => {
  document.body.innerHTML = "";
  vi.restoreAllMocks();
});

describe("what it shows", () => {
  it("lists the family with diet, portion, allergies and days", async () => {
    const { card } = await mount();
    const [anna, olle] = $$(card, ".member");
    expect(anna.querySelector(".title")!.textContent).toBe("Anna");
    const meta = anna.querySelector(".meta")!.textContent!.replace(/\s+/g, " ");
    expect(meta).toContain("Vegetarian");
    expect(meta).toContain("Small");
    expect($$(card, ".tag.allergy").map((t) => t.textContent)).toEqual(["Milk", "kiwi"]); // known ones translated, custom as written
    expect(meta).toContain("svamp");
    expect(meta).toContain("Every dinner");
    expect(olle.querySelector(".meta")!.textContent).toContain("Mon, Wed");
  });

  it("is in Swedish for a Swedish user", async () => {
    const { card } = await mount({ language: "sv" });
    expect((card.shadowRoot!.querySelector("ha-card") as unknown as { header: string }).header).toBe("Familj");
    expect($$(card, ".tag.allergy")[0].textContent).toBe("Mjölk");
    expect(text(card)).toContain("Alla middagar");
  });

  it("says so when the family is empty or not available yet", async () => {
    expect(text((await mount({ family: { members: [] } })).card)).toContain("Nobody has been added yet.");
    expect(text((await mount({ family: null })).card)).toContain("not available yet");
  });

  it("is read-only when editing is off", async () => {
    const { card } = await mount({}, { editable: false });
    expect($$(card, "button")).toHaveLength(0);
  });
});

const PEOPLE = [
  { id: "person.eva", name: "Eva Berg", picture: "/api/image/serve/abc/512x512" },
  { id: "person.kim", name: "Kim" },
];

describe("linking a Home Assistant person", () => {
  async function open(options: HassOptions = {}) {
    const mounted = await mount({ persons: PEOPLE, ...options });
    button(mounted.card, "Add person").click();
    await settle(mounted.card);
    return mounted;
  }
  const personSelect = (card: Element) => $$(card, "label.field").find((l) => l.querySelector("span")!.textContent!.startsWith("Home Assistant person"))!.querySelector("select")!;

  it("offers the people in Home Assistant and fills in the name", async () => {
    const { card, hass } = await open();
    const select = personSelect(card);
    expect([...select.options].map((o) => o.textContent!.trim())).toEqual(["None", "Eva Berg", "Kim"]);
    select.value = "person.eva";
    select.dispatchEvent(new Event("change"));
    await settle(card);
    expect(($$(card, "label.field input")[0] as HTMLInputElement).value).toBe("Eva Berg");
    button(card, "Save").click();
    await settle(card);
    expect(hass.callService).toHaveBeenCalledWith("weeklymenu", "set_member", expect.objectContaining({ name: "Eva Berg", person: "person.eva" }));
  });

  it("keeps a name that was typed by hand", async () => {
    const { card } = await open();
    await type(card, "Name", "Evita");
    personSelect(card).value = "person.eva";
    personSelect(card).dispatchEvent(new Event("change"));
    await settle(card);
    expect(($$(card, "label.field input")[0] as HTMLInputElement).value).toBe("Evita");
  });

  it("changes the name along when another person is picked", async () => {
    const { card } = await open();
    for (const id of ["person.eva", "person.kim"]) {
      personSelect(card).value = id;
      personSelect(card).dispatchEvent(new Event("change"));
      await settle(card);
    }
    expect(($$(card, "label.field input")[0] as HTMLInputElement).value).toBe("Kim");
  });

  it("is left out when Home Assistant has no people", async () => {
    const { card } = await mount();
    button(card, "Add person").click();
    await settle(card);
    expect($$(card, "label.field").some((l) => l.textContent!.includes("Home Assistant person"))).toBe(false);
  });

  it("shows the picture of a linked person and the first letter of others", async () => {
    const { card } = await mount({
      persons: PEOPLE,
      family: { members: [{ ...FAMILY[0], person: "person.eva" }, { ...FAMILY[1], person: "person.kim" }] },
    });
    const [anna, olle] = $$(card, ".member");
    expect(anna.querySelector("img.avatar")!.getAttribute("src")).toBe("/api/image/serve/abc/512x512");
    expect(olle.querySelector("img")).toBeNull();
    expect(olle.querySelector(".avatar")!.textContent).toBe("O"); // linked, but no picture
  });

  it("shows initials for people who are not linked", async () => {
    const { card } = await mount();
    expect($$(card, ".member .avatar").map((a) => a.textContent)).toEqual(["A", "O"]);
  });

  it("can unlink a person", async () => {
    const { card, hass } = await mount({
      persons: PEOPLE,
      family: { members: [{ ...FAMILY[0], person: "person.eva" }] },
    });
    button(card, "Edit").click();
    await settle(card);
    personSelect(card).value = "";
    personSelect(card).dispatchEvent(new Event("change"));
    await settle(card);
    button(card, "Save").click();
    await settle(card);
    expect(hass.callService).toHaveBeenCalledWith("weeklymenu", "set_member", expect.objectContaining({ id: "1", person: null }));
  });
});

describe("adding a person", () => {
  it("opens an empty form with sensible defaults", async () => {
    const { card } = await mount();
    button(card, "Add person").click();
    await settle(card);
    expect(($$(card, "label.field input")[0] as HTMLInputElement).value).toBe("");
    expect(button(card, "Save").disabled).toBe(true); // no name yet
    const days = $$(card, "fieldset")[1].querySelectorAll<HTMLInputElement>("input");
    expect([...days].map((d) => d.checked)).toEqual([true, true, true, true, true]); // the dinner days
    expect(button(card, "Remove")).toBeUndefined();
  });

  it("saves what was entered through set_member", async () => {
    const { card, hass } = await mount();
    button(card, "Add person").click();
    await settle(card);
    await type(card, "Name", "  Eva ");
    await tick(card, "Egg", true);
    await tick(card, "Fish", true);
    await type(card, "Other allergies", "kiwi, , mango ");
    await type(card, "Dislikes", "lök,svamp");
    await choose(card, "Diet", "vegan");
    await choose(card, "Portion size", "large");
    await tick(card, "Fri", false);
    await tick(card, "Allergens can be cooked separately (turn off for severe allergies)", false);
    button(card, "Save").click();
    await settle(card);
    expect(hass.callService).toHaveBeenCalledWith("weeklymenu", "set_member", {
      name: "Eva",
      allergies: ["egg", "fish", "kiwi", "mango"],
      dislikes: ["lök", "svamp"],
      likes: [],
      diet: "vegan",
      portion: "large",
      attends: ["mon", "tue", "wed", "thu"],
      cook_separately: false,
    });
    expect($(card, "form")).toBeNull(); // closed after saving
  });

  it("will not save without a name or without any day", async () => {
    const { card, hass } = await mount();
    button(card, "Add person").click();
    await settle(card);
    await type(card, "Name", "Eva");
    expect(button(card, "Save").disabled).toBe(false);
    for (const day of ["Mon", "Tue", "Wed", "Thu", "Fri"]) await tick(card, day, false);
    expect(button(card, "Save").disabled).toBe(true);
    expect(text(card)).toContain("Pick at least one day.");
    expect(hass.callService).not.toHaveBeenCalled();
  });

  it("can be cancelled", async () => {
    const { card, hass } = await mount();
    button(card, "Add person").click();
    await settle(card);
    button(card, "Cancel").click();
    await settle(card);
    expect($(card, "form")).toBeNull();
    expect(hass.callService).not.toHaveBeenCalled();
  });
});

describe("changing and removing", () => {
  it("fills the form from the person, with known and own allergies apart", async () => {
    const { card } = await mount();
    button(card, "Edit").click();
    await settle(card);
    const value = (label: string) =>
      ($$(card, "label.field").find((l) => l.querySelector("span")!.textContent!.trim().startsWith(label))!.querySelector("input") as HTMLInputElement).value;
    expect(value("Name")).toBe("Anna");
    expect(value("Other allergies")).toBe("kiwi");
    expect(value("Dislikes")).toBe("svamp");
    const milk = $$(card, "label.check").find((l) => l.textContent!.trim() === "Milk")!.querySelector("input")!;
    expect(milk.checked).toBe(true);
    const separately = $$(card, "label.check").find((l) => l.textContent!.includes("cooked separately"))!.querySelector("input")!;
    expect(separately.checked).toBe(false);
    expect(button(card, "Remove")).toBeDefined();
  });

  it("saves a change with the person's id", async () => {
    const { card, hass } = await mount();
    button(card, "Edit").click();
    await settle(card);
    await choose(card, "Portion size", "normal");
    button(card, "Save").click();
    await settle(card);
    expect(hass.callService).toHaveBeenCalledWith(
      "weeklymenu",
      "set_member",
      expect.objectContaining({ id: "1", name: "Anna", portion: "normal", allergies: ["milk", "kiwi"], cook_separately: false }),
    );
  });

  it("removes a person after asking", async () => {
    const { card, hass } = await mount();
    button(card, "Edit").click();
    await settle(card);
    button(card, "Remove").click();
    await settle(card);
    expect(window.confirm).toHaveBeenCalledWith("Remove Anna?");
    expect(hass.callService).toHaveBeenCalledWith("weeklymenu", "remove_member", { id: "1" });
  });

  it("keeps the person when the question is answered no", async () => {
    vi.spyOn(window, "confirm").mockReturnValue(false);
    const { card, hass } = await mount();
    button(card, "Edit").click();
    await settle(card);
    button(card, "Remove").click();
    await settle(card);
    expect(hass.callService).not.toHaveBeenCalled();
    expect($(card, "form")).not.toBeNull();
  });

  it("keeps the form open and shows the reason when saving fails", async () => {
    const { card, hass } = await mount();
    button(card, "Add person").click();
    await settle(card);
    await type(card, "Name", "Anna");
    hass.callService.mockRejectedValueOnce(new Error("There is already a family member called Anna."));
    button(card, "Save").click();
    await settle(card);
    await settle(card);
    expect(text(card)).toContain("Something went wrong: There is already a family member called Anna.");
    expect($(card, "form")).not.toBeNull();
  });
});
