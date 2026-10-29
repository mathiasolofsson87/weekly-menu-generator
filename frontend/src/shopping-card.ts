import { LitElement, html, nothing, type TemplateResult } from "lit";
import { DOMAIN, isoWeek, readShopping } from "./data";
import { t, shoppingError, type Key } from "./i18n";
import { errorMessage } from "./parts";
import { cardStyles } from "./styles";
import type { HomeAssistant, LovelaceCardConfig } from "./types";

export interface ShoppingCardConfig extends LovelaceCardConfig {
  title?: string;
  show_added?: boolean;
  show_skipped?: boolean;
}

type Group = "added" | "review" | "failed" | "pending" | "skipped";

const GROUPS: { key: Group; label: Key; css: string }[] = [
  { key: "review", label: "shopReview", css: "warning" },
  { key: "failed", label: "shopFailed", css: "error" },
  { key: "pending", label: "shopPending", css: "" },
  { key: "added", label: "shopAdded", css: "" },
  { key: "skipped", label: "shopSkipped", css: "" },
];

/** What the last confirmed menu put on the shopping lists, and what did not make it. */
export class WeeklyMenuShoppingCard extends LitElement {
  static override properties = {
    hass: { attribute: false },
    _config: { state: true },
    _busy: { state: true },
    _error: { state: true },
  };
  static override styles = cardStyles;

  declare hass: HomeAssistant;
  declare _config: ShoppingCardConfig;
  declare _busy: boolean;
  declare _error: string;

  constructor() {
    super();
    this._config = { type: "custom:weeklymenu-shopping-card" };
    this._busy = false;
    this._error = "";
  }

  static getConfigElement(): HTMLElement {
    return document.createElement("weeklymenu-shopping-card-editor");
  }

  static getStubConfig(): Partial<ShoppingCardConfig> {
    return {};
  }

  setConfig(config: ShoppingCardConfig): void {
    if (!config) throw new Error("Invalid configuration");
    this._config = { show_added: true, show_skipped: false, ...config };
  }

  getCardSize(): number {
    return 4;
  }

  private async _retry(): Promise<void> {
    this._busy = true;
    this._error = "";
    try {
      await this.hass.callService(DOMAIN, "add_to_shopping", {});
    } catch (err) {
      this._error = errorMessage(err);
    } finally {
      this._busy = false;
    }
  }

  protected override render(): TemplateResult {
    if (!this.hass) return html``;
    const hass = this.hass;
    const shop = readShopping(hass);
    const header = this._config.title ?? t(hass, "shoppingTitle");
    if (!shop.hasResult) {
      return html`<ha-card .header=${header}><div class="empty">${t(hass, "shopNothing")}</div></ha-card>`;
    }
    const retryable = shop.counts.failed + shop.counts.pending;
    // "reauth_required" only says a sign-in failed; skip it when a store already says which
    const named = shop.errors.some((e) => e.endsWith(": auth_failed"));
    const errors = [
      ...new Set(shop.errors.filter((e) => !(named && e === "reauth_required")).map((e) => shoppingError(hass, e))),
    ];

    return html`<ha-card .header=${header}>
      <div class="head">
        <span>
          ${shop.weekStart ? t(hass, "week", { n: isoWeek(shop.weekStart) }) : ""}
          ${shop.targets.length ? ` · ${t(hass, "shopTargets", { targets: shop.targets.join(", ") })}` : ""}
        </span>
      </div>
      <div class="head chips">
        ${GROUPS.filter((g) => shop.counts[g.key] > 0).map(
          (g) => html`<span class="chip ${g.css === "warning" ? "draft" : ""}">${t(hass, g.label)}: ${shop.counts[g.key]}</span>`,
        )}
      </div>
      ${errors.map((text) => html`<div class="banner warning">${text}</div>`)}
      ${this._error ? html`<div class="banner error">${t(hass, "error", { error: this._error })}</div>` : nothing}
      ${GROUPS.map((g) => this._renderGroup(g, shop[g.key]))}
      ${retryable
        ? html`<div class="foot">
            <button class="primary" ?disabled=${this._busy} @click=${() => this._retry()}>${t(hass, "shopRetry")}</button>
          </div>`
        : nothing}
    </ha-card>`;
  }

  private _renderGroup(group: (typeof GROUPS)[number], items: string[]): TemplateResult | typeof nothing {
    if (!items.length) return nothing;
    if (group.key === "added" && this._config.show_added === false) return nothing;
    if (group.key === "skipped" && !this._config.show_skipped) return nothing;
    // what needs attention is open; the long, settled lists are folded away
    const open = group.key === "review" || group.key === "failed" || group.key === "pending";
    return html`<details class="group ${group.css}" ?open=${open}>
      <summary>${t(this.hass, group.label)} (${items.length})</summary>
      <ul>
        ${items.map((item) => html`<li>${item}</li>`)}
      </ul>
    </details>`;
  }
}
