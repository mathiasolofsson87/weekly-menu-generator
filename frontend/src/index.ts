import { language, t } from "./i18n";
import { WeeklyMenuCardEditor, WeeklyMenuTodayCardEditor } from "./editors";
import { WeeklyMenuCard } from "./menu-card";
import { WeeklyMenuTodayCard } from "./today-card";

declare global {
  interface Window {
    customCards?: { type: string; name: string; description: string; preview?: boolean }[];
  }
}

function define(name: string, element: CustomElementConstructor): void {
  if (!customElements.get(name)) customElements.define(name, element);
}

define("weeklymenu-menu-card", WeeklyMenuCard);
define("weeklymenu-menu-card-editor", WeeklyMenuCardEditor);
define("weeklymenu-today-card", WeeklyMenuTodayCard);
define("weeklymenu-today-card-editor", WeeklyMenuTodayCardEditor);

// Names in the card picker, in the browser's language (the picker has no Home Assistant object yet).
const hass = { language: language({ language: navigator.language }) };
window.customCards = window.customCards ?? [];
window.customCards.push(
  {
    type: "weeklymenu-menu-card",
    name: t(hass, "cardMenuName"),
    description: t(hass, "cardMenuDescription"),
    preview: true,
  },
  {
    type: "weeklymenu-today-card",
    name: t(hass, "cardTodayName"),
    description: t(hass, "cardTodayDescription"),
    preview: true,
  },
);
