import { html, nothing, type TemplateResult } from "lit";
import { percent } from "./data";
import { t, tagLabel, type Key } from "./i18n";
import type { Dinner, HomeAssistant, SplitGroup } from "./types";

/** Time, tags and where the recipe came from. */
export function renderMeta(hass: HomeAssistant, dinner: Dinner): TemplateResult {
  const sourceKey = `source_${dinner.source}` as Key;
  const source = dinner.source ? t(hass, sourceKey) : "";
  return html`<div class="meta">
    ${dinner.totalTime ? html`<span>${t(hass, "minutes", { n: dinner.totalTime })}</span>` : nothing}
    ${dinner.tags.map((tag) => html`<span class="tag">${tagLabel(hass, tag)}</span>`)}
    ${source && !source.startsWith("source_") ? html`<span class="badge">${source}</span>` : nothing}
    ${dinner.split.length
      ? html`<span class="badge split" title=${t(hass, "split")}>${t(hass, "split")}</span>`
      : nothing}
    ${dinner.locked ? html`<span class="badge">${t(hass, "locked")}</span>` : nothing}
  </div>`;
}

/** Who gets what instead, and the clean-pan reminder where an allergy is involved. */
export function renderSplit(hass: HomeAssistant, groups: SplitGroup[]): TemplateResult | typeof nothing {
  if (!groups.length) return nothing;
  return html`<div class="split-note">
    <strong>${t(hass, "split")}</strong>
    ${groups.map(
      (group) => html`<div>
        ${group.swaps.map(
          (swap) =>
            html`<div>
              ${t(hass, "splitNote", {
                members: group.members.join(", ") + ` (${percent(group.share)})`,
                from: swap.original,
                to: swap.replacement,
              })}
            </div>`,
        )}
        ${group.separatePans ? html`<em>${t(hass, "cleanPans")}</em>` : nothing}
      </div>`,
    )}
  </div>`;
}

export function renderIngredients(hass: HomeAssistant, ingredients: string[]): TemplateResult | typeof nothing {
  if (!ingredients.length) return nothing;
  return html`<div>
    <h4>${t(hass, "ingredients")}</h4>
    <ul>
      ${ingredients.map((line) => html`<li>${line}</li>`)}
    </ul>
  </div>`;
}

export function errorMessage(err: unknown): string {
  if (err && typeof err === "object" && "message" in err) return String((err as { message: unknown }).message);
  return String(err);
}
