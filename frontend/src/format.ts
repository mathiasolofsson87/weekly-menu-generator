import { language, type LangSource } from "./i18n";

function parse(isoDate: string): Date {
  const [y, m, d] = isoDate.split("-").map(Number);
  return new Date(Date.UTC(y, m - 1, d));
}

/** "mån" and "2 nov" for an ISO date, in the user's language. */
export function dayLabel(hass: LangSource | undefined, isoDate: string): { weekday: string; date: string } {
  const locale = language(hass);
  const date = parse(isoDate);
  const options = { timeZone: "UTC" } as const;
  return {
    weekday: new Intl.DateTimeFormat(locale, { ...options, weekday: "short" }).format(date),
    date: new Intl.DateTimeFormat(locale, { ...options, day: "numeric", month: "short" }).format(date),
  };
}

export function weekdayName(hass: LangSource | undefined, isoDate: string): string {
  return new Intl.DateTimeFormat(language(hass), { timeZone: "UTC", weekday: "long" }).format(parse(isoDate));
}

/** A language-aware name for a weekday key ("tue" -> "tisdag"). */
export function weekdayKeyName(hass: LangSource | undefined, key: string): string {
  const index = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"].indexOf(key);
  if (index < 0) return key;
  // 2026-11-02 is a Monday
  return weekdayName(hass, `2026-11-${String(2 + index).padStart(2, "0")}`);
}

/** A short, language-aware name for a weekday key ("tue" -> "Tue" / "tis"). */
export function weekdayShort(hass: LangSource | undefined, key: string): string {
  const index = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"].indexOf(key);
  if (index < 0) return key;
  return dayLabel(hass, `2026-11-${String(2 + index).padStart(2, "0")}`).weekday;
}
