import { LitElement, html, nothing, type TemplateResult } from "lit";
import { DOMAIN, readFamily } from "./data";
import { weekdayShort } from "./format";
import { t, type Key } from "./i18n";
import { errorMessage } from "./parts";
import { cardStyles } from "./styles";
import { ALLERGENS, DIETS, PORTIONS, WEEKDAYS, type HomeAssistant, type LovelaceCardConfig, type Member } from "./types";

export interface FamilyCardConfig extends LovelaceCardConfig {
  title?: string;
  editable?: boolean;
}

/** What the form edits. `id` is empty for a new person. */
interface Draft {
  id: string;
  name: string;
  allergies: string[]; // the known allergens that are ticked
  otherAllergies: string; // free text, comma separated
  dislikes: string;
  likes: string;
  diet: string;
  portion: string;
  attends: string[];
  cookSeparately: boolean;
}

const KNOWN = new Set<string>(ALLERGENS);

const words = (text: string): string[] =>
  text
    .split(",")
    .map((w) => w.trim())
    .filter(Boolean);

function toDraft(member: Member | undefined, defaultDays: string[]): Draft {
  if (!member) {
    return {
      id: "",
      name: "",
      allergies: [],
      otherAllergies: "",
      dislikes: "",
      likes: "",
      diet: "omnivore",
      portion: "normal",
      attends: [...defaultDays],
      cookSeparately: true,
    };
  }
  return {
    id: member.id,
    name: member.name,
    allergies: member.allergies.filter((a) => KNOWN.has(a)),
    otherAllergies: member.allergies.filter((a) => !KNOWN.has(a)).join(", "),
    dislikes: member.dislikes.join(", "),
    likes: member.likes.join(", "),
    diet: member.diet,
    portion: member.portion,
    attends: [...member.attends],
    cookSeparately: member.cookSeparately,
  };
}

/** The people the menu is planned for. Editing calls the set_member and remove_member services. */
export class WeeklyMenuFamilyCard extends LitElement {
  static override properties = {
    hass: { attribute: false },
    _config: { state: true },
    _draft: { state: true },
    _busy: { state: true },
    _error: { state: true },
  };
  static override styles = cardStyles;

  declare hass: HomeAssistant;
  declare _config: FamilyCardConfig;
  declare _draft: Draft | null;
  declare _busy: boolean;
  declare _error: string;

  constructor() {
    super();
    this._config = { type: "custom:weeklymenu-family-card" };
    this._draft = null;
    this._busy = false;
    this._error = "";
  }

  static getConfigElement(): HTMLElement {
    return document.createElement("weeklymenu-family-card-editor");
  }

  static getStubConfig(): Partial<FamilyCardConfig> {
    return {};
  }

  setConfig(config: FamilyCardConfig): void {
    if (!config) throw new Error("Invalid configuration");
    this._config = { editable: true, ...config };
  }

  getCardSize(): number {
    return this.hass ? 2 + readFamily(this.hass).members.length : 3;
  }

  // --- actions ----------------------------------------------------------------------

  private _set(patch: Partial<Draft>): void {
    if (this._draft) this._draft = { ...this._draft, ...patch };
  }

  private _toggle(list: "allergies" | "attends", value: string): void {
    if (!this._draft) return;
    const current = this._draft[list];
    this._set({ [list]: current.includes(value) ? current.filter((v) => v !== value) : [...current, value] });
  }

  private async _run(service: string, data: Record<string, unknown>): Promise<boolean> {
    this._busy = true;
    this._error = "";
    try {
      await this.hass.callService(DOMAIN, service, data);
      return true;
    } catch (err) {
      this._error = errorMessage(err);
      return false;
    } finally {
      this._busy = false;
    }
  }

  private async _save(): Promise<void> {
    const draft = this._draft;
    if (!draft || !draft.name.trim() || !draft.attends.length) return;
    const data: Record<string, unknown> = {
      name: draft.name.trim(),
      allergies: [...draft.allergies, ...words(draft.otherAllergies)],
      dislikes: words(draft.dislikes),
      likes: words(draft.likes),
      diet: draft.diet,
      portion: draft.portion,
      attends: WEEKDAYS.filter((d) => draft.attends.includes(d)),
      cook_separately: draft.cookSeparately,
    };
    if (draft.id) data.id = draft.id;
    if (await this._run("set_member", data)) this._draft = null;
  }

  private async _remove(): Promise<void> {
    const draft = this._draft;
    if (!draft?.id || !window.confirm(t(this.hass, "famRemoveAsk", { name: draft.name }))) return;
    if (await this._run("remove_member", { id: draft.id })) this._draft = null;
  }

  // --- rendering --------------------------------------------------------------------------

  protected override render(): TemplateResult {
    if (!this.hass) return html``;
    const hass = this.hass;
    const family = readFamily(hass);
    const header = this._config.title ?? t(hass, "familyTitle");
    if (!family.available) {
      return html`<ha-card .header=${header}><div class="empty">${t(hass, "famNoFamily")}</div></ha-card>`;
    }
    const editable = this._config.editable !== false;
    const days = family.dinnerDays.length ? family.dinnerDays : [...WEEKDAYS];
    return html`<ha-card .header=${header}>
      ${this._error ? html`<div class="banner error">${t(hass, "error", { error: this._error })}</div>` : nothing}
      ${family.members.length
        ? family.members.map((m) => this._renderMember(m, family.dinnerDays, editable, days))
        : html`<div class="empty">${t(hass, "famNone")}</div>`}
      ${this._draft && !this._draft.id ? this._renderForm(this._draft, days) : nothing}
      ${editable && !this._draft
        ? html`<div class="foot">
            <button class="primary" ?disabled=${this._busy} @click=${() => (this._draft = toDraft(undefined, days))}>
              ${t(hass, "famAdd")}
            </button>
          </div>`
        : nothing}
    </ha-card>`;
  }

  private _renderMember(member: Member, dinnerDays: string[], editable: boolean, days: string[]): TemplateResult {
    const hass = this.hass;
    const editing = this._draft?.id === member.id;
    const attends = days.filter((d) => member.attends.includes(d));
    const every = attends.length === days.length;
    return html`<div class="member">
      <div class="main">
        <div style="flex:1;min-width:0">
          <div class="title">${member.name}</div>
          <div class="meta">
            ${member.diet !== "omnivore" ? html`<span class="badge">${t(hass, `diet_${member.diet}` as Key)}</span>` : nothing}
            ${member.portion !== "normal" ? html`<span class="badge">${t(hass, `portion_${member.portion}` as Key)}</span>` : nothing}
            ${member.allergies.map((a) => html`<span class="tag allergy">${KNOWN.has(a) ? t(hass, `allergen_${a}` as Key) : a}</span>`)}
            ${member.dislikes.length ? html`<span>${member.dislikes.join(", ")}</span>` : nothing}
            <span>${every ? t(hass, "famEveryDay") : attends.map((d) => weekdayShort(hass, d)).join(", ")}</span>
          </div>
        </div>
        ${editable && !editing
          ? html`<button ?disabled=${this._busy} @click=${() => (this._draft = toDraft(member, dinnerDays))}>
              ${t(hass, "famEdit")}
            </button>`
          : nothing}
      </div>
      ${editing && this._draft ? this._renderForm(this._draft, days) : nothing}
    </div>`;
  }

  private _renderForm(draft: Draft, days: string[]): TemplateResult {
    const hass = this.hass;
    const valid = draft.name.trim() !== "" && draft.attends.length > 0;
    const text = (label: Key, value: string, key: keyof Draft) => html`<label class="field">
      <span>${t(hass, label)}</span>
      <input
        type="text"
        .value=${value}
        @input=${(ev: Event) => this._set({ [key]: (ev.target as HTMLInputElement).value })}
      />
    </label>`;
    return html`<form class="form" @submit=${(ev: Event) => ev.preventDefault()}>
      ${text("famName", draft.name, "name")}
      <fieldset>
        <legend>${t(hass, "famAllergies")}</legend>
        <div class="checks">
          ${ALLERGENS.map(
            (a) => html`<label class="check">
              <input type="checkbox" .checked=${draft.allergies.includes(a)} @change=${() => this._toggle("allergies", a)} />
              ${t(hass, `allergen_${a}` as Key)}
            </label>`,
          )}
        </div>
      </fieldset>
      ${text("famOtherAllergies", draft.otherAllergies, "otherAllergies")} ${text("famDislikes", draft.dislikes, "dislikes")}
      ${text("famLikes", draft.likes, "likes")}
      <div class="row">
        <label class="field">
          <span>${t(hass, "famDiet")}</span>
          <select .value=${draft.diet} @change=${(ev: Event) => this._set({ diet: (ev.target as HTMLSelectElement).value })}>
            ${DIETS.map((d) => html`<option value=${d} ?selected=${draft.diet === d}>${t(hass, `diet_${d}` as Key)}</option>`)}
          </select>
        </label>
        <label class="field">
          <span>${t(hass, "famPortion")}</span>
          <select .value=${draft.portion} @change=${(ev: Event) => this._set({ portion: (ev.target as HTMLSelectElement).value })}>
            ${PORTIONS.map((p) => html`<option value=${p} ?selected=${draft.portion === p}>${t(hass, `portion_${p}` as Key)}</option>`)}
          </select>
        </label>
      </div>
      <fieldset>
        <legend>${t(hass, "famDays")}</legend>
        <div class="checks">
          ${days.map(
            (d) => html`<label class="check">
              <input type="checkbox" .checked=${draft.attends.includes(d)} @change=${() => this._toggle("attends", d)} />
              ${weekdayShort(hass, d)}
            </label>`,
          )}
        </div>
        ${draft.attends.length ? nothing : html`<small class="hint-error">${t(hass, "famNoDays")}</small>`}
      </fieldset>
      <label class="check">
        <input
          type="checkbox"
          .checked=${draft.cookSeparately}
          @change=${(ev: Event) => this._set({ cookSeparately: (ev.target as HTMLInputElement).checked })}
        />
        ${t(hass, "famCookSeparately")}
      </label>
      <small>${t(hass, "famAppliesLater")}</small>
      <div class="row">
        <button class="primary" type="button" ?disabled=${this._busy || !valid} @click=${() => this._save()}>${t(hass, "famSave")}</button>
        <button type="button" ?disabled=${this._busy} @click=${() => (this._draft = null)}>${t(hass, "famCancel")}</button>
        ${draft.id
          ? html`<button type="button" ?disabled=${this._busy} @click=${() => this._remove()}>${t(hass, "famRemove")}</button>`
          : nothing}
      </div>
    </form>`;
  }
}
