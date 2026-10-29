import { describe, expect, it } from "vitest";
import { discover, isoWeek, percent, readDinner, readMenu, readToday } from "../src/data";
import { SPLIT, WEEK, makeHass } from "./fixtures";

describe("discover", () => {
  it("finds the integration's entities by translation key and ignores others", () => {
    const found = discover(makeHass({ days: WEEK }));
    expect(found.get("status")).toBe("sensor.weekly_menu_status");
    expect(found.get("weekday_tue")).toBe("sensor.weekly_menu_weekday_tue");
    expect(found.get("today")).toBe("sensor.weekly_menu_today");
    expect([...found.values()]).not.toContain("sensor.other");
  });

  it("copes with a frontend that has no entity registry", () => {
    const hass = makeHass();
    delete hass.entities;
    expect(discover(hass).size).toBe(0);
    expect(readMenu(hass)).toEqual({ status: "none", weekStart: undefined, warnings: [], days: [] });
  });
});

describe("readMenu", () => {
  it("reads status, week, warnings and the planned days in week order", () => {
    const menu = readMenu(makeHass({ days: [...WEEK].reverse(), warnings: ["no_recipe:thu"] }));
    expect(menu.status).toBe("draft");
    expect(menu.weekStart).toBe("2026-11-02");
    expect(menu.warnings).toEqual(["no_recipe:thu"]);
    expect(menu.days.map((d) => d.title)).toEqual(["Pasta carbonara", "Chili con carne", "Linsgryta"]);
    expect(menu.days.map((d) => d.weekday)).toEqual(["mon", "tue", "wed"]);
  });

  it("reads one dinner completely", () => {
    const [mon] = readMenu(makeHass({ days: [{ ...WEEK[0], attrs: { split: SPLIT, locked: true } }] })).days;
    expect(mon).toMatchObject({
      date: "2026-11-02",
      title: "Pasta carbonara",
      recipeId: "ica:2026-11-02",
      totalTime: 45,
      servings: 4,
      tags: ["quick", "family_friendly"],
      ingredients: ["400 g pasta", "2 dl grädde"],
      locked: true,
      source: "ica",
      alternatives: [{ id: "alt:2026-11-02", title: "Alternativ 2026-11-02" }],
    });
    expect(mon.split).toEqual([
      {
        members: ["Anna"],
        share: 0.5,
        separatePans: true,
        swaps: [{ original: "600 g entrecote", replacement: "600 g tofu" }],
      },
    ]);
  });

  it.each([["unknown"], ["unavailable"], [""]])("skips a day whose sensor is %j", (state) => {
    const hass = makeHass({ days: WEEK });
    hass.states["sensor.weekly_menu_weekday_tue"].state = state;
    expect(readMenu(hass).days.map((d) => d.weekday)).toEqual(["mon", "wed"]);
  });

  it("maps an unknown status to none", () => {
    expect(readMenu(makeHass({ status: "none" })).status).toBe("none");
    const hass = makeHass();
    hass.states["sensor.weekly_menu_status"].state = "unavailable";
    expect(readMenu(hass).status).toBe("none");
  });

  it("survives malformed attributes", () => {
    const hass = makeHass({
      days: [
        {
          ...WEEK[0],
          attrs: { split: { groups: "x" }, alternatives: [{ id: 1 }, null, { id: "a", title: "T" }], tags: "q", ingredients: [1, "ok"], total_time: "soon" },
        },
      ],
    });
    const [mon] = readMenu(hass).days;
    expect(mon.split).toEqual([]);
    expect(mon.alternatives).toEqual([{ id: "a", title: "T" }]);
    expect(mon.tags).toEqual([]);
    expect(mon.ingredients).toEqual(["ok"]);
    expect(mon.totalTime).toBeUndefined();
  });

  it("skips a sensor that has no date", () => {
    const hass = makeHass({ days: [WEEK[0]] });
    delete hass.states["sensor.weekly_menu_weekday_mon"].attributes.date;
    expect(readMenu(hass).days).toEqual([]);
  });
});

describe("readToday / readDinner", () => {
  it("reads tonight's dinner", () => {
    expect(readToday(makeHass({ today: { title: "Tacos" } }))?.title).toBe("Tacos");
  });
  it("is undefined when nothing is planned", () => {
    expect(readToday(makeHass({ today: null }))).toBeUndefined();
    expect(readDinner(makeHass(), undefined)).toBeUndefined();
  });
});

describe("helpers", () => {
  it.each([
    ["2026-11-02", 45],
    ["2026-01-01", 1],
    ["2020-12-31", 53],
    ["2021-01-03", 53],
    ["2021-01-04", 1],
    ["2024-12-30", 1],
  ])("isoWeek(%s) is %i", (date, week) => expect(isoWeek(date)).toBe(week));

  it("formats a share", () => {
    expect(percent(0.5)).toBe("50 %");
    expect(percent(1 / 3)).toBe("33 %");
  });

});
