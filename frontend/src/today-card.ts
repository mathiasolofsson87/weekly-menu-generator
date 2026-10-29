import { LitElement, html, nothing, type TemplateResult } from "lit";
import { readToday } from "./data";
import { t } from "./i18n";
import { renderIngredients, renderMeta, renderSplit } from "./parts";
import { cardStyles } from "./styles";
import type { HomeAssistant, LovelaceCardConfig } from "./types";

export interface TodayCardConfig extends LovelaceCardConfig {
  title?: string;
  show_image?: boolean;
  show_ingredients?: boolean;
}

/** Tonight's dinner, compact. */
export class WeeklyMenuTodayCard extends LitElement {
  static override properties = {
    hass: { attribute: false },
    _config: { state: true },
  };
  static override styles = [
    cardStyles,
    // only what differs from the menu card
  ];

  declare hass: HomeAssistant;
  declare _config: TodayCardConfig;

  constructor() {
    super();
    this._config = { type: "custom:weeklymenu-today-card" };
  }

  static getConfigElement(): HTMLElement {
    return document.createElement("weeklymenu-today-card-editor");
  }

  static getStubConfig(): Partial<TodayCardConfig> {
    return {};
  }

  setConfig(config: TodayCardConfig): void {
    if (!config) throw new Error("Invalid configuration");
    this._config = { show_image: true, show_ingredients: false, ...config };
  }

  getCardSize(): number {
    return 3;
  }

  protected override render(): TemplateResult {
    if (!this.hass) return html``;
    const hass = this.hass;
    const dinner = readToday(hass);
    const header = this._config.title ?? t(hass, "todayTitle");
    if (!dinner) {
      return html`<ha-card .header=${header}><div class="empty">${t(hass, "noDinner")}</div></ha-card>`;
    }
    const title = dinner.url
      ? html`<a href=${dinner.url} target="_blank" rel="noopener noreferrer" title=${t(hass, "openRecipe")}>${dinner.title}</a>`
      : dinner.title;
    return html`<ha-card .header=${header}>
      <div class="day" style="grid-template-columns: 1fr">
        <div class="main">
          ${this._config.show_image !== false && dinner.image
            ? html`<img src=${dinner.image} alt="" loading="lazy" style="width:72px;height:72px" />`
            : nothing}
          <div>
            <div class="title">${title}</div>
            ${renderMeta(hass, dinner)}
          </div>
        </div>
        <div class="more" style="padding-left:0">
          ${renderSplit(hass, dinner.split)}
          ${this._config.show_ingredients ? renderIngredients(hass, dinner.ingredients) : nothing}
        </div>
      </div>
    </ha-card>`;
  }
}
