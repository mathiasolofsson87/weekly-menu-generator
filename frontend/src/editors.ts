import { LitElement, html, type TemplateResult } from "lit";
import { t, type Key } from "./i18n";
import type { HomeAssistant, LovelaceCardConfig } from "./types";

interface Field {
  name: string;
  selector: Record<string, unknown>;
}

/** A card editor built from Home Assistant's own form. */
abstract class CardEditor extends LitElement {
  static override properties = {
    hass: { attribute: false },
    _config: { state: true },
  };

  declare hass: HomeAssistant;
  declare _config: LovelaceCardConfig;

  protected abstract readonly fields: Field[];
  protected abstract readonly defaults: Record<string, unknown>;

  setConfig(config: LovelaceCardConfig): void {
    this._config = config;
  }

  private readonly _label = (field: { name: string }): string => t(this.hass, `editor_${field.name}` as Key);

  private _changed(ev: CustomEvent<{ value: LovelaceCardConfig }>): void {
    ev.stopPropagation();
    this.dispatchEvent(
      new CustomEvent("config-changed", {
        detail: { config: { ...this._config, ...ev.detail.value } },
        bubbles: true,
        composed: true,
      }),
    );
  }

  protected override render(): TemplateResult {
    if (!this.hass || !this._config) return html``;
    return html`<ha-form
      .hass=${this.hass}
      .data=${{ ...this.defaults, ...this._config }}
      .schema=${this.fields}
      .computeLabel=${this._label}
      @value-changed=${this._changed}
    ></ha-form>`;
  }
}

export class WeeklyMenuCardEditor extends CardEditor {
  protected readonly fields: Field[] = [
    { name: "title", selector: { text: {} } },
    { name: "show_images", selector: { boolean: {} } },
    { name: "show_actions", selector: { boolean: {} } },
  ];
  protected readonly defaults = { show_images: true, show_actions: true };
}

export class WeeklyMenuTodayCardEditor extends CardEditor {
  protected readonly fields: Field[] = [
    { name: "title", selector: { text: {} } },
    { name: "show_image", selector: { boolean: {} } },
    { name: "show_ingredients", selector: { boolean: {} } },
  ];
  protected readonly defaults = { show_image: true, show_ingredients: false };
}
