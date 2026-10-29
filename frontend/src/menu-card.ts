import { LitElement, html, nothing, type TemplateResult } from "lit";
import { DOMAIN, isoWeek, readMenu } from "./data";
import { dayLabel, weekdayKeyName } from "./format";
import { t, warning } from "./i18n";
import { errorMessage, renderIngredients, renderMeta, renderSplit } from "./parts";
import { cardStyles } from "./styles";
import type { Dinner, HomeAssistant, LovelaceCardConfig, MenuModel } from "./types";

export interface MenuCardConfig extends LovelaceCardConfig {
  title?: string;
  show_images?: boolean;
  show_actions?: boolean;
}

/** The week's dinners, with the buttons to change them. */
export class WeeklyMenuCard extends LitElement {
  static override properties = {
    hass: { attribute: false },
    _config: { state: true },
    _open: { state: true },
    _busy: { state: true },
    _error: { state: true },
    _hints: { state: true },
  };
  static override styles = cardStyles;

  declare hass: HomeAssistant;
  declare _config: MenuCardConfig;
  declare _open: Set<string>;
  declare _busy: boolean;
  declare _error: string;
  declare _hints: Record<string, string>;

  constructor() {
    super();
    this._config = { type: "custom:weeklymenu-menu-card" };
    this._open = new Set();
    this._busy = false;
    this._error = "";
    this._hints = {};
  }

  static getConfigElement(): HTMLElement {
    return document.createElement("weeklymenu-menu-card-editor");
  }

  static getStubConfig(): Partial<MenuCardConfig> {
    return {};
  }

  setConfig(config: MenuCardConfig): void {
    if (!config) throw new Error("Invalid configuration");
    this._config = { show_images: true, show_actions: true, ...config };
  }

  getCardSize(): number {
    return this.hass ? 2 + readMenu(this.hass).days.length : 4;
  }

  // --- actions ------------------------------------------------------------------

  private async _call(service: string, data: Record<string, unknown> = {}): Promise<void> {
    this._busy = true;
    this._error = "";
    try {
      await this.hass.callService(DOMAIN, service, data);
    } catch (err) {
      this._error = errorMessage(err);
    } finally {
      this._busy = false;
    }
  }

  private _toggle(date: string): void {
    const open = new Set(this._open);
    if (!open.delete(date)) open.add(date);
    this._open = open;
  }

  private _confirm(menu: MenuModel): void {
    if (!window.confirm(t(this.hass, "confirmAsk"))) return;
    void this._call("confirm_menu", menu.weekStart ? { week_start: menu.weekStart } : {});
  }

  private _regenerateDay(day: Dinner): void {
    const hint = (this._hints[day.date] ?? "").trim();
    void this._call("regenerate_day", { date: day.date, ...(hint ? { hint } : {}) });
  }

  private _pick(day: Dinner, ev: Event): void {
    const select = ev.target as HTMLSelectElement;
    const value = select.value;
    select.value = "";
    if (value) void this._call("set_recipe", { date: day.date, recipe_id: value });
  }

  private _swap(day: Dinner, ev: Event): void {
    const select = ev.target as HTMLSelectElement;
    const value = select.value;
    select.value = "";
    if (value) void this._call("swap_days", { date: day.date, other_date: value });
  }

  // --- rendering -------------------------------------------------------------------

  protected override render(): TemplateResult {
    if (!this.hass) return html``;
    const hass = this.hass;
    const menu = readMenu(hass);
    const confirmed = menu.status === "confirmed";
    const canEdit = this._config.show_actions !== false && !confirmed;
    const warnings = [...new Set(menu.warnings.map((w) => warning(hass, w, (d) => weekdayKeyName(hass, d))))];

    return html`<ha-card .header=${this._config.title ?? t(hass, "menuTitle")}>
      <div class="head">
        <span>${menu.weekStart ? t(hass, "week", { n: isoWeek(menu.weekStart) }) : ""}</span>
        <span class="chip ${menu.status}">${t(hass, `status_${menu.status}`)}</span>
      </div>
      ${warnings.map((text) => html`<div class="banner warning">${text}</div>`)}
      ${this._error ? html`<div class="banner error">${t(hass, "error", { error: this._error })}</div>` : nothing}
      ${this._busy ? html`<div class="banner">${t(hass, "working")}</div>` : nothing}
      ${menu.days.length
        ? menu.days.map((day) => this._renderDay(day, menu, canEdit))
        : html`<div class="empty">${t(hass, "noMenu")}</div>`}
      ${confirmed && this._config.show_actions !== false
        ? html`<div class="banner">${t(hass, "confirmedNote")}</div>`
        : nothing}
      ${this._renderFooter(menu, canEdit)}
    </ha-card>`;
  }

  private _renderFooter(menu: MenuModel, canEdit: boolean): TemplateResult | typeof nothing {
    if (!canEdit) return nothing;
    const empty = menu.days.length === 0;
    return html`<div class="foot">
      <button
        class=${empty ? "primary" : ""}
        ?disabled=${this._busy}
        @click=${() => this._call("generate_menu", menu.weekStart && !empty ? { week_start: menu.weekStart } : {})}
      >
        ${empty ? t(this.hass, "generate") : t(this.hass, "regenerateAll")}
      </button>
      ${menu.status === "draft" && !empty
        ? html`<button class="primary" ?disabled=${this._busy} @click=${() => this._confirm(menu)}>
            ${t(this.hass, "confirm")}
          </button>`
        : nothing}
    </div>`;
  }

  private _renderDay(day: Dinner, menu: MenuModel, canEdit: boolean): TemplateResult {
    const hass = this.hass;
    const label = dayLabel(hass, day.date);
    const open = this._open.has(day.date);
    const title = day.url
      ? html`<a href=${day.url} target="_blank" rel="noopener noreferrer" title=${t(hass, "openRecipe")}>${day.title}</a>`
      : day.title;
    const others = menu.days.filter((d) => d.date !== day.date && !d.locked);

    return html`<div class="day">
      <div class="when">
        <div class="wd">${label.weekday}</div>
        <div class="dt">${label.date}</div>
      </div>
      <div class="main">
        ${this._config.show_images !== false && day.image ? html`<img src=${day.image} alt="" loading="lazy" />` : nothing}
        <div>
          <div class="title">${title}</div>
          ${renderMeta(hass, day)}
        </div>
      </div>
      <div class="actions">
        ${canEdit
          ? html`<button
              class="icon ${day.locked ? "on" : ""}"
              ?disabled=${this._busy}
              title=${day.locked ? t(hass, "unlock") : t(hass, "lock")}
              aria-label=${day.locked ? t(hass, "unlock") : t(hass, "lock")}
              aria-pressed=${day.locked ? "true" : "false"}
              @click=${() => this._call("lock_day", { date: day.date, locked: !day.locked })}
            >
              <ha-icon icon=${day.locked ? "mdi:lock" : "mdi:lock-open-variant-outline"}></ha-icon>
            </button>`
          : nothing}
        <button
          class="icon"
          title=${open ? t(hass, "hide") : t(hass, "show")}
          aria-label=${open ? t(hass, "hide") : t(hass, "show")}
          aria-expanded=${open ? "true" : "false"}
          @click=${() => this._toggle(day.date)}
        >
          <ha-icon icon=${open ? "mdi:chevron-up" : "mdi:chevron-down"}></ha-icon>
        </button>
      </div>
      ${open ? this._renderMore(day, others, canEdit) : nothing}
    </div>`;
  }

  private _renderMore(day: Dinner, others: Dinner[], canEdit: boolean): TemplateResult {
    const hass = this.hass;
    return html`<div class="more">
      ${renderSplit(hass, day.split)} ${renderIngredients(hass, day.ingredients)}
      ${canEdit
        ? html`<div class="row">
              <input
                type="text"
                .value=${this._hints[day.date] ?? ""}
                placeholder=${t(hass, "hint")}
                aria-label=${t(hass, "hint")}
                @input=${(ev: Event) => {
                  this._hints = { ...this._hints, [day.date]: (ev.target as HTMLInputElement).value };
                }}
              />
              <button ?disabled=${this._busy || day.locked} @click=${() => this._regenerateDay(day)}>
                ${t(hass, "newDinner")}
              </button>
            </div>
            <div class="row">
              ${day.alternatives.length
                ? html`<select
                    ?disabled=${this._busy}
                    aria-label=${t(hass, "alternatives")}
                    @change=${(ev: Event) => this._pick(day, ev)}
                  >
                    <option value="">${t(hass, "alternatives")}: ${t(hass, "choose")}</option>
                    ${day.alternatives.map((alt) => html`<option value=${alt.id}>${alt.title}</option>`)}
                  </select>`
                : nothing}
              ${others.length && !day.locked
                ? html`<select
                    ?disabled=${this._busy}
                    aria-label=${t(hass, "swapWith")}
                    @change=${(ev: Event) => this._swap(day, ev)}
                  >
                    <option value="">${t(hass, "swapWith")}</option>
                    ${others.map((other) => {
                      const l = dayLabel(hass, other.date);
                      return html`<option value=${other.date}>${l.weekday} ${l.date}: ${other.title}</option>`;
                    })}
                  </select>`
                : nothing}
            </div>`
        : nothing}
    </div>`;
  }
}
