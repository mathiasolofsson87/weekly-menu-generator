const M = {
  en: {
    menuTitle: "Weekly menu",
    todayTitle: "Tonight's dinner",
    week: "Week {n}",
    status_none: "No menu",
    status_draft: "Draft",
    status_confirmed: "Confirmed",
    noMenu: "There is no menu yet.",
    noDinner: "No dinner is planned for today.",
    generate: "Generate menu",
    regenerateAll: "Regenerate all",
    confirm: "Confirm",
    confirmAsk: "Confirm this menu? It can't be changed afterwards.",
    confirmedNote: "The menu is confirmed and can't be changed.",
    newDinner: "New dinner",
    hint: "Wish (optional)",
    lock: "Lock",
    unlock: "Unlock",
    locked: "Locked",
    show: "Show details",
    hide: "Hide details",
    alternatives: "Other options",
    choose: "Choose…",
    swapWith: "Swap with…",
    ingredients: "Ingredients",
    minutes: "{n} min",
    openRecipe: "Open recipe",
    working: "Working…",
    error: "Something went wrong: {error}",
    split: "Cooked in more than one version",
    splitNote: "{members}: {from} → {to}",
    cleanPans: "Use a clean pan and utensils.",
    source_ica: "ICA",
    source_ai_task: "AI",
    tag_quick: "Quick",
    tag_easy: "Easy",
    tag_fancy: "Fancy",
    tag_family_friendly: "Family friendly",
    tag_budget: "Budget",
    tag_vegetarian: "Vegetarian",
    tag_fish: "Fish",
    warn_no_recipe: "No recipe was found for {detail}.",
    warn_source_failed: "The recipe source {detail} did not work.",
    warn_no_sources: "No recipe sources are active or set up.",
    warn_no_days: "There are no dinner days to plan.",
    warn_split_limit_exceeded: "{detail} is cooked in several versions beyond your limit.",
    editor_title: "Title",
    editor_show_images: "Show pictures",
    editor_show_actions: "Show buttons for changing the menu",
    editor_show_ingredients: "Show ingredients",
    editor_show_image: "Show picture",
    cardMenuName: "Weekly menu",
    cardMenuDescription: "The week's dinners, with buttons to regenerate, lock, swap and confirm.",
    cardTodayName: "Tonight's dinner",
    cardTodayDescription: "Today's dinner, compact.",
    shoppingTitle: "Shopping",
    shopNothing: "Nothing has been bought yet. Confirm a menu to build the list.",
    shopTargets: "To: {targets}",
    shopAdded: "Added",
    shopReview: "Needs a look",
    shopFailed: "Not delivered",
    shopPending: "Waiting",
    shopSkipped: "Pantry (not bought)",
    shopRetry: "Try again",
    err_reauth_required: "A sign-in no longer works. Sign in again under Settings.",
    err_no_targets: "No shopping list is set up.",
    err_no_review_list: "Items that could not be placed had no review list to go to.",
    err_auth_failed: "The sign-in to {store} no longer works. Sign in again under Settings.",
    err_geo_blocked: "{store} only answers connections from Sweden.",
    familyTitle: "Family",
    famNoFamily: "The family is not available yet.",
    famNone: "Nobody has been added yet.",
    famAdd: "Add person",
    famEdit: "Edit",
    famSave: "Save",
    famCancel: "Cancel",
    famRemove: "Remove",
    famRemoveAsk: "Remove {name}?",
    famName: "Name",
    famAllergies: "Allergies",
    famOtherAllergies: "Other allergies (separate with commas)",
    famDislikes: "Dislikes (separate with commas)",
    famLikes: "Likes (separate with commas)",
    famDiet: "Diet",
    famPortion: "Portion size",
    famDays: "Eats dinner on",
    famNoDays: "Pick at least one day.",
    famCookSeparately: "Allergens can be cooked separately (turn off for severe allergies)",
    famAppliesLater: "Changes apply to menus made from now on.",
    famEveryDay: "Every dinner",
    allergen_gluten: "Gluten",
    allergen_milk: "Milk",
    allergen_lactose: "Lactose",
    allergen_egg: "Egg",
    allergen_fish: "Fish",
    allergen_crustaceans: "Crustaceans",
    allergen_molluscs: "Molluscs",
    allergen_peanuts: "Peanuts",
    allergen_tree_nuts: "Tree nuts",
    allergen_soy: "Soy",
    allergen_sesame: "Sesame",
    allergen_celery: "Celery",
    allergen_mustard: "Mustard",
    allergen_lupin: "Lupin",
    allergen_sulphites: "Sulphites",
    diet_omnivore: "Eats everything",
    diet_vegetarian: "Vegetarian",
    diet_vegan: "Vegan",
    diet_pescatarian: "Pescatarian",
    portion_small: "Small",
    portion_normal: "Normal",
    portion_large: "Large",
    editor_show_added: "List the added items",
    editor_show_skipped: "List the skipped pantry items",
    editor_editable: "Allow editing",
    cardShoppingName: "Shopping result",
    cardShoppingDescription: "What was put on the shopping lists, what needs a look and what failed.",
    cardFamilyName: "Family",
    cardFamilyDescription: "The people the menu is planned for, with their allergies and preferences."
  },
  sv: {
    menuTitle: "Veckomeny",
    todayTitle: "Kvällens middag",
    week: "Vecka {n}",
    status_none: "Ingen meny",
    status_draft: "Utkast",
    status_confirmed: "Bekräftad",
    noMenu: "Det finns ingen meny än.",
    noDinner: "Ingen middag är planerad idag.",
    generate: "Skapa meny",
    regenerateAll: "Skapa om allt",
    confirm: "Bekräfta",
    confirmAsk: "Bekräfta menyn? Den kan inte ändras efteråt.",
    confirmedNote: "Menyn är bekräftad och kan inte ändras.",
    newDinner: "Byt middag",
    hint: "Önskemål (valfritt)",
    lock: "Lås",
    unlock: "Lås upp",
    locked: "Låst",
    show: "Visa detaljer",
    hide: "Dölj detaljer",
    alternatives: "Andra förslag",
    choose: "Välj…",
    swapWith: "Byt plats med…",
    ingredients: "Ingredienser",
    minutes: "{n} min",
    openRecipe: "Öppna recept",
    working: "Arbetar…",
    error: "Något gick fel: {error}",
    split: "Lagas i flera versioner",
    splitNote: "{members}: {from} → {to}",
    cleanPans: "Använd rena pannor och redskap.",
    source_ica: "ICA",
    source_ai_task: "AI",
    tag_quick: "Snabbt",
    tag_easy: "Enkelt",
    tag_fancy: "Festligt",
    tag_family_friendly: "Barnvänligt",
    tag_budget: "Billigt",
    tag_vegetarian: "Vegetariskt",
    tag_fish: "Fisk",
    warn_no_recipe: "Inget recept hittades för {detail}.",
    warn_source_failed: "Receptkällan {detail} fungerade inte.",
    warn_no_sources: "Inga receptkällor är aktiva eller inställda.",
    warn_no_days: "Inga middagsdagar att planera.",
    warn_split_limit_exceeded: "{detail} lagas i flera versioner trots din gräns.",
    editor_title: "Rubrik",
    editor_show_images: "Visa bilder",
    editor_show_actions: "Visa knappar för att ändra menyn",
    editor_show_ingredients: "Visa ingredienser",
    editor_show_image: "Visa bild",
    cardMenuName: "Veckomeny",
    cardMenuDescription: "Veckans middagar, med knappar för att skapa om, låsa, byta plats och bekräfta.",
    cardTodayName: "Kvällens middag",
    cardTodayDescription: "Dagens middag, kompakt.",
    shoppingTitle: "Inköp",
    shopNothing: "Inget har handlats än. Bekräfta en meny för att bygga listan.",
    shopTargets: "Till: {targets}",
    shopAdded: "Tillagda",
    shopReview: "Behöver granskas",
    shopFailed: "Inte levererade",
    shopPending: "Väntar",
    shopSkipped: "Skafferi (köps inte)",
    shopRetry: "Försök igen",
    err_reauth_required: "En inloggning fungerar inte längre. Logga in igen under Inställningar.",
    err_no_targets: "Ingen inköpslista är inställd.",
    err_no_review_list: "Varor som inte kunde placeras hade ingen granskningslista att hamna på.",
    err_auth_failed: "Inloggningen till {store} fungerar inte längre. Logga in igen under Inställningar.",
    err_geo_blocked: "{store} svarar bara på anslutningar från Sverige.",
    familyTitle: "Familj",
    famNoFamily: "Familjen är inte tillgänglig än.",
    famNone: "Ingen har lagts till än.",
    famAdd: "Lägg till person",
    famEdit: "Ändra",
    famSave: "Spara",
    famCancel: "Avbryt",
    famRemove: "Ta bort",
    famRemoveAsk: "Ta bort {name}?",
    famName: "Namn",
    famAllergies: "Allergier",
    famOtherAllergies: "Andra allergier (separera med kommatecken)",
    famDislikes: "Ogillar (separera med kommatecken)",
    famLikes: "Gillar (separera med kommatecken)",
    famDiet: "Kost",
    famPortion: "Portionsstorlek",
    famDays: "Äter middag på",
    famNoDays: "Välj minst en dag.",
    famCookSeparately: "Allergener kan lagas separat (stäng av vid svåra allergier)",
    famAppliesLater: "Ändringar gäller menyer som skapas från nu.",
    famEveryDay: "Alla middagar",
    allergen_gluten: "Gluten",
    allergen_milk: "Mjölk",
    allergen_lactose: "Laktos",
    allergen_egg: "Ägg",
    allergen_fish: "Fisk",
    allergen_crustaceans: "Kräftdjur",
    allergen_molluscs: "Blötdjur",
    allergen_peanuts: "Jordnötter",
    allergen_tree_nuts: "Trädnötter",
    allergen_soy: "Soja",
    allergen_sesame: "Sesam",
    allergen_celery: "Selleri",
    allergen_mustard: "Senap",
    allergen_lupin: "Lupin",
    allergen_sulphites: "Sulfiter",
    diet_omnivore: "Äter allt",
    diet_vegetarian: "Vegetarian",
    diet_vegan: "Vegan",
    diet_pescatarian: "Pescetarian",
    portion_small: "Liten",
    portion_normal: "Normal",
    portion_large: "Stor",
    editor_show_added: "Lista de tillagda varorna",
    editor_show_skipped: "Lista de överhoppade skafferivarorna",
    editor_editable: "Tillåt ändringar",
    cardShoppingName: "Inköpsresultat",
    cardShoppingDescription: "Vad som lades på inköpslistorna, vad som behöver granskas och vad som misslyckades.",
    cardFamilyName: "Familj",
    cardFamilyDescription: "Personerna menyn planeras för, med allergier och önskemål."
  }
};
function H(r) {
  return (r?.locale?.language ?? r?.language ?? "en").slice(0, 2) === "sv" ? "sv" : "en";
}
function o(r, e, t = {}) {
  return (M[H(r)][e] ?? M.en[e]).replace(/\{(\w+)\}/g, (i, a) => String(t[a] ?? `{${a}}`));
}
function Ue(r, e, t) {
  const [s, i = ""] = e.split(":"), a = `warn_${s}`;
  if (!(a in M.en)) return e;
  const n = s === "no_recipe" || s === "split_limit_exceeded" ? t(i) : i;
  return o(r, a, { detail: n });
}
function Oe(r, e) {
  const t = `tag_${e}`;
  return t in M.en ? o(r, t) : e.replace(/_/g, " ");
}
function Ie(r, e) {
  const [t, s] = e.includes(": ") ? e.split(": ", 2) : ["", e], i = `err_${s}`;
  return i in M.en ? o(r, i, { store: t.toUpperCase() }) : e;
}
/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const j = globalThis, ee = j.ShadowRoot && (j.ShadyCSS === void 0 || j.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, te = Symbol(), ne = /* @__PURE__ */ new WeakMap();
let be = class {
  constructor(e, t, s) {
    if (this._$cssResult$ = !0, s !== te) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = e, this.t = t;
  }
  get styleSheet() {
    let e = this.o;
    const t = this.t;
    if (ee && e === void 0) {
      const s = t !== void 0 && t.length === 1;
      s && (e = ne.get(t)), e === void 0 && ((this.o = e = new CSSStyleSheet()).replaceSync(this.cssText), s && ne.set(t, e));
    }
    return e;
  }
  toString() {
    return this.cssText;
  }
};
const Le = (r) => new be(typeof r == "string" ? r : r + "", void 0, te), je = (r, ...e) => {
  const t = r.length === 1 ? r[0] : e.reduce((s, i, a) => s + ((n) => {
    if (n._$cssResult$ === !0) return n.cssText;
    if (typeof n == "number") return n;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + n + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(i) + r[a + 1], r[0]);
  return new be(t, r, te);
}, Fe = (r, e) => {
  if (ee) r.adoptedStyleSheets = e.map((t) => t instanceof CSSStyleSheet ? t : t.styleSheet);
  else for (const t of e) {
    const s = document.createElement("style"), i = j.litNonce;
    i !== void 0 && s.setAttribute("nonce", i), s.textContent = t.cssText, r.appendChild(s);
  }
}, oe = ee ? (r) => r : (r) => r instanceof CSSStyleSheet ? ((e) => {
  let t = "";
  for (const s of e.cssRules) t += s.cssText;
  return Le(t);
})(r) : r;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: He, defineProperty: ze, getOwnPropertyDescriptor: We, getOwnPropertyNames: Ve, getOwnPropertySymbols: Be, getPrototypeOf: qe } = Object, z = globalThis, le = z.trustedTypes, Ke = le ? le.emptyScript : "", Ge = z.reactiveElementPolyfillSupport, P = (r, e) => r, J = { toAttribute(r, e) {
  switch (e) {
    case Boolean:
      r = r ? Ke : null;
      break;
    case Object:
    case Array:
      r = r == null ? r : JSON.stringify(r);
  }
  return r;
}, fromAttribute(r, e) {
  let t = r;
  switch (e) {
    case Boolean:
      t = r !== null;
      break;
    case Number:
      t = r === null ? null : Number(r);
      break;
    case Object:
    case Array:
      try {
        t = JSON.parse(r);
      } catch {
        t = null;
      }
  }
  return t;
} }, ke = (r, e) => !He(r, e), de = { attribute: !0, type: String, converter: J, reflect: !1, useDefault: !1, hasChanged: ke };
Symbol.metadata ??= Symbol("metadata"), z.litPropertyMetadata ??= /* @__PURE__ */ new WeakMap();
let C = class extends HTMLElement {
  static addInitializer(e) {
    this._$Ei(), (this.l ??= []).push(e);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(e, t = de) {
    if (t.state && (t.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(e) && ((t = Object.create(t)).wrapped = !0), this.elementProperties.set(e, t), !t.noAccessor) {
      const s = Symbol(), i = this.getPropertyDescriptor(e, s, t);
      i !== void 0 && ze(this.prototype, e, i);
    }
  }
  static getPropertyDescriptor(e, t, s) {
    const { get: i, set: a } = We(this.prototype, e) ?? { get() {
      return this[t];
    }, set(n) {
      this[t] = n;
    } };
    return { get: i, set(n) {
      const c = i?.call(this);
      a?.call(this, n), this.requestUpdate(e, c, s);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(e) {
    return this.elementProperties.get(e) ?? de;
  }
  static _$Ei() {
    if (this.hasOwnProperty(P("elementProperties"))) return;
    const e = qe(this);
    e.finalize(), e.l !== void 0 && (this.l = [...e.l]), this.elementProperties = new Map(e.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(P("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(P("properties"))) {
      const t = this.properties, s = [...Ve(t), ...Be(t)];
      for (const i of s) this.createProperty(i, t[i]);
    }
    const e = this[Symbol.metadata];
    if (e !== null) {
      const t = litPropertyMetadata.get(e);
      if (t !== void 0) for (const [s, i] of t) this.elementProperties.set(s, i);
    }
    this._$Eh = /* @__PURE__ */ new Map();
    for (const [t, s] of this.elementProperties) {
      const i = this._$Eu(t, s);
      i !== void 0 && this._$Eh.set(i, t);
    }
    this.elementStyles = this.finalizeStyles(this.styles);
  }
  static finalizeStyles(e) {
    const t = [];
    if (Array.isArray(e)) {
      const s = new Set(e.flat(1 / 0).reverse());
      for (const i of s) t.unshift(oe(i));
    } else e !== void 0 && t.push(oe(e));
    return t;
  }
  static _$Eu(e, t) {
    const s = t.attribute;
    return s === !1 ? void 0 : typeof s == "string" ? s : typeof e == "string" ? e.toLowerCase() : void 0;
  }
  constructor() {
    super(), this._$Ep = void 0, this.isUpdatePending = !1, this.hasUpdated = !1, this._$Em = null, this._$Ev();
  }
  _$Ev() {
    this._$ES = new Promise((e) => this.enableUpdating = e), this._$AL = /* @__PURE__ */ new Map(), this._$E_(), this.requestUpdate(), this.constructor.l?.forEach((e) => e(this));
  }
  addController(e) {
    (this._$EO ??= /* @__PURE__ */ new Set()).add(e), this.renderRoot !== void 0 && this.isConnected && e.hostConnected?.();
  }
  removeController(e) {
    this._$EO?.delete(e);
  }
  _$E_() {
    const e = /* @__PURE__ */ new Map(), t = this.constructor.elementProperties;
    for (const s of t.keys()) this.hasOwnProperty(s) && (e.set(s, this[s]), delete this[s]);
    e.size > 0 && (this._$Ep = e);
  }
  createRenderRoot() {
    const e = this.shadowRoot ?? this.attachShadow(this.constructor.shadowRootOptions);
    return Fe(e, this.constructor.elementStyles), e;
  }
  connectedCallback() {
    this.renderRoot ??= this.createRenderRoot(), this.enableUpdating(!0), this._$EO?.forEach((e) => e.hostConnected?.());
  }
  enableUpdating(e) {
  }
  disconnectedCallback() {
    this._$EO?.forEach((e) => e.hostDisconnected?.());
  }
  attributeChangedCallback(e, t, s) {
    this._$AK(e, s);
  }
  _$ET(e, t) {
    const s = this.constructor.elementProperties.get(e), i = this.constructor._$Eu(e, s);
    if (i !== void 0 && s.reflect === !0) {
      const a = (s.converter?.toAttribute !== void 0 ? s.converter : J).toAttribute(t, s.type);
      this._$Em = e, a == null ? this.removeAttribute(i) : this.setAttribute(i, a), this._$Em = null;
    }
  }
  _$AK(e, t) {
    const s = this.constructor, i = s._$Eh.get(e);
    if (i !== void 0 && this._$Em !== i) {
      const a = s.getPropertyOptions(i), n = typeof a.converter == "function" ? { fromAttribute: a.converter } : a.converter?.fromAttribute !== void 0 ? a.converter : J;
      this._$Em = i;
      const c = n.fromAttribute(t, a.type);
      this[i] = c ?? this._$Ej?.get(i) ?? c, this._$Em = null;
    }
  }
  requestUpdate(e, t, s, i = !1, a) {
    if (e !== void 0) {
      const n = this.constructor;
      if (i === !1 && (a = this[e]), s ??= n.getPropertyOptions(e), !((s.hasChanged ?? ke)(a, t) || s.useDefault && s.reflect && a === this._$Ej?.get(e) && !this.hasAttribute(n._$Eu(e, s)))) return;
      this.C(e, t, s);
    }
    this.isUpdatePending === !1 && (this._$ES = this._$EP());
  }
  C(e, t, { useDefault: s, reflect: i, wrapped: a }, n) {
    s && !(this._$Ej ??= /* @__PURE__ */ new Map()).has(e) && (this._$Ej.set(e, n ?? t ?? this[e]), a !== !0 || n !== void 0) || (this._$AL.has(e) || (this.hasUpdated || s || (t = void 0), this._$AL.set(e, t)), i === !0 && this._$Em !== e && (this._$Eq ??= /* @__PURE__ */ new Set()).add(e));
  }
  async _$EP() {
    this.isUpdatePending = !0;
    try {
      await this._$ES;
    } catch (t) {
      Promise.reject(t);
    }
    const e = this.scheduleUpdate();
    return e != null && await e, !this.isUpdatePending;
  }
  scheduleUpdate() {
    return this.performUpdate();
  }
  performUpdate() {
    if (!this.isUpdatePending) return;
    if (!this.hasUpdated) {
      if (this.renderRoot ??= this.createRenderRoot(), this._$Ep) {
        for (const [i, a] of this._$Ep) this[i] = a;
        this._$Ep = void 0;
      }
      const s = this.constructor.elementProperties;
      if (s.size > 0) for (const [i, a] of s) {
        const { wrapped: n } = a, c = this[i];
        n !== !0 || this._$AL.has(i) || c === void 0 || this.C(i, void 0, a, c);
      }
    }
    let e = !1;
    const t = this._$AL;
    try {
      e = this.shouldUpdate(t), e ? (this.willUpdate(t), this._$EO?.forEach((s) => s.hostUpdate?.()), this.update(t)) : this._$EM();
    } catch (s) {
      throw e = !1, this._$EM(), s;
    }
    e && this._$AE(t);
  }
  willUpdate(e) {
  }
  _$AE(e) {
    this._$EO?.forEach((t) => t.hostUpdated?.()), this.hasUpdated || (this.hasUpdated = !0, this.firstUpdated(e)), this.updated(e);
  }
  _$EM() {
    this._$AL = /* @__PURE__ */ new Map(), this.isUpdatePending = !1;
  }
  get updateComplete() {
    return this.getUpdateComplete();
  }
  getUpdateComplete() {
    return this._$ES;
  }
  shouldUpdate(e) {
    return !0;
  }
  update(e) {
    this._$Eq &&= this._$Eq.forEach((t) => this._$ET(t, this[t])), this._$EM();
  }
  updated(e) {
  }
  firstUpdated(e) {
  }
};
C.elementStyles = [], C.shadowRootOptions = { mode: "open" }, C[P("elementProperties")] = /* @__PURE__ */ new Map(), C[P("finalized")] = /* @__PURE__ */ new Map(), Ge?.({ ReactiveElement: C }), (z.reactiveElementVersions ??= []).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const se = globalThis, ce = (r) => r, F = se.trustedTypes, he = F ? F.createPolicy("lit-html", { createHTML: (r) => r }) : void 0, xe = "$lit$", w = `lit$${Math.random().toFixed(9).slice(2)}$`, Ae = "?" + w, Ze = `<${Ae}>`, E = document, R = () => E.createComment(""), U = (r) => r === null || typeof r != "object" && typeof r != "function", ie = Array.isArray, Je = (r) => ie(r) || typeof r?.[Symbol.iterator] == "function", G = `[ 	
\f\r]`, D = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, pe = /-->/g, ue = />/g, x = RegExp(`>|${G}(?:([^\\s"'>=/]+)(${G}*=${G}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`, "g"), ge = /'/g, me = /"/g, Se = /^(?:script|style|textarea|title)$/i, Ye = (r) => (e, ...t) => ({ _$litType$: r, strings: e, values: t }), l = Ye(1), T = Symbol.for("lit-noChange"), d = Symbol.for("lit-nothing"), fe = /* @__PURE__ */ new WeakMap(), A = E.createTreeWalker(E, 129);
function Ee(r, e) {
  if (!ie(r) || !r.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return he !== void 0 ? he.createHTML(e) : e;
}
const Qe = (r, e) => {
  const t = r.length - 1, s = [];
  let i, a = e === 2 ? "<svg>" : e === 3 ? "<math>" : "", n = D;
  for (let c = 0; c < t; c++) {
    const h = r[c];
    let p, g, u = -1, _ = 0;
    for (; _ < h.length && (n.lastIndex = _, g = n.exec(h), g !== null); ) _ = n.lastIndex, n === D ? g[1] === "!--" ? n = pe : g[1] !== void 0 ? n = ue : g[2] !== void 0 ? (Se.test(g[2]) && (i = RegExp("</" + g[2], "g")), n = x) : g[3] !== void 0 && (n = x) : n === x ? g[0] === ">" ? (n = i ?? D, u = -1) : g[1] === void 0 ? u = -2 : (u = n.lastIndex - g[2].length, p = g[1], n = g[3] === void 0 ? x : g[3] === '"' ? me : ge) : n === me || n === ge ? n = x : n === pe || n === ue ? n = D : (n = x, i = void 0);
    const y = n === x && r[c + 1].startsWith("/>") ? " " : "";
    a += n === D ? h + Ze : u >= 0 ? (s.push(p), h.slice(0, u) + xe + h.slice(u) + w + y) : h + w + (u === -2 ? c : y);
  }
  return [Ee(r, a + (r[t] || "<?>") + (e === 2 ? "</svg>" : e === 3 ? "</math>" : "")), s];
};
class O {
  constructor({ strings: e, _$litType$: t }, s) {
    let i;
    this.parts = [];
    let a = 0, n = 0;
    const c = e.length - 1, h = this.parts, [p, g] = Qe(e, t);
    if (this.el = O.createElement(p, s), A.currentNode = this.el.content, t === 2 || t === 3) {
      const u = this.el.content.firstChild;
      u.replaceWith(...u.childNodes);
    }
    for (; (i = A.nextNode()) !== null && h.length < c; ) {
      if (i.nodeType === 1) {
        if (i.hasAttributes()) for (const u of i.getAttributeNames()) if (u.endsWith(xe)) {
          const _ = g[n++], y = i.getAttribute(u).split(w), L = /([.?@])?(.*)/.exec(_);
          h.push({ type: 1, index: a, name: L[2], strings: y, ctor: L[1] === "." ? et : L[1] === "?" ? tt : L[1] === "@" ? st : W }), i.removeAttribute(u);
        } else u.startsWith(w) && (h.push({ type: 6, index: a }), i.removeAttribute(u));
        if (Se.test(i.tagName)) {
          const u = i.textContent.split(w), _ = u.length - 1;
          if (_ > 0) {
            i.textContent = F ? F.emptyScript : "";
            for (let y = 0; y < _; y++) i.append(u[y], R()), A.nextNode(), h.push({ type: 2, index: ++a });
            i.append(u[_], R());
          }
        }
      } else if (i.nodeType === 8) if (i.data === Ae) h.push({ type: 2, index: a });
      else {
        let u = -1;
        for (; (u = i.data.indexOf(w, u + 1)) !== -1; ) h.push({ type: 7, index: a }), u += w.length - 1;
      }
      a++;
    }
  }
  static createElement(e, t) {
    const s = E.createElement("template");
    return s.innerHTML = e, s;
  }
}
function N(r, e, t = r, s) {
  if (e === T) return e;
  let i = s !== void 0 ? t._$Co?.[s] : t._$Cl;
  const a = U(e) ? void 0 : e._$litDirective$;
  return i?.constructor !== a && (i?._$AO?.(!1), a === void 0 ? i = void 0 : (i = new a(r), i._$AT(r, t, s)), s !== void 0 ? (t._$Co ??= [])[s] = i : t._$Cl = i), i !== void 0 && (e = N(r, i._$AS(r, e.values), i, s)), e;
}
class Xe {
  constructor(e, t) {
    this._$AV = [], this._$AN = void 0, this._$AD = e, this._$AM = t;
  }
  get parentNode() {
    return this._$AM.parentNode;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  u(e) {
    const { el: { content: t }, parts: s } = this._$AD, i = (e?.creationScope ?? E).importNode(t, !0);
    A.currentNode = i;
    let a = A.nextNode(), n = 0, c = 0, h = s[0];
    for (; h !== void 0; ) {
      if (n === h.index) {
        let p;
        h.type === 2 ? p = new I(a, a.nextSibling, this, e) : h.type === 1 ? p = new h.ctor(a, h.name, h.strings, this, e) : h.type === 6 && (p = new it(a, this, e)), this._$AV.push(p), h = s[++c];
      }
      n !== h?.index && (a = A.nextNode(), n++);
    }
    return A.currentNode = E, i;
  }
  p(e) {
    let t = 0;
    for (const s of this._$AV) s !== void 0 && (s.strings !== void 0 ? (s._$AI(e, s, t), t += s.strings.length - 2) : s._$AI(e[t])), t++;
  }
}
class I {
  get _$AU() {
    return this._$AM?._$AU ?? this._$Cv;
  }
  constructor(e, t, s, i) {
    this.type = 2, this._$AH = d, this._$AN = void 0, this._$AA = e, this._$AB = t, this._$AM = s, this.options = i, this._$Cv = i?.isConnected ?? !0;
  }
  get parentNode() {
    let e = this._$AA.parentNode;
    const t = this._$AM;
    return t !== void 0 && e?.nodeType === 11 && (e = t.parentNode), e;
  }
  get startNode() {
    return this._$AA;
  }
  get endNode() {
    return this._$AB;
  }
  _$AI(e, t = this) {
    e = N(this, e, t), U(e) ? e === d || e == null || e === "" ? (this._$AH !== d && this._$AR(), this._$AH = d) : e !== this._$AH && e !== T && this._(e) : e._$litType$ !== void 0 ? this.$(e) : e.nodeType !== void 0 ? this.T(e) : Je(e) ? this.k(e) : this._(e);
  }
  O(e) {
    return this._$AA.parentNode.insertBefore(e, this._$AB);
  }
  T(e) {
    this._$AH !== e && (this._$AR(), this._$AH = this.O(e));
  }
  _(e) {
    this._$AH !== d && U(this._$AH) ? this._$AA.nextSibling.data = e : this.T(E.createTextNode(e)), this._$AH = e;
  }
  $(e) {
    const { values: t, _$litType$: s } = e, i = typeof s == "number" ? this._$AC(e) : (s.el === void 0 && (s.el = O.createElement(Ee(s.h, s.h[0]), this.options)), s);
    if (this._$AH?._$AD === i) this._$AH.p(t);
    else {
      const a = new Xe(i, this), n = a.u(this.options);
      a.p(t), this.T(n), this._$AH = a;
    }
  }
  _$AC(e) {
    let t = fe.get(e.strings);
    return t === void 0 && fe.set(e.strings, t = new O(e)), t;
  }
  k(e) {
    ie(this._$AH) || (this._$AH = [], this._$AR());
    const t = this._$AH;
    let s, i = 0;
    for (const a of e) i === t.length ? t.push(s = new I(this.O(R()), this.O(R()), this, this.options)) : s = t[i], s._$AI(a), i++;
    i < t.length && (this._$AR(s && s._$AB.nextSibling, i), t.length = i);
  }
  _$AR(e = this._$AA.nextSibling, t) {
    for (this._$AP?.(!1, !0, t); e !== this._$AB; ) {
      const s = ce(e).nextSibling;
      ce(e).remove(), e = s;
    }
  }
  setConnected(e) {
    this._$AM === void 0 && (this._$Cv = e, this._$AP?.(e));
  }
}
class W {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(e, t, s, i, a) {
    this.type = 1, this._$AH = d, this._$AN = void 0, this.element = e, this.name = t, this._$AM = i, this.options = a, s.length > 2 || s[0] !== "" || s[1] !== "" ? (this._$AH = Array(s.length - 1).fill(new String()), this.strings = s) : this._$AH = d;
  }
  _$AI(e, t = this, s, i) {
    const a = this.strings;
    let n = !1;
    if (a === void 0) e = N(this, e, t, 0), n = !U(e) || e !== this._$AH && e !== T, n && (this._$AH = e);
    else {
      const c = e;
      let h, p;
      for (e = a[0], h = 0; h < a.length - 1; h++) p = N(this, c[s + h], t, h), p === T && (p = this._$AH[h]), n ||= !U(p) || p !== this._$AH[h], p === d ? e = d : e !== d && (e += (p ?? "") + a[h + 1]), this._$AH[h] = p;
    }
    n && !i && this.j(e);
  }
  j(e) {
    e === d ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, e ?? "");
  }
}
class et extends W {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(e) {
    this.element[this.name] = e === d ? void 0 : e;
  }
}
class tt extends W {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(e) {
    this.element.toggleAttribute(this.name, !!e && e !== d);
  }
}
class st extends W {
  constructor(e, t, s, i, a) {
    super(e, t, s, i, a), this.type = 5;
  }
  _$AI(e, t = this) {
    if ((e = N(this, e, t, 0) ?? d) === T) return;
    const s = this._$AH, i = e === d && s !== d || e.capture !== s.capture || e.once !== s.once || e.passive !== s.passive, a = e !== d && (s === d || i);
    i && this.element.removeEventListener(this.name, this, s), a && this.element.addEventListener(this.name, this, e), this._$AH = e;
  }
  handleEvent(e) {
    typeof this._$AH == "function" ? this._$AH.call(this.options?.host ?? this.element, e) : this._$AH.handleEvent(e);
  }
}
class it {
  constructor(e, t, s) {
    this.element = e, this.type = 6, this._$AN = void 0, this._$AM = t, this.options = s;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(e) {
    N(this, e);
  }
}
const rt = se.litHtmlPolyfillSupport;
rt?.(O, I), (se.litHtmlVersions ??= []).push("3.3.3");
const at = (r, e, t) => {
  const s = t?.renderBefore ?? e;
  let i = s._$litPart$;
  if (i === void 0) {
    const a = t?.renderBefore ?? null;
    s._$litPart$ = i = new I(e.insertBefore(R(), a), a, void 0, t ?? {});
  }
  return i._$AI(r), i;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const re = globalThis;
class $ extends C {
  constructor() {
    super(...arguments), this.renderOptions = { host: this }, this._$Do = void 0;
  }
  createRenderRoot() {
    const e = super.createRenderRoot();
    return this.renderOptions.renderBefore ??= e.firstChild, e;
  }
  update(e) {
    const t = this.render();
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(e), this._$Do = at(t, this.renderRoot, this.renderOptions);
  }
  connectedCallback() {
    super.connectedCallback(), this._$Do?.setConnected(!0);
  }
  disconnectedCallback() {
    super.disconnectedCallback(), this._$Do?.setConnected(!1);
  }
  render() {
    return T;
  }
}
$._$litElement$ = !0, $.finalized = !0, re.litElementHydrateSupport?.({ LitElement: $ });
const nt = re.litElementPolyfillSupport;
nt?.({ LitElement: $ });
(re.litElementVersions ??= []).push("4.2.2");
class V extends $ {
  constructor() {
    super(...arguments), this._label = (e) => o(this.hass, `editor_${e.name}`);
  }
  static {
    this.properties = {
      hass: { attribute: !1 },
      _config: { state: !0 }
    };
  }
  setConfig(e) {
    this._config = e;
  }
  _changed(e) {
    e.stopPropagation(), this.dispatchEvent(
      new CustomEvent("config-changed", {
        detail: { config: { ...this._config, ...e.detail.value } },
        bubbles: !0,
        composed: !0
      })
    );
  }
  render() {
    return !this.hass || !this._config ? l`` : l`<ha-form
      .hass=${this.hass}
      .data=${{ ...this.defaults, ...this._config }}
      .schema=${this.fields}
      .computeLabel=${this._label}
      @value-changed=${this._changed}
    ></ha-form>`;
  }
}
class ot extends V {
  constructor() {
    super(...arguments), this.fields = [
      { name: "title", selector: { text: {} } },
      { name: "show_images", selector: { boolean: {} } },
      { name: "show_actions", selector: { boolean: {} } }
    ], this.defaults = { show_images: !0, show_actions: !0 };
  }
}
class lt extends V {
  constructor() {
    super(...arguments), this.fields = [
      { name: "title", selector: { text: {} } },
      { name: "show_image", selector: { boolean: {} } },
      { name: "show_ingredients", selector: { boolean: {} } }
    ], this.defaults = { show_image: !0, show_ingredients: !1 };
  }
}
class dt extends V {
  constructor() {
    super(...arguments), this.fields = [
      { name: "title", selector: { text: {} } },
      { name: "show_added", selector: { boolean: {} } },
      { name: "show_skipped", selector: { boolean: {} } }
    ], this.defaults = { show_added: !0, show_skipped: !1 };
  }
}
class ct extends V {
  constructor() {
    super(...arguments), this.fields = [
      { name: "title", selector: { text: {} } },
      { name: "editable", selector: { boolean: {} } }
    ], this.defaults = { editable: !0 };
  }
}
const Y = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"], Ce = [
  "gluten",
  "milk",
  "lactose",
  "egg",
  "fish",
  "crustaceans",
  "molluscs",
  "peanuts",
  "tree_nuts",
  "soy",
  "sesame",
  "celery",
  "mustard",
  "lupin",
  "sulphites"
], ht = ["omnivore", "vegetarian", "vegan", "pescatarian"], pt = ["small", "normal", "large"], B = "weeklymenu";
function q(r) {
  const e = /* @__PURE__ */ new Map();
  for (const t of Object.values(r.entities ?? {}))
    t.platform === B && t.translation_key && e.set(t.translation_key, t.entity_id);
  return e;
}
const f = (r) => typeof r == "string" && r !== "" ? r : void 0, b = (r) => typeof r == "number" && Number.isFinite(r) ? r : void 0, m = (r) => Array.isArray(r) ? r.filter((e) => typeof e == "string") : [], S = (r) => typeof r == "object" && r !== null;
function ut(r) {
  return (S(r) && Array.isArray(r.groups) ? r.groups : []).filter(S).map((t) => {
    const s = Array.isArray(t.substitutions) ? t.substitutions : [], i = (a) => S(a) ? f(a.raw) ?? f(a.name) ?? "" : "";
    return {
      members: m(t.members),
      share: b(t.share) ?? 0,
      separatePans: t.separate_pans === !0,
      swaps: s.filter(S).map((a) => ({
        original: i(a.original),
        replacement: i(a.replacement)
      }))
    };
  });
}
function gt(r) {
  return Array.isArray(r) ? r.filter(S).filter((e) => typeof e.id == "string" && typeof e.title == "string").map((e) => ({ id: e.id, title: e.title })) : [];
}
function Te(r, e, t = "") {
  const s = e ? r.states[e] : void 0;
  if (!s || ["unknown", "unavailable", ""].includes(s.state)) return;
  const i = s.attributes, a = f(i.date);
  if (a)
    return {
      entityId: s.entity_id,
      weekday: t,
      date: a,
      title: s.state,
      recipeId: f(i.recipe_id) ?? "",
      url: f(i.url),
      image: f(i.image),
      source: f(i.source),
      totalTime: b(i.total_time),
      servings: b(i.servings),
      tags: m(i.tags),
      ingredients: m(i.ingredients),
      locked: i.locked === !0,
      alternatives: gt(i.alternatives),
      split: ut(i.split)
    };
}
function _e(r) {
  const e = q(r), t = r.states[e.get("status") ?? ""], s = t?.state, i = t?.attributes ?? {}, a = [];
  for (const n of Y) {
    const c = Te(r, e.get(`weekday_${n}`), n);
    c && a.push(c);
  }
  return {
    status: s === "draft" || s === "confirmed" ? s : "none",
    weekStart: f(i.week_start),
    warnings: m(i.warnings),
    days: a
  };
}
function mt(r) {
  return Te(r, q(r).get("today"));
}
function Ne(r) {
  const [e, t, s] = r.split("-").map(Number), i = new Date(Date.UTC(e, t - 1, s)), a = i.getUTCDay() || 7;
  i.setUTCDate(i.getUTCDate() + 4 - a);
  const n = Date.UTC(i.getUTCFullYear(), 0, 1);
  return Math.ceil(((i.getTime() - n) / 864e5 + 1) / 7);
}
function ft(r) {
  return `${Math.round(r * 100)} %`;
}
function _t(r) {
  const e = r.states[q(r).get("shopping") ?? ""], t = e?.attributes ?? {}, s = S(t.counts) ? t.counts : {};
  return {
    hasResult: !!e && !["unknown", "unavailable", ""].includes(e.state),
    weekStart: f(t.week_start),
    counts: {
      added: b(s.added) ?? 0,
      review: b(s.review) ?? 0,
      failed: b(s.failed) ?? 0,
      skipped: b(s.skipped) ?? 0,
      pending: b(s.pending) ?? 0
    },
    added: m(t.added),
    review: m(t.review),
    failed: m(t.failed),
    pending: m(t.pending),
    skipped: m(t.skipped),
    targets: m(t.targets),
    errors: m(t.errors)
  };
}
function $e(r) {
  const e = r.states[q(r).get("family") ?? ""];
  return !e || ["unknown", "unavailable", ""].includes(e.state) ? { available: !1, members: [], dinnerDays: [] } : {
    available: !0,
    members: (Array.isArray(e.attributes.members) ? e.attributes.members : []).filter(S).map((i) => ({
      id: f(i.id) ?? "",
      name: f(i.name) ?? "",
      person: f(i.person),
      allergies: m(i.allergies),
      dislikes: m(i.dislikes),
      likes: m(i.likes),
      diet: f(i.diet) ?? "omnivore",
      portion: f(i.portion) ?? "normal",
      attends: m(i.attends),
      cookSeparately: i.cook_separately !== !1
    })).filter((i) => i.id && i.name),
    dinnerDays: m(e.attributes.dinner_days)
  };
}
function De(r) {
  const [e, t, s] = r.split("-").map(Number);
  return new Date(Date.UTC(e, t - 1, s));
}
function Q(r, e) {
  const t = H(r), s = De(e), i = { timeZone: "UTC" };
  return {
    weekday: new Intl.DateTimeFormat(t, { ...i, weekday: "short" }).format(s),
    date: new Intl.DateTimeFormat(t, { ...i, day: "numeric", month: "short" }).format(s)
  };
}
function $t(r, e) {
  return new Intl.DateTimeFormat(H(r), { timeZone: "UTC", weekday: "long" }).format(De(e));
}
function yt(r, e) {
  const t = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"].indexOf(e);
  return t < 0 ? e : $t(r, `2026-11-${String(2 + t).padStart(2, "0")}`);
}
function ye(r, e) {
  const t = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"].indexOf(e);
  return t < 0 ? e : Q(r, `2026-11-${String(2 + t).padStart(2, "0")}`).weekday;
}
function Pe(r, e) {
  const t = `source_${e.source}`, s = e.source ? o(r, t) : "";
  return l`<div class="meta">
    ${e.totalTime ? l`<span>${o(r, "minutes", { n: e.totalTime })}</span>` : d}
    ${e.tags.map((i) => l`<span class="tag">${Oe(r, i)}</span>`)}
    ${s && !s.startsWith("source_") ? l`<span class="badge">${s}</span>` : d}
    ${e.split.length ? l`<span class="badge split" title=${o(r, "split")}>${o(r, "split")}</span>` : d}
    ${e.locked ? l`<span class="badge">${o(r, "locked")}</span>` : d}
  </div>`;
}
function Me(r, e) {
  return e.length ? l`<div class="split-note">
    <strong>${o(r, "split")}</strong>
    ${e.map(
    (t) => l`<div>
        ${t.swaps.map(
      (s) => l`<div>
              ${o(r, "splitNote", {
        members: t.members.join(", ") + ` (${ft(t.share)})`,
        from: s.original,
        to: s.replacement
      })}
            </div>`
    )}
        ${t.separatePans ? l`<em>${o(r, "cleanPans")}</em>` : d}
      </div>`
  )}
  </div>` : d;
}
function Re(r, e) {
  return e.length ? l`<div>
    <h4>${o(r, "ingredients")}</h4>
    <ul>
      ${e.map((t) => l`<li>${t}</li>`)}
    </ul>
  </div>` : d;
}
function ae(r) {
  return r && typeof r == "object" && "message" in r ? String(r.message) : String(r);
}
const K = je`
  :host {
    display: block;
    container-type: inline-size;
  }
  ha-card {
    overflow: hidden;
  }
  .head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 0 16px 8px;
    color: var(--secondary-text-color);
    font-size: 0.9em;
  }
  .head {
    flex-wrap: wrap;
  }
  .head.chips {
    justify-content: flex-start;
  }
  .chip {
    white-space: nowrap;
    border-radius: 12px;
    padding: 2px 10px;
    font-size: 0.8em;
    background: var(--secondary-background-color);
    color: var(--primary-text-color);
  }
  .chip.draft {
    background: var(--warning-color, #ffa600);
    color: var(--text-primary-color, #fff);
  }
  .chip.confirmed {
    background: var(--success-color, #43a047);
    color: var(--text-primary-color, #fff);
  }
  .banner {
    margin: 0 16px 8px;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 0.9em;
    background: var(--secondary-background-color);
  }
  .banner.error {
    background: var(--error-color, #db4437);
    color: var(--text-primary-color, #fff);
  }
  .banner.warning {
    border-left: 4px solid var(--warning-color, #ffa600);
  }
  .empty {
    padding: 8px 16px 16px;
    color: var(--secondary-text-color);
  }
  .day {
    display: grid;
    grid-template-columns: 56px minmax(0, 1fr) auto;
    gap: 4px 12px;
    align-items: center;
    padding: 10px 16px;
    border-top: 1px solid var(--divider-color);
  }
  .when {
    text-align: center;
    line-height: 1.2;
  }
  .when .wd {
    font-weight: 500;
    text-transform: capitalize;
  }
  .when .dt {
    font-size: 0.8em;
    color: var(--secondary-text-color);
  }
  .main {
    display: flex;
    gap: 12px;
    align-items: center;
    min-width: 0;
  }
  .main img {
    width: 48px;
    height: 48px;
    border-radius: 8px;
    object-fit: cover;
    flex: none;
  }
  .title {
    font-weight: 500;
    overflow-wrap: anywhere;
  }
  .title a {
    color: inherit;
    text-decoration: none;
  }
  .title a:hover {
    text-decoration: underline;
  }
  .meta {
    display: flex;
    flex-wrap: wrap;
    gap: 4px 8px;
    margin-top: 2px;
    font-size: 0.85em;
    color: var(--secondary-text-color);
  }
  .tag {
    border-radius: 8px;
    padding: 0 6px;
    background: var(--secondary-background-color);
  }
  .badge {
    border-radius: 8px;
    padding: 0 6px;
    border: 1px solid var(--divider-color);
  }
  .badge.split {
    border-color: var(--primary-color);
    color: var(--primary-color);
  }
  .actions {
    display: flex;
    gap: 2px;
  }
  .more {
    grid-column: 1 / -1;
    display: grid;
    gap: 8px;
    min-width: 0;
    padding: 4px 0 4px 68px;
    font-size: 0.9em;
  }
  .more h4 {
    margin: 4px 0 2px;
    font-size: 0.9em;
    color: var(--secondary-text-color);
  }
  .more ul {
    margin: 0;
    padding-left: 18px;
  }
  .row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
    min-width: 0;
  }
  .row input {
    flex: 1 1 140px;
  }
  .row select {
    flex: 1 1 100%;
  }
  .split-note {
    border-left: 3px solid var(--primary-color);
    padding-left: 8px;
  }
  button {
    font: inherit;
    cursor: pointer;
    border: none;
    border-radius: 8px;
    padding: 6px 12px;
    background: var(--secondary-background-color);
    color: var(--primary-text-color);
  }
  button.primary {
    background: var(--primary-color);
    color: var(--text-primary-color, #fff);
  }
  button.icon {
    padding: 6px;
    background: transparent;
    line-height: 0;
    color: var(--secondary-text-color);
  }
  button.icon.on {
    color: var(--primary-color);
  }
  button:disabled {
    opacity: 0.4;
    cursor: default;
  }
  input,
  select {
    max-width: 100%;
    box-sizing: border-box;
    font: inherit;
    padding: 6px 8px;
    border-radius: 8px;
    border: 1px solid var(--divider-color);
    background: var(--card-background-color);
    color: var(--primary-text-color);
    min-width: 0;
  }
  .foot {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: flex-end;
    padding: 12px 16px;
    border-top: 1px solid var(--divider-color);
  }

  .member {
    padding: 10px 16px;
    border-top: 1px solid var(--divider-color);
  }
  .member .main {
    align-items: flex-start;
  }
  .tag.allergy {
    background: var(--error-color, #db4437);
    color: var(--text-primary-color, #fff);
  }
  .form {
    display: grid;
    gap: 10px;
    padding-top: 10px;
  }
  .field {
    display: grid;
    gap: 2px;
    min-width: 0;
    flex: 1 1 140px;
  }
  .field > span,
  legend {
    font-size: 0.85em;
    color: var(--secondary-text-color);
  }
  fieldset {
    margin: 0;
    padding: 0;
    border: none;
    min-width: 0;
  }
  .checks {
    display: flex;
    flex-wrap: wrap;
    gap: 4px 12px;
  }
  .check {
    display: flex;
    gap: 4px;
    align-items: center;
    font-size: 0.9em;
  }
  .hint-error {
    color: var(--error-color, #db4437);
  }
  .group {
    padding: 4px 16px;
    border-top: 1px solid var(--divider-color);
  }
  .group summary {
    cursor: pointer;
    padding: 6px 0;
    font-weight: 500;
  }
  .group.warning summary {
    color: var(--warning-color, #ffa600);
  }
  .group.error summary {
    color: var(--error-color, #db4437);
  }
  .group ul {
    margin: 0 0 8px;
    padding-left: 18px;
  }

  /* A narrow card (a phone, or a small grid cell): give the text all the room. */
  @container (max-width: 440px) {
    .day {
      grid-template-columns: 44px minmax(0, 1fr) auto;
      gap: 4px 8px;
      padding: 10px 12px;
    }
    .main {
      gap: 8px;
    }
    .main img {
      width: 40px;
      height: 40px;
    }
    .more {
      padding-left: 0;
    }
    .head,
    .foot {
      padding-left: 12px;
      padding-right: 12px;
    }
    .banner {
      margin-left: 12px;
      margin-right: 12px;
    }
  }
`, X = new Set(Ce), Z = (r) => r.split(",").map((e) => e.trim()).filter(Boolean);
function ve(r, e) {
  return r ? {
    id: r.id,
    name: r.name,
    allergies: r.allergies.filter((t) => X.has(t)),
    otherAllergies: r.allergies.filter((t) => !X.has(t)).join(", "),
    dislikes: r.dislikes.join(", "),
    likes: r.likes.join(", "),
    diet: r.diet,
    portion: r.portion,
    attends: [...r.attends],
    cookSeparately: r.cookSeparately
  } : {
    id: "",
    name: "",
    allergies: [],
    otherAllergies: "",
    dislikes: "",
    likes: "",
    diet: "omnivore",
    portion: "normal",
    attends: [...e],
    cookSeparately: !0
  };
}
class vt extends $ {
  static {
    this.properties = {
      hass: { attribute: !1 },
      _config: { state: !0 },
      _draft: { state: !0 },
      _busy: { state: !0 },
      _error: { state: !0 }
    };
  }
  static {
    this.styles = K;
  }
  constructor() {
    super(), this._config = { type: "custom:weeklymenu-family-card" }, this._draft = null, this._busy = !1, this._error = "";
  }
  static getConfigElement() {
    return document.createElement("weeklymenu-family-card-editor");
  }
  static getStubConfig() {
    return {};
  }
  setConfig(e) {
    if (!e) throw new Error("Invalid configuration");
    this._config = { editable: !0, ...e };
  }
  getCardSize() {
    return this.hass ? 2 + $e(this.hass).members.length : 3;
  }
  // --- actions ----------------------------------------------------------------------
  _set(e) {
    this._draft && (this._draft = { ...this._draft, ...e });
  }
  _toggle(e, t) {
    if (!this._draft) return;
    const s = this._draft[e];
    this._set({ [e]: s.includes(t) ? s.filter((i) => i !== t) : [...s, t] });
  }
  async _run(e, t) {
    this._busy = !0, this._error = "";
    try {
      return await this.hass.callService(B, e, t), !0;
    } catch (s) {
      return this._error = ae(s), !1;
    } finally {
      this._busy = !1;
    }
  }
  async _save() {
    const e = this._draft;
    if (!e || !e.name.trim() || !e.attends.length) return;
    const t = {
      name: e.name.trim(),
      allergies: [...e.allergies, ...Z(e.otherAllergies)],
      dislikes: Z(e.dislikes),
      likes: Z(e.likes),
      diet: e.diet,
      portion: e.portion,
      attends: Y.filter((s) => e.attends.includes(s)),
      cook_separately: e.cookSeparately
    };
    e.id && (t.id = e.id), await this._run("set_member", t) && (this._draft = null);
  }
  async _remove() {
    const e = this._draft;
    !e?.id || !window.confirm(o(this.hass, "famRemoveAsk", { name: e.name })) || await this._run("remove_member", { id: e.id }) && (this._draft = null);
  }
  // --- rendering --------------------------------------------------------------------------
  render() {
    if (!this.hass) return l``;
    const e = this.hass, t = $e(e), s = this._config.title ?? o(e, "familyTitle");
    if (!t.available)
      return l`<ha-card .header=${s}><div class="empty">${o(e, "famNoFamily")}</div></ha-card>`;
    const i = this._config.editable !== !1, a = t.dinnerDays.length ? t.dinnerDays : [...Y];
    return l`<ha-card .header=${s}>
      ${this._error ? l`<div class="banner error">${o(e, "error", { error: this._error })}</div>` : d}
      ${t.members.length ? t.members.map((n) => this._renderMember(n, t.dinnerDays, i, a)) : l`<div class="empty">${o(e, "famNone")}</div>`}
      ${this._draft && !this._draft.id ? this._renderForm(this._draft, a) : d}
      ${i && !this._draft ? l`<div class="foot">
            <button class="primary" ?disabled=${this._busy} @click=${() => this._draft = ve(void 0, a)}>
              ${o(e, "famAdd")}
            </button>
          </div>` : d}
    </ha-card>`;
  }
  _renderMember(e, t, s, i) {
    const a = this.hass, n = this._draft?.id === e.id, c = i.filter((p) => e.attends.includes(p)), h = c.length === i.length;
    return l`<div class="member">
      <div class="main">
        <div style="flex:1;min-width:0">
          <div class="title">${e.name}</div>
          <div class="meta">
            ${e.diet !== "omnivore" ? l`<span class="badge">${o(a, `diet_${e.diet}`)}</span>` : d}
            ${e.portion !== "normal" ? l`<span class="badge">${o(a, `portion_${e.portion}`)}</span>` : d}
            ${e.allergies.map((p) => l`<span class="tag allergy">${X.has(p) ? o(a, `allergen_${p}`) : p}</span>`)}
            ${e.dislikes.length ? l`<span>${e.dislikes.join(", ")}</span>` : d}
            <span>${h ? o(a, "famEveryDay") : c.map((p) => ye(a, p)).join(", ")}</span>
          </div>
        </div>
        ${s && !n ? l`<button ?disabled=${this._busy} @click=${() => this._draft = ve(e, t)}>
              ${o(a, "famEdit")}
            </button>` : d}
      </div>
      ${n && this._draft ? this._renderForm(this._draft, i) : d}
    </div>`;
  }
  _renderForm(e, t) {
    const s = this.hass, i = e.name.trim() !== "" && e.attends.length > 0, a = (n, c, h) => l`<label class="field">
      <span>${o(s, n)}</span>
      <input
        type="text"
        .value=${c}
        @input=${(p) => this._set({ [h]: p.target.value })}
      />
    </label>`;
    return l`<form class="form" @submit=${(n) => n.preventDefault()}>
      ${a("famName", e.name, "name")}
      <fieldset>
        <legend>${o(s, "famAllergies")}</legend>
        <div class="checks">
          ${Ce.map(
      (n) => l`<label class="check">
              <input type="checkbox" .checked=${e.allergies.includes(n)} @change=${() => this._toggle("allergies", n)} />
              ${o(s, `allergen_${n}`)}
            </label>`
    )}
        </div>
      </fieldset>
      ${a("famOtherAllergies", e.otherAllergies, "otherAllergies")} ${a("famDislikes", e.dislikes, "dislikes")}
      ${a("famLikes", e.likes, "likes")}
      <div class="row">
        <label class="field">
          <span>${o(s, "famDiet")}</span>
          <select .value=${e.diet} @change=${(n) => this._set({ diet: n.target.value })}>
            ${ht.map((n) => l`<option value=${n} ?selected=${e.diet === n}>${o(s, `diet_${n}`)}</option>`)}
          </select>
        </label>
        <label class="field">
          <span>${o(s, "famPortion")}</span>
          <select .value=${e.portion} @change=${(n) => this._set({ portion: n.target.value })}>
            ${pt.map((n) => l`<option value=${n} ?selected=${e.portion === n}>${o(s, `portion_${n}`)}</option>`)}
          </select>
        </label>
      </div>
      <fieldset>
        <legend>${o(s, "famDays")}</legend>
        <div class="checks">
          ${t.map(
      (n) => l`<label class="check">
              <input type="checkbox" .checked=${e.attends.includes(n)} @change=${() => this._toggle("attends", n)} />
              ${ye(s, n)}
            </label>`
    )}
        </div>
        ${e.attends.length ? d : l`<small class="hint-error">${o(s, "famNoDays")}</small>`}
      </fieldset>
      <label class="check">
        <input
          type="checkbox"
          .checked=${e.cookSeparately}
          @change=${(n) => this._set({ cookSeparately: n.target.checked })}
        />
        ${o(s, "famCookSeparately")}
      </label>
      <small>${o(s, "famAppliesLater")}</small>
      <div class="row">
        <button class="primary" type="button" ?disabled=${this._busy || !i} @click=${() => this._save()}>${o(s, "famSave")}</button>
        <button type="button" ?disabled=${this._busy} @click=${() => this._draft = null}>${o(s, "famCancel")}</button>
        ${e.id ? l`<button type="button" ?disabled=${this._busy} @click=${() => this._remove()}>${o(s, "famRemove")}</button>` : d}
      </div>
    </form>`;
  }
}
class wt extends $ {
  static {
    this.properties = {
      hass: { attribute: !1 },
      _config: { state: !0 },
      _open: { state: !0 },
      _busy: { state: !0 },
      _error: { state: !0 },
      _hints: { state: !0 }
    };
  }
  static {
    this.styles = K;
  }
  constructor() {
    super(), this._config = { type: "custom:weeklymenu-menu-card" }, this._open = /* @__PURE__ */ new Set(), this._busy = !1, this._error = "", this._hints = {};
  }
  static getConfigElement() {
    return document.createElement("weeklymenu-menu-card-editor");
  }
  static getStubConfig() {
    return {};
  }
  setConfig(e) {
    if (!e) throw new Error("Invalid configuration");
    this._config = { show_images: !0, show_actions: !0, ...e };
  }
  getCardSize() {
    return this.hass ? 2 + _e(this.hass).days.length : 4;
  }
  // --- actions ------------------------------------------------------------------
  async _call(e, t = {}) {
    this._busy = !0, this._error = "";
    try {
      await this.hass.callService(B, e, t);
    } catch (s) {
      this._error = ae(s);
    } finally {
      this._busy = !1;
    }
  }
  _toggle(e) {
    const t = new Set(this._open);
    t.delete(e) || t.add(e), this._open = t;
  }
  _confirm(e) {
    window.confirm(o(this.hass, "confirmAsk")) && this._call("confirm_menu", e.weekStart ? { week_start: e.weekStart } : {});
  }
  _regenerateDay(e) {
    const t = (this._hints[e.date] ?? "").trim();
    this._call("regenerate_day", { date: e.date, ...t ? { hint: t } : {} });
  }
  _pick(e, t) {
    const s = t.target, i = s.value;
    s.value = "", i && this._call("set_recipe", { date: e.date, recipe_id: i });
  }
  _swap(e, t) {
    const s = t.target, i = s.value;
    s.value = "", i && this._call("swap_days", { date: e.date, other_date: i });
  }
  // --- rendering -------------------------------------------------------------------
  render() {
    if (!this.hass) return l``;
    const e = this.hass, t = _e(e), s = t.status === "confirmed", i = this._config.show_actions !== !1 && !s, a = [...new Set(t.warnings.map((n) => Ue(e, n, (c) => yt(e, c))))];
    return l`<ha-card .header=${this._config.title ?? o(e, "menuTitle")}>
      <div class="head">
        <span>${t.weekStart ? o(e, "week", { n: Ne(t.weekStart) }) : ""}</span>
        <span class="chip ${t.status}">${o(e, `status_${t.status}`)}</span>
      </div>
      ${a.map((n) => l`<div class="banner warning">${n}</div>`)}
      ${this._error ? l`<div class="banner error">${o(e, "error", { error: this._error })}</div>` : d}
      ${this._busy ? l`<div class="banner">${o(e, "working")}</div>` : d}
      ${t.days.length ? t.days.map((n) => this._renderDay(n, t, i)) : l`<div class="empty">${o(e, "noMenu")}</div>`}
      ${s && this._config.show_actions !== !1 ? l`<div class="banner">${o(e, "confirmedNote")}</div>` : d}
      ${this._renderFooter(t, i)}
    </ha-card>`;
  }
  _renderFooter(e, t) {
    if (!t) return d;
    const s = e.days.length === 0;
    return l`<div class="foot">
      <button
        class=${s ? "primary" : ""}
        ?disabled=${this._busy}
        @click=${() => this._call("generate_menu", e.weekStart && !s ? { week_start: e.weekStart } : {})}
      >
        ${s ? o(this.hass, "generate") : o(this.hass, "regenerateAll")}
      </button>
      ${e.status === "draft" && !s ? l`<button class="primary" ?disabled=${this._busy} @click=${() => this._confirm(e)}>
            ${o(this.hass, "confirm")}
          </button>` : d}
    </div>`;
  }
  _renderDay(e, t, s) {
    const i = this.hass, a = Q(i, e.date), n = this._open.has(e.date), c = e.url ? l`<a href=${e.url} target="_blank" rel="noopener noreferrer" title=${o(i, "openRecipe")}>${e.title}</a>` : e.title, h = t.days.filter((p) => p.date !== e.date && !p.locked);
    return l`<div class="day">
      <div class="when">
        <div class="wd">${a.weekday}</div>
        <div class="dt">${a.date}</div>
      </div>
      <div class="main">
        ${this._config.show_images !== !1 && e.image ? l`<img src=${e.image} alt="" loading="lazy" />` : d}
        <div>
          <div class="title">${c}</div>
          ${Pe(i, e)}
        </div>
      </div>
      <div class="actions">
        ${s ? l`<button
              class="icon ${e.locked ? "on" : ""}"
              ?disabled=${this._busy}
              title=${e.locked ? o(i, "unlock") : o(i, "lock")}
              aria-label=${e.locked ? o(i, "unlock") : o(i, "lock")}
              aria-pressed=${e.locked ? "true" : "false"}
              @click=${() => this._call("lock_day", { date: e.date, locked: !e.locked })}
            >
              <ha-icon icon=${e.locked ? "mdi:lock" : "mdi:lock-open-variant-outline"}></ha-icon>
            </button>` : d}
        <button
          class="icon"
          title=${n ? o(i, "hide") : o(i, "show")}
          aria-label=${n ? o(i, "hide") : o(i, "show")}
          aria-expanded=${n ? "true" : "false"}
          @click=${() => this._toggle(e.date)}
        >
          <ha-icon icon=${n ? "mdi:chevron-up" : "mdi:chevron-down"}></ha-icon>
        </button>
      </div>
      ${n ? this._renderMore(e, h, s) : d}
    </div>`;
  }
  _renderMore(e, t, s) {
    const i = this.hass;
    return l`<div class="more">
      ${Me(i, e.split)} ${Re(i, e.ingredients)}
      ${s ? l`<div class="row">
              <input
                type="text"
                .value=${this._hints[e.date] ?? ""}
                placeholder=${o(i, "hint")}
                aria-label=${o(i, "hint")}
                @input=${(a) => {
      this._hints = { ...this._hints, [e.date]: a.target.value };
    }}
              />
              <button ?disabled=${this._busy || e.locked} @click=${() => this._regenerateDay(e)}>
                ${o(i, "newDinner")}
              </button>
            </div>
            <div class="row">
              ${e.alternatives.length ? l`<select
                    ?disabled=${this._busy}
                    aria-label=${o(i, "alternatives")}
                    @change=${(a) => this._pick(e, a)}
                  >
                    <option value="">${o(i, "alternatives")}: ${o(i, "choose")}</option>
                    ${e.alternatives.map((a) => l`<option value=${a.id}>${a.title}</option>`)}
                  </select>` : d}
              ${t.length && !e.locked ? l`<select
                    ?disabled=${this._busy}
                    aria-label=${o(i, "swapWith")}
                    @change=${(a) => this._swap(e, a)}
                  >
                    <option value="">${o(i, "swapWith")}</option>
                    ${t.map((a) => {
      const n = Q(i, a.date);
      return l`<option value=${a.date}>${n.weekday} ${n.date}: ${a.title}</option>`;
    })}
                  </select>` : d}
            </div>` : d}
    </div>`;
  }
}
const we = [
  { key: "review", label: "shopReview", css: "warning" },
  { key: "failed", label: "shopFailed", css: "error" },
  { key: "pending", label: "shopPending", css: "" },
  { key: "added", label: "shopAdded", css: "" },
  { key: "skipped", label: "shopSkipped", css: "" }
];
class bt extends $ {
  static {
    this.properties = {
      hass: { attribute: !1 },
      _config: { state: !0 },
      _busy: { state: !0 },
      _error: { state: !0 }
    };
  }
  static {
    this.styles = K;
  }
  constructor() {
    super(), this._config = { type: "custom:weeklymenu-shopping-card" }, this._busy = !1, this._error = "";
  }
  static getConfigElement() {
    return document.createElement("weeklymenu-shopping-card-editor");
  }
  static getStubConfig() {
    return {};
  }
  setConfig(e) {
    if (!e) throw new Error("Invalid configuration");
    this._config = { show_added: !0, show_skipped: !1, ...e };
  }
  getCardSize() {
    return 4;
  }
  async _retry() {
    this._busy = !0, this._error = "";
    try {
      await this.hass.callService(B, "add_to_shopping", {});
    } catch (e) {
      this._error = ae(e);
    } finally {
      this._busy = !1;
    }
  }
  render() {
    if (!this.hass) return l``;
    const e = this.hass, t = _t(e), s = this._config.title ?? o(e, "shoppingTitle");
    if (!t.hasResult)
      return l`<ha-card .header=${s}><div class="empty">${o(e, "shopNothing")}</div></ha-card>`;
    const i = t.counts.failed + t.counts.pending, a = t.errors.some((c) => c.endsWith(": auth_failed")), n = [
      ...new Set(t.errors.filter((c) => !(a && c === "reauth_required")).map((c) => Ie(e, c)))
    ];
    return l`<ha-card .header=${s}>
      <div class="head">
        <span>
          ${t.weekStart ? o(e, "week", { n: Ne(t.weekStart) }) : ""}
          ${t.targets.length ? ` · ${o(e, "shopTargets", { targets: t.targets.join(", ") })}` : ""}
        </span>
      </div>
      <div class="head chips">
        ${we.filter((c) => t.counts[c.key] > 0).map(
      (c) => l`<span class="chip ${c.css === "warning" ? "draft" : ""}">${o(e, c.label)}: ${t.counts[c.key]}</span>`
    )}
      </div>
      ${n.map((c) => l`<div class="banner warning">${c}</div>`)}
      ${this._error ? l`<div class="banner error">${o(e, "error", { error: this._error })}</div>` : d}
      ${we.map((c) => this._renderGroup(c, t[c.key]))}
      ${i ? l`<div class="foot">
            <button class="primary" ?disabled=${this._busy} @click=${() => this._retry()}>${o(e, "shopRetry")}</button>
          </div>` : d}
    </ha-card>`;
  }
  _renderGroup(e, t) {
    if (!t.length || e.key === "added" && this._config.show_added === !1 || e.key === "skipped" && !this._config.show_skipped) return d;
    const s = e.key === "review" || e.key === "failed" || e.key === "pending";
    return l`<details class="group ${e.css}" ?open=${s}>
      <summary>${o(this.hass, e.label)} (${t.length})</summary>
      <ul>
        ${t.map((i) => l`<li>${i}</li>`)}
      </ul>
    </details>`;
  }
}
class kt extends $ {
  static {
    this.properties = {
      hass: { attribute: !1 },
      _config: { state: !0 }
    };
  }
  static {
    this.styles = [
      K
      // only what differs from the menu card
    ];
  }
  constructor() {
    super(), this._config = { type: "custom:weeklymenu-today-card" };
  }
  static getConfigElement() {
    return document.createElement("weeklymenu-today-card-editor");
  }
  static getStubConfig() {
    return {};
  }
  setConfig(e) {
    if (!e) throw new Error("Invalid configuration");
    this._config = { show_image: !0, show_ingredients: !1, ...e };
  }
  getCardSize() {
    return 3;
  }
  render() {
    if (!this.hass) return l``;
    const e = this.hass, t = mt(e), s = this._config.title ?? o(e, "todayTitle");
    if (!t)
      return l`<ha-card .header=${s}><div class="empty">${o(e, "noDinner")}</div></ha-card>`;
    const i = t.url ? l`<a href=${t.url} target="_blank" rel="noopener noreferrer" title=${o(e, "openRecipe")}>${t.title}</a>` : t.title;
    return l`<ha-card .header=${s}>
      <div class="day" style="grid-template-columns: 1fr">
        <div class="main">
          ${this._config.show_image !== !1 && t.image ? l`<img src=${t.image} alt="" loading="lazy" style="width:72px;height:72px" />` : d}
          <div>
            <div class="title">${i}</div>
            ${Pe(e, t)}
          </div>
        </div>
        <div class="more" style="padding-left:0">
          ${Me(e, t.split)}
          ${this._config.show_ingredients ? Re(e, t.ingredients) : d}
        </div>
      </div>
    </ha-card>`;
  }
}
function k(r, e) {
  customElements.get(r) || customElements.define(r, e);
}
k("weeklymenu-menu-card", wt);
k("weeklymenu-menu-card-editor", ot);
k("weeklymenu-today-card", kt);
k("weeklymenu-today-card-editor", lt);
k("weeklymenu-shopping-card", bt);
k("weeklymenu-shopping-card-editor", dt);
k("weeklymenu-family-card", vt);
k("weeklymenu-family-card-editor", ct);
const v = { language: H({ language: navigator.language }) };
window.customCards = window.customCards ?? [];
window.customCards.push(
  {
    type: "weeklymenu-menu-card",
    name: o(v, "cardMenuName"),
    description: o(v, "cardMenuDescription"),
    preview: !0
  },
  {
    type: "weeklymenu-today-card",
    name: o(v, "cardTodayName"),
    description: o(v, "cardTodayDescription"),
    preview: !0
  },
  {
    type: "weeklymenu-shopping-card",
    name: o(v, "cardShoppingName"),
    description: o(v, "cardShoppingDescription"),
    preview: !0
  },
  {
    type: "weeklymenu-family-card",
    name: o(v, "cardFamilyName"),
    description: o(v, "cardFamilyDescription"),
    preview: !0
  }
);
