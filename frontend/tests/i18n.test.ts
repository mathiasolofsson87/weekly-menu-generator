import { describe, expect, it } from "vitest";
import { dayLabel, weekdayKeyName } from "../src/format";
import { language, t, tagLabel, warning } from "../src/i18n";

describe("language", () => {
  it("prefers the user's locale, falls back to the system language, then English", () => {
    expect(language({ language: "en", locale: { language: "sv-SE" } })).toBe("sv");
    expect(language({ language: "sv" })).toBe("sv");
    expect(language({ language: "de" })).toBe("en");
    expect(language(undefined)).toBe("en");
  });
});

describe("t", () => {
  it("translates and fills in variables", () => {
    expect(t({ language: "sv" }, "week", { n: 45 })).toBe("Vecka 45");
    expect(t({ language: "en" }, "week", { n: 45 })).toBe("Week 45");
    expect(t({ language: "sv" }, "splitNote", { members: "Anna", from: "a", to: "b" })).toBe("Anna: a → b");
  });
  it("keeps a placeholder that was not given", () => {
    expect(t({ language: "en" }, "week")).toBe("Week {n}");
  });
});

describe("warning", () => {
  const day = (key: string) => (key === "tue" ? "Tuesday" : key);
  it("explains known codes", () => {
    expect(warning({ language: "en" }, "no_recipe:tue", day)).toBe("No recipe was found for Tuesday.");
    expect(warning({ language: "sv" }, "source_failed:ica", day)).toBe("Receptkällan ica fungerade inte.");
    expect(warning({ language: "en" }, "no_sources", day)).toBe("No recipe sources are active or set up.");
  });
  it("shows an unknown code as it is", () => {
    expect(warning({ language: "en" }, "something_new:x", day)).toBe("something_new:x");
  });
});

describe("dates", () => {
  it("labels a date in the user's language", () => {
    expect(dayLabel({ language: "sv" }, "2026-11-02")).toEqual({ weekday: "mån", date: "2 nov." });
    expect(dayLabel({ language: "en" }, "2026-11-02")).toEqual({ weekday: "Mon", date: "Nov 2" });
  });
  it("names a weekday key", () => {
    expect(weekdayKeyName({ language: "sv" }, "tue")).toBe("tisdag");
    expect(weekdayKeyName({ language: "en" }, "sun")).toBe("Sunday");
    expect(weekdayKeyName({ language: "en" }, "xyz")).toBe("xyz");
  });
});

describe("tags", () => {
  it("translates the style tags the backend produces", () => {
    expect(tagLabel({ language: "sv" }, "family_friendly")).toBe("Barnvänligt");
    expect(tagLabel({ language: "en" }, "quick")).toBe("Quick");
  });
  it("shows an unknown tag as written", () => {
    expect(tagLabel({ language: "sv" }, "air_fryer")).toBe("air fryer");
  });
});
