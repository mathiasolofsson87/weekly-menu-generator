import { afterEach, describe, expect, it } from "vitest";
import "../src/index";
import type { WeeklyMenuCardEditor } from "../src/editors";
import { makeHass, settle } from "./fixtures";

type Form = HTMLElement & {
  data: Record<string, unknown>;
  schema: { name: string }[];
  computeLabel: (field: { name: string }) => string;
};

async function mount(tag: string, config: Record<string, unknown>, language = "en") {
  const editor = document.createElement(tag) as WeeklyMenuCardEditor;
  editor.setConfig({ type: "custom:x", ...config });
  editor.hass = makeHass({ language });
  document.body.append(editor);
  await settle(editor);
  return { editor, form: editor.shadowRoot!.querySelector("ha-form") as Form };
}

afterEach(() => {
  document.body.innerHTML = "";
});

describe("menu card editor", () => {
  it("builds a form from the card's options, filling in the defaults", async () => {
    const { form } = await mount("weeklymenu-menu-card-editor", { title: "Mat" });
    expect(form.schema.map((f) => f.name)).toEqual(["title", "show_images", "show_actions"]);
    expect(form.data).toMatchObject({ title: "Mat", show_images: true, show_actions: true });
  });

  it("labels the fields in the user's language", async () => {
    const { form } = await mount("weeklymenu-menu-card-editor", {}, "sv");
    expect(form.schema.map((f) => form.computeLabel(f))).toEqual([
      "Rubrik",
      "Visa bilder",
      "Visa knappar för att ändra menyn",
    ]);
  });

  it("reports changes as a new config, keeping what it does not edit", async () => {
    const { editor, form } = await mount("weeklymenu-menu-card-editor", { title: "Mat", grid_options: { rows: 3 } });
    const seen: unknown[] = [];
    editor.addEventListener("config-changed", (ev) => seen.push((ev as CustomEvent).detail.config));
    form.dispatchEvent(
      new CustomEvent("value-changed", { detail: { value: { title: "Mat", show_images: false, show_actions: true } } }),
    );
    expect(seen).toEqual([
      { type: "custom:x", title: "Mat", grid_options: { rows: 3 }, show_images: false, show_actions: true },
    ]);
  });
});

describe("today card editor", () => {
  it("has its own options and defaults", async () => {
    const { form } = await mount("weeklymenu-today-card-editor", {});
    expect(form.schema.map((f) => f.name)).toEqual(["title", "show_image", "show_ingredients"]);
    expect(form.data).toMatchObject({ show_image: true, show_ingredients: false });
    expect(form.computeLabel({ name: "show_ingredients" })).toBe("Show ingredients");
  });

  it("renders nothing until it has both a config and hass", async () => {
    const editor = document.createElement("weeklymenu-today-card-editor") as WeeklyMenuCardEditor;
    document.body.append(editor);
    await editor.updateComplete;
    expect(editor.shadowRoot!.querySelector("ha-form")).toBeNull();
  });
});
