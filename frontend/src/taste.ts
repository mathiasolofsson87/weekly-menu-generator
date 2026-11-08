import { LitElement, html, nothing, type TemplateResult } from "lit";
import { DOMAIN, readFamily } from "./data";
import { t } from "./i18n";
import { errorMessage } from "./parts";
import { cardStyles } from "./styles";
import type { Alternative, Dinner, HomeAssistant, Member } from "./types";

/** The family member behind the logged-in Home Assistant user, through their linked person. */
export function currentMember(hass: HomeAssistant, members: Member[]): Member | undefined {
  const userId = hass.user?.id;
  if (!userId) return undefined;
  return members.find((m) => m.person && hass.states[m.person]?.attributes?.user_id === userId);
}

/** An option's text: a heart for a favorite and each member's stars, such as "♥ Gryta (Anna ★5, Bo ★2)". */
export function alternativeLabel(alt: Alternative, members: Member[]): string {
  const stars = members
    .filter((m) => alt.ratings[m.id])
    .map((m) => `${m.name} ★${alt.ratings[m.id]}`)
    .join(", ");
  return `${alt.favoriteOf.length ? "♥ " : ""}${alt.title}${stars ? ` (${stars})` : ""}`;
}

/** Favorites first, otherwise in the planner's order. */
export function favoritesFirst(alternatives: Alternative[]): Alternative[] {
  return [...alternatives].sort((a, b) => Number(b.favoriteOf.length > 0) - Number(a.favoriteOf.length > 0));
}

/** Stars and a heart for one dinner, for one family member. Calls rate_recipe and favorite_recipe. */
export class WeeklyMenuTaste extends LitElement {
  static override properties = {
    hass: { attribute: false },
    dinner: { attribute: false },
    _member: { state: true },
    _error: { state: true },
  };
  static override styles = cardStyles;

  declare hass: HomeAssistant;
  declare dinner: Dinner | undefined;
  declare _member: string;
  declare _error: string;

  constructor() {
    super();
    this._member = "";
    this._error = "";
  }

  private async _call(service: string, data: Record<string, unknown>): Promise<void> {
    this._error = "";
    try {
      await this.hass.callService(DOMAIN, service, data);
    } catch (err) {
      this._error = errorMessage(err);
    }
  }

  protected override render(): TemplateResult | typeof nothing {
    const dinner = this.dinner;
    if (!this.hass || !dinner?.recipeId) return nothing;
    const hass = this.hass;
    const members = readFamily(hass).members;
    if (!members.length) return nothing;
    const me = members.find((m) => m.id === this._member) ?? currentMember(hass, members) ?? members[0];
    const rating = dinner.ratings[me.id] ?? 0;
    const favorite = dinner.favoriteOf.includes(me.id);
    const names = dinner.favoriteOf.map((id) => members.find((m) => m.id === id)?.name).filter(Boolean);
    const starLabel = (n: number) => (n === 1 ? t(hass, "starOne") : t(hass, "starsN", { n }));
    return html`<div class="taste">
      ${members.length > 1
        ? html`<select
            aria-label=${t(hass, "rateAs")}
            .value=${me.id}
            @change=${(ev: Event) => (this._member = (ev.target as HTMLSelectElement).value)}
          >
            ${members.map((m) => html`<option value=${m.id} ?selected=${m.id === me.id}>${m.name}</option>`)}
          </select>`
        : nothing}
      <span class="stars" role="group" aria-label=${t(hass, "ratingGroup")}>
        ${[1, 2, 3, 4, 5].map(
          (n) => html`<button
            class="icon ${n <= rating ? "on" : ""}"
            title=${starLabel(n)}
            aria-label=${starLabel(n)}
            aria-pressed=${n === rating ? "true" : "false"}
            @click=${() =>
              void this._call("rate_recipe", { member: me.id, recipe_id: dinner.recipeId, rating: n === rating ? 0 : n })}
          >
            <ha-icon icon=${n <= rating ? "mdi:star" : "mdi:star-outline"}></ha-icon>
          </button>`,
        )}
      </span>
      <button
        class="icon heart ${favorite ? "on" : ""}"
        title=${favorite ? t(hass, "favoriteRemove") : t(hass, "favoriteAdd")}
        aria-label=${favorite ? t(hass, "favoriteRemove") : t(hass, "favoriteAdd")}
        aria-pressed=${favorite ? "true" : "false"}
        @click=${() => void this._call("favorite_recipe", { member: me.id, recipe_id: dinner.recipeId, favorite: !favorite })}
      >
        <ha-icon icon=${favorite ? "mdi:heart" : "mdi:heart-outline"}></ha-icon>
      </button>
      ${names.length ? html`<span class="liked">${t(hass, "favoriteOf", { names: names.join(", ") })}</span>` : nothing}
      ${this._error ? html`<span class="banner error">${t(hass, "error", { error: this._error })}</span>` : nothing}
    </div>`;
  }
}
