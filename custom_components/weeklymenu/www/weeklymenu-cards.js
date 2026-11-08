const R = {
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
    rateAs: "Rating as",
    ratingGroup: "Rating",
    starsN: "{n} stars",
    starOne: "1 star",
    favoriteAdd: "Add to favorites",
    favoriteRemove: "Remove from favorites",
    favoriteOf: "Favorite of {names}",
    famChild: "Child (their ratings count half)",
    famNotify: 'Notify service for "How was it?" (such as mobile_app_annas_phone)',
    famChildBadge: "Child",
    famFavorites: "Favorites ({n})",
    famNoFavorites: "No favorites yet. Add one with the heart on a dinner.",
    famRemoveFavorite: "Remove {title} from favorites",
    famName: "Name",
    famPerson: "Home Assistant person (shows their picture)",
    famNoPerson: "None",
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
    rateAs: "Betyg som",
    ratingGroup: "Betyg",
    starsN: "{n} stjärnor",
    starOne: "1 stjärna",
    favoriteAdd: "Lägg till som favorit",
    favoriteRemove: "Ta bort som favorit",
    favoriteOf: "Favorit hos {names}",
    famChild: "Barn (betyget väger hälften)",
    famNotify: 'Notistjänst för "Hur var det?" (till exempel mobile_app_annas_telefon)',
    famChildBadge: "Barn",
    famFavorites: "Favoriter ({n})",
    famNoFavorites: "Inga favoriter än. Lägg till en med hjärtat på en middag.",
    famRemoveFavorite: "Ta bort {title} som favorit",
    famName: "Namn",
    famPerson: "Person i Home Assistant (visar deras bild)",
    famNoPerson: "Ingen",
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
function W(r) {
  return (r?.locale?.language ?? r?.language ?? "en").slice(0, 2) === "sv" ? "sv" : "en";
}
function o(r, e, t = {}) {
  return (R[W(r)][e] ?? R.en[e]).replace(/\{(\w+)\}/g, (i, n) => String(t[n] ?? `{${n}}`));
}
function je(r, e, t) {
  const [s, i = ""] = e.split(":"), n = `warn_${s}`;
  if (!(n in R.en)) return e;
  const a = s === "no_recipe" || s === "split_limit_exceeded" ? t(i) : i;
  return o(r, n, { detail: a });
}
function Le(r, e) {
  const t = `tag_${e}`;
  return t in R.en ? o(r, t) : e.replace(/_/g, " ");
}
function Ie(r, e) {
  const [t, s] = e.includes(": ") ? e.split(": ", 2) : ["", e], i = `err_${s}`;
  return i in R.en ? o(r, i, { store: t.toUpperCase() }) : e;
}
/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const z = globalThis, se = z.ShadowRoot && (z.ShadyCSS === void 0 || z.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, ie = Symbol(), le = /* @__PURE__ */ new WeakMap();
let ke = class {
  constructor(e, t, s) {
    if (this._$cssResult$ = !0, s !== ie) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = e, this.t = t;
  }
  get styleSheet() {
    let e = this.o;
    const t = this.t;
    if (se && e === void 0) {
      const s = t !== void 0 && t.length === 1;
      s && (e = le.get(t)), e === void 0 && ((this.o = e = new CSSStyleSheet()).replaceSync(this.cssText), s && le.set(t, e));
    }
    return e;
  }
  toString() {
    return this.cssText;
  }
};
const He = (r) => new ke(typeof r == "string" ? r : r + "", void 0, ie), ze = (r, ...e) => {
  const t = r.length === 1 ? r[0] : e.reduce((s, i, n) => s + ((a) => {
    if (a._$cssResult$ === !0) return a.cssText;
    if (typeof a == "number") return a;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + a + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(i) + r[n + 1], r[0]);
  return new ke(t, r, ie);
}, Be = (r, e) => {
  if (se) r.adoptedStyleSheets = e.map((t) => t instanceof CSSStyleSheet ? t : t.styleSheet);
  else for (const t of e) {
    const s = document.createElement("style"), i = z.litNonce;
    i !== void 0 && s.setAttribute("nonce", i), s.textContent = t.cssText, r.appendChild(s);
  }
}, de = se ? (r) => r : (r) => r instanceof CSSStyleSheet ? ((e) => {
  let t = "";
  for (const s of e.cssRules) t += s.cssText;
  return He(t);
})(r) : r;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: We, defineProperty: Ve, getOwnPropertyDescriptor: Ge, getOwnPropertyNames: qe, getOwnPropertySymbols: Ke, getPrototypeOf: Ze } = Object, V = globalThis, ce = V.trustedTypes, Je = ce ? ce.emptyScript : "", Ye = V.reactiveElementPolyfillSupport, D = (r, e) => r, Q = { toAttribute(r, e) {
  switch (e) {
    case Boolean:
      r = r ? Je : null;
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
} }, xe = (r, e) => !We(r, e), he = { attribute: !0, type: String, converter: Q, reflect: !1, useDefault: !1, hasChanged: xe };
Symbol.metadata ??= Symbol("metadata"), V.litPropertyMetadata ??= /* @__PURE__ */ new WeakMap();
let C = class extends HTMLElement {
  static addInitializer(e) {
    this._$Ei(), (this.l ??= []).push(e);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(e, t = he) {
    if (t.state && (t.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(e) && ((t = Object.create(t)).wrapped = !0), this.elementProperties.set(e, t), !t.noAccessor) {
      const s = Symbol(), i = this.getPropertyDescriptor(e, s, t);
      i !== void 0 && Ve(this.prototype, e, i);
    }
  }
  static getPropertyDescriptor(e, t, s) {
    const { get: i, set: n } = Ge(this.prototype, e) ?? { get() {
      return this[t];
    }, set(a) {
      this[t] = a;
    } };
    return { get: i, set(a) {
      const h = i?.call(this);
      n?.call(this, a), this.requestUpdate(e, h, s);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(e) {
    return this.elementProperties.get(e) ?? he;
  }
  static _$Ei() {
    if (this.hasOwnProperty(D("elementProperties"))) return;
    const e = Ze(this);
    e.finalize(), e.l !== void 0 && (this.l = [...e.l]), this.elementProperties = new Map(e.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(D("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(D("properties"))) {
      const t = this.properties, s = [...qe(t), ...Ke(t)];
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
      for (const i of s) t.unshift(de(i));
    } else e !== void 0 && t.push(de(e));
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
    return Be(e, this.constructor.elementStyles), e;
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
      const n = (s.converter?.toAttribute !== void 0 ? s.converter : Q).toAttribute(t, s.type);
      this._$Em = e, n == null ? this.removeAttribute(i) : this.setAttribute(i, n), this._$Em = null;
    }
  }
  _$AK(e, t) {
    const s = this.constructor, i = s._$Eh.get(e);
    if (i !== void 0 && this._$Em !== i) {
      const n = s.getPropertyOptions(i), a = typeof n.converter == "function" ? { fromAttribute: n.converter } : n.converter?.fromAttribute !== void 0 ? n.converter : Q;
      this._$Em = i;
      const h = a.fromAttribute(t, n.type);
      this[i] = h ?? this._$Ej?.get(i) ?? h, this._$Em = null;
    }
  }
  requestUpdate(e, t, s, i = !1, n) {
    if (e !== void 0) {
      const a = this.constructor;
      if (i === !1 && (n = this[e]), s ??= a.getPropertyOptions(e), !((s.hasChanged ?? xe)(n, t) || s.useDefault && s.reflect && n === this._$Ej?.get(e) && !this.hasAttribute(a._$Eu(e, s)))) return;
      this.C(e, t, s);
    }
    this.isUpdatePending === !1 && (this._$ES = this._$EP());
  }
  C(e, t, { useDefault: s, reflect: i, wrapped: n }, a) {
    s && !(this._$Ej ??= /* @__PURE__ */ new Map()).has(e) && (this._$Ej.set(e, a ?? t ?? this[e]), n !== !0 || a !== void 0) || (this._$AL.has(e) || (this.hasUpdated || s || (t = void 0), this._$AL.set(e, t)), i === !0 && this._$Em !== e && (this._$Eq ??= /* @__PURE__ */ new Set()).add(e));
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
        for (const [i, n] of this._$Ep) this[i] = n;
        this._$Ep = void 0;
      }
      const s = this.constructor.elementProperties;
      if (s.size > 0) for (const [i, n] of s) {
        const { wrapped: a } = n, h = this[i];
        a !== !0 || this._$AL.has(i) || h === void 0 || this.C(i, void 0, n, h);
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
C.elementStyles = [], C.shadowRootOptions = { mode: "open" }, C[D("elementProperties")] = /* @__PURE__ */ new Map(), C[D("finalized")] = /* @__PURE__ */ new Map(), Ye?.({ ReactiveElement: C }), (V.reactiveElementVersions ??= []).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const re = globalThis, pe = (r) => r, B = re.trustedTypes, ue = B ? B.createPolicy("lit-html", { createHTML: (r) => r }) : void 0, Ae = "$lit$", x = `lit$${Math.random().toFixed(9).slice(2)}$`, Se = "?" + x, Qe = `<${Se}>`, E = document, M = () => E.createComment(""), O = (r) => r === null || typeof r != "object" && typeof r != "function", ae = Array.isArray, Xe = (r) => ae(r) || typeof r?.[Symbol.iterator] == "function", J = `[ 	
\f\r]`, P = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, me = /-->/g, fe = />/g, A = RegExp(`>|${J}(?:([^\\s"'>=/]+)(${J}*=${J}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`, "g"), ge = /'/g, _e = /"/g, Ee = /^(?:script|style|textarea|title)$/i, et = (r) => (e, ...t) => ({ _$litType$: r, strings: e, values: t }), l = et(1), N = Symbol.for("lit-noChange"), c = Symbol.for("lit-nothing"), $e = /* @__PURE__ */ new WeakMap(), S = E.createTreeWalker(E, 129);
function Ce(r, e) {
  if (!ae(r) || !r.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return ue !== void 0 ? ue.createHTML(e) : e;
}
const tt = (r, e) => {
  const t = r.length - 1, s = [];
  let i, n = e === 2 ? "<svg>" : e === 3 ? "<math>" : "", a = P;
  for (let h = 0; h < t; h++) {
    const d = r[h];
    let p, u, m = -1, y = 0;
    for (; y < d.length && (a.lastIndex = y, u = a.exec(d), u !== null); ) y = a.lastIndex, a === P ? u[1] === "!--" ? a = me : u[1] !== void 0 ? a = fe : u[2] !== void 0 ? (Ee.test(u[2]) && (i = RegExp("</" + u[2], "g")), a = A) : u[3] !== void 0 && (a = A) : a === A ? u[0] === ">" ? (a = i ?? P, m = -1) : u[1] === void 0 ? m = -2 : (m = a.lastIndex - u[2].length, p = u[1], a = u[3] === void 0 ? A : u[3] === '"' ? _e : ge) : a === _e || a === ge ? a = A : a === me || a === fe ? a = P : (a = A, i = void 0);
    const w = a === A && r[h + 1].startsWith("/>") ? " " : "";
    n += a === P ? d + Qe : m >= 0 ? (s.push(p), d.slice(0, m) + Ae + d.slice(m) + x + w) : d + x + (m === -2 ? h : w);
  }
  return [Ce(r, n + (r[t] || "<?>") + (e === 2 ? "</svg>" : e === 3 ? "</math>" : "")), s];
};
class F {
  constructor({ strings: e, _$litType$: t }, s) {
    let i;
    this.parts = [];
    let n = 0, a = 0;
    const h = e.length - 1, d = this.parts, [p, u] = tt(e, t);
    if (this.el = F.createElement(p, s), S.currentNode = this.el.content, t === 2 || t === 3) {
      const m = this.el.content.firstChild;
      m.replaceWith(...m.childNodes);
    }
    for (; (i = S.nextNode()) !== null && d.length < h; ) {
      if (i.nodeType === 1) {
        if (i.hasAttributes()) for (const m of i.getAttributeNames()) if (m.endsWith(Ae)) {
          const y = u[a++], w = i.getAttribute(m).split(x), H = /([.?@])?(.*)/.exec(y);
          d.push({ type: 1, index: n, name: H[2], strings: w, ctor: H[1] === "." ? it : H[1] === "?" ? rt : H[1] === "@" ? at : G }), i.removeAttribute(m);
        } else m.startsWith(x) && (d.push({ type: 6, index: n }), i.removeAttribute(m));
        if (Ee.test(i.tagName)) {
          const m = i.textContent.split(x), y = m.length - 1;
          if (y > 0) {
            i.textContent = B ? B.emptyScript : "";
            for (let w = 0; w < y; w++) i.append(m[w], M()), S.nextNode(), d.push({ type: 2, index: ++n });
            i.append(m[y], M());
          }
        }
      } else if (i.nodeType === 8) if (i.data === Se) d.push({ type: 2, index: n });
      else {
        let m = -1;
        for (; (m = i.data.indexOf(x, m + 1)) !== -1; ) d.push({ type: 7, index: n }), m += x.length - 1;
      }
      n++;
    }
  }
  static createElement(e, t) {
    const s = E.createElement("template");
    return s.innerHTML = e, s;
  }
}
function T(r, e, t = r, s) {
  if (e === N) return e;
  let i = s !== void 0 ? t._$Co?.[s] : t._$Cl;
  const n = O(e) ? void 0 : e._$litDirective$;
  return i?.constructor !== n && (i?._$AO?.(!1), n === void 0 ? i = void 0 : (i = new n(r), i._$AT(r, t, s)), s !== void 0 ? (t._$Co ??= [])[s] = i : t._$Cl = i), i !== void 0 && (e = T(r, i._$AS(r, e.values), i, s)), e;
}
class st {
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
    S.currentNode = i;
    let n = S.nextNode(), a = 0, h = 0, d = s[0];
    for (; d !== void 0; ) {
      if (a === d.index) {
        let p;
        d.type === 2 ? p = new j(n, n.nextSibling, this, e) : d.type === 1 ? p = new d.ctor(n, d.name, d.strings, this, e) : d.type === 6 && (p = new nt(n, this, e)), this._$AV.push(p), d = s[++h];
      }
      a !== d?.index && (n = S.nextNode(), a++);
    }
    return S.currentNode = E, i;
  }
  p(e) {
    let t = 0;
    for (const s of this._$AV) s !== void 0 && (s.strings !== void 0 ? (s._$AI(e, s, t), t += s.strings.length - 2) : s._$AI(e[t])), t++;
  }
}
class j {
  get _$AU() {
    return this._$AM?._$AU ?? this._$Cv;
  }
  constructor(e, t, s, i) {
    this.type = 2, this._$AH = c, this._$AN = void 0, this._$AA = e, this._$AB = t, this._$AM = s, this.options = i, this._$Cv = i?.isConnected ?? !0;
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
    e = T(this, e, t), O(e) ? e === c || e == null || e === "" ? (this._$AH !== c && this._$AR(), this._$AH = c) : e !== this._$AH && e !== N && this._(e) : e._$litType$ !== void 0 ? this.$(e) : e.nodeType !== void 0 ? this.T(e) : Xe(e) ? this.k(e) : this._(e);
  }
  O(e) {
    return this._$AA.parentNode.insertBefore(e, this._$AB);
  }
  T(e) {
    this._$AH !== e && (this._$AR(), this._$AH = this.O(e));
  }
  _(e) {
    this._$AH !== c && O(this._$AH) ? this._$AA.nextSibling.data = e : this.T(E.createTextNode(e)), this._$AH = e;
  }
  $(e) {
    const { values: t, _$litType$: s } = e, i = typeof s == "number" ? this._$AC(e) : (s.el === void 0 && (s.el = F.createElement(Ce(s.h, s.h[0]), this.options)), s);
    if (this._$AH?._$AD === i) this._$AH.p(t);
    else {
      const n = new st(i, this), a = n.u(this.options);
      n.p(t), this.T(a), this._$AH = n;
    }
  }
  _$AC(e) {
    let t = $e.get(e.strings);
    return t === void 0 && $e.set(e.strings, t = new F(e)), t;
  }
  k(e) {
    ae(this._$AH) || (this._$AH = [], this._$AR());
    const t = this._$AH;
    let s, i = 0;
    for (const n of e) i === t.length ? t.push(s = new j(this.O(M()), this.O(M()), this, this.options)) : s = t[i], s._$AI(n), i++;
    i < t.length && (this._$AR(s && s._$AB.nextSibling, i), t.length = i);
  }
  _$AR(e = this._$AA.nextSibling, t) {
    for (this._$AP?.(!1, !0, t); e !== this._$AB; ) {
      const s = pe(e).nextSibling;
      pe(e).remove(), e = s;
    }
  }
  setConnected(e) {
    this._$AM === void 0 && (this._$Cv = e, this._$AP?.(e));
  }
}
class G {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(e, t, s, i, n) {
    this.type = 1, this._$AH = c, this._$AN = void 0, this.element = e, this.name = t, this._$AM = i, this.options = n, s.length > 2 || s[0] !== "" || s[1] !== "" ? (this._$AH = Array(s.length - 1).fill(new String()), this.strings = s) : this._$AH = c;
  }
  _$AI(e, t = this, s, i) {
    const n = this.strings;
    let a = !1;
    if (n === void 0) e = T(this, e, t, 0), a = !O(e) || e !== this._$AH && e !== N, a && (this._$AH = e);
    else {
      const h = e;
      let d, p;
      for (e = n[0], d = 0; d < n.length - 1; d++) p = T(this, h[s + d], t, d), p === N && (p = this._$AH[d]), a ||= !O(p) || p !== this._$AH[d], p === c ? e = c : e !== c && (e += (p ?? "") + n[d + 1]), this._$AH[d] = p;
    }
    a && !i && this.j(e);
  }
  j(e) {
    e === c ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, e ?? "");
  }
}
class it extends G {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(e) {
    this.element[this.name] = e === c ? void 0 : e;
  }
}
class rt extends G {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(e) {
    this.element.toggleAttribute(this.name, !!e && e !== c);
  }
}
class at extends G {
  constructor(e, t, s, i, n) {
    super(e, t, s, i, n), this.type = 5;
  }
  _$AI(e, t = this) {
    if ((e = T(this, e, t, 0) ?? c) === N) return;
    const s = this._$AH, i = e === c && s !== c || e.capture !== s.capture || e.once !== s.once || e.passive !== s.passive, n = e !== c && (s === c || i);
    i && this.element.removeEventListener(this.name, this, s), n && this.element.addEventListener(this.name, this, e), this._$AH = e;
  }
  handleEvent(e) {
    typeof this._$AH == "function" ? this._$AH.call(this.options?.host ?? this.element, e) : this._$AH.handleEvent(e);
  }
}
class nt {
  constructor(e, t, s) {
    this.element = e, this.type = 6, this._$AN = void 0, this._$AM = t, this.options = s;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(e) {
    T(this, e);
  }
}
const ot = re.litHtmlPolyfillSupport;
ot?.(F, j), (re.litHtmlVersions ??= []).push("3.3.3");
const lt = (r, e, t) => {
  const s = t?.renderBefore ?? e;
  let i = s._$litPart$;
  if (i === void 0) {
    const n = t?.renderBefore ?? null;
    s._$litPart$ = i = new j(e.insertBefore(M(), n), n, void 0, t ?? {});
  }
  return i._$AI(r), i;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const ne = globalThis;
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
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(e), this._$Do = lt(t, this.renderRoot, this.renderOptions);
  }
  connectedCallback() {
    super.connectedCallback(), this._$Do?.setConnected(!0);
  }
  disconnectedCallback() {
    super.disconnectedCallback(), this._$Do?.setConnected(!1);
  }
  render() {
    return N;
  }
}
$._$litElement$ = !0, $.finalized = !0, ne.litElementHydrateSupport?.({ LitElement: $ });
const dt = ne.litElementPolyfillSupport;
dt?.({ LitElement: $ });
(ne.litElementVersions ??= []).push("4.2.2");
class q extends $ {
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
class ct extends q {
  constructor() {
    super(...arguments), this.fields = [
      { name: "title", selector: { text: {} } },
      { name: "show_images", selector: { boolean: {} } },
      { name: "show_actions", selector: { boolean: {} } }
    ], this.defaults = { show_images: !0, show_actions: !0 };
  }
}
class ht extends q {
  constructor() {
    super(...arguments), this.fields = [
      { name: "title", selector: { text: {} } },
      { name: "show_image", selector: { boolean: {} } },
      { name: "show_ingredients", selector: { boolean: {} } }
    ], this.defaults = { show_image: !0, show_ingredients: !1 };
  }
}
class pt extends q {
  constructor() {
    super(...arguments), this.fields = [
      { name: "title", selector: { text: {} } },
      { name: "show_added", selector: { boolean: {} } },
      { name: "show_skipped", selector: { boolean: {} } }
    ], this.defaults = { show_added: !0, show_skipped: !1 };
  }
}
class ut extends q {
  constructor() {
    super(...arguments), this.fields = [
      { name: "title", selector: { text: {} } },
      { name: "editable", selector: { boolean: {} } }
    ], this.defaults = { editable: !0 };
  }
}
const X = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"], Ne = [
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
], mt = ["omnivore", "vegetarian", "vegan", "pescatarian"], ft = ["small", "normal", "large"], L = "weeklymenu";
function K(r) {
  const e = /* @__PURE__ */ new Map();
  for (const t of Object.values(r.entities ?? {}))
    t.platform === L && t.translation_key && e.set(t.translation_key, t.entity_id);
  return e;
}
const g = (r) => typeof r == "string" && r !== "" ? r : void 0, _ = (r) => typeof r == "number" && Number.isFinite(r) ? r : void 0, f = (r) => Array.isArray(r) ? r.filter((e) => typeof e == "string") : [], v = (r) => typeof r == "object" && r !== null;
function gt(r) {
  return (v(r) && Array.isArray(r.groups) ? r.groups : []).filter(v).map((t) => {
    const s = Array.isArray(t.substitutions) ? t.substitutions : [], i = _(t.share) ?? 0, n = (a) => {
      if (!v(a)) return "";
      const h = _(a.amount), d = g(a.name);
      return h === void 0 || !d || i <= 0 || i >= 1 ? g(a.raw) ?? d ?? "" : [Math.round(h * i * 10) / 10, g(a.unit), d].filter((u) => u !== void 0).join(" ");
    };
    return {
      members: f(t.members),
      share: i,
      separatePans: t.separate_pans === !0,
      swaps: s.filter(v).map((a) => ({
        original: n(a.original),
        replacement: n(a.replacement)
      }))
    };
  });
}
function _t(r) {
  return Array.isArray(r) ? r.filter(v).filter((e) => typeof e.id == "string" && typeof e.title == "string").map((e) => ({
    id: e.id,
    title: e.title,
    ratings: Te(e.ratings),
    favoriteOf: f(e.favorite_of)
  })) : [];
}
function Te(r) {
  const e = {};
  if (v(r))
    for (const [t, s] of Object.entries(r))
      typeof s == "number" && s >= 1 && s <= 5 && (e[t] = s);
  return e;
}
function $t(r) {
  return Array.isArray(r) ? r.filter(v).filter((e) => typeof e.id == "string" && typeof e.title == "string").map((e) => ({
    id: e.id,
    title: e.title,
    image: g(e.image),
    url: g(e.url),
    rating: _(e.rating)
  })) : [];
}
function Pe(r, e, t = "") {
  const s = e ? r.states[e] : void 0;
  if (!s || ["unknown", "unavailable", ""].includes(s.state)) return;
  const i = s.attributes, n = g(i.date);
  if (n)
    return {
      entityId: s.entity_id,
      weekday: t,
      date: n,
      title: s.state,
      recipeId: g(i.recipe_id) ?? "",
      url: g(i.url),
      image: g(i.image),
      source: g(i.source),
      totalTime: _(i.total_time),
      servings: _(i.servings),
      tags: f(i.tags),
      ingredients: f(i.ingredients),
      locked: i.locked === !0,
      alternatives: _t(i.alternatives),
      split: gt(i.split),
      ratings: Te(i.ratings),
      favoriteOf: f(i.favorite_of)
    };
}
function ye(r) {
  const e = K(r), t = r.states[e.get("status") ?? ""], s = t?.state, i = t?.attributes ?? {}, n = [];
  for (const a of X) {
    const h = Pe(r, e.get(`weekday_${a}`), a);
    h && n.push(h);
  }
  return {
    status: s === "draft" || s === "confirmed" ? s : "none",
    weekStart: g(i.week_start),
    warnings: f(i.warnings),
    days: n
  };
}
function yt(r) {
  return Pe(r, K(r).get("today"));
}
function De(r) {
  const [e, t, s] = r.split("-").map(Number), i = new Date(Date.UTC(e, t - 1, s)), n = i.getUTCDay() || 7;
  i.setUTCDate(i.getUTCDate() + 4 - n);
  const a = Date.UTC(i.getUTCFullYear(), 0, 1);
  return Math.ceil(((i.getTime() - a) / 864e5 + 1) / 7);
}
function vt(r) {
  return `${Math.round(r * 100)} %`;
}
function bt(r) {
  const e = r.states[K(r).get("shopping") ?? ""], t = e?.attributes ?? {}, s = v(t.counts) ? t.counts : {};
  return {
    hasResult: !!e && !["unknown", "unavailable", ""].includes(e.state),
    weekStart: g(t.week_start),
    counts: {
      added: _(s.added) ?? 0,
      review: _(s.review) ?? 0,
      failed: _(s.failed) ?? 0,
      skipped: _(s.skipped) ?? 0,
      pending: _(s.pending) ?? 0
    },
    added: f(t.added),
    review: f(t.review),
    failed: f(t.failed),
    pending: f(t.pending),
    skipped: f(t.skipped),
    targets: f(t.targets),
    errors: f(t.errors)
  };
}
function U(r) {
  const e = r.states[K(r).get("family") ?? ""];
  return !e || ["unknown", "unavailable", ""].includes(e.state) ? { available: !1, members: [], dinnerDays: [] } : {
    available: !0,
    members: (Array.isArray(e.attributes.members) ? e.attributes.members : []).filter(v).map((i) => ({
      id: g(i.id) ?? "",
      name: g(i.name) ?? "",
      person: g(i.person),
      allergies: f(i.allergies),
      dislikes: f(i.dislikes),
      likes: f(i.likes),
      diet: g(i.diet) ?? "omnivore",
      portion: g(i.portion) ?? "normal",
      attends: f(i.attends),
      cookSeparately: i.cook_separately !== !1,
      child: i.child === !0,
      notify: g(i.notify) ?? "",
      favorites: $t(i.favorites)
    })).filter((i) => i.id && i.name),
    dinnerDays: f(e.attributes.dinner_days)
  };
}
function Re(r) {
  const [e, t, s] = r.split("-").map(Number);
  return new Date(Date.UTC(e, t - 1, s));
}
function ee(r, e) {
  const t = W(r), s = Re(e), i = { timeZone: "UTC" };
  return {
    weekday: new Intl.DateTimeFormat(t, { ...i, weekday: "short" }).format(s),
    date: new Intl.DateTimeFormat(t, { ...i, day: "numeric", month: "short" }).format(s)
  };
}
function wt(r, e) {
  return new Intl.DateTimeFormat(W(r), { timeZone: "UTC", weekday: "long" }).format(Re(e));
}
function kt(r, e) {
  const t = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"].indexOf(e);
  return t < 0 ? e : wt(r, `2026-11-${String(2 + t).padStart(2, "0")}`);
}
function ve(r, e) {
  const t = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"].indexOf(e);
  return t < 0 ? e : ee(r, `2026-11-${String(2 + t).padStart(2, "0")}`).weekday;
}
function Me(r, e) {
  const t = `source_${e.source}`, s = e.source ? o(r, t) : "";
  return l`<div class="meta">
    ${e.totalTime ? l`<span>${o(r, "minutes", { n: e.totalTime })}</span>` : c}
    ${e.tags.map((i) => l`<span class="tag">${Le(r, i)}</span>`)}
    ${s && !s.startsWith("source_") ? l`<span class="badge">${s}</span>` : c}
    ${e.split.length ? l`<span class="badge split" title=${o(r, "split")}>${o(r, "split")}</span>` : c}
    ${e.locked ? l`<span class="badge">${o(r, "locked")}</span>` : c}
  </div>`;
}
function Oe(r, e) {
  return e.length ? l`<div class="split-note">
    <strong>${o(r, "split")}</strong>
    ${e.map(
    (t) => l`<div>
        ${t.swaps.map(
      (s) => l`<div>
              ${o(r, "splitNote", {
        members: t.members.join(", ") + ` (${vt(t.share)})`,
        from: s.original,
        to: s.replacement
      })}
            </div>`
    )}
        ${t.separatePans ? l`<em>${o(r, "cleanPans")}</em>` : c}
      </div>`
  )}
  </div>` : c;
}
function Fe(r, e) {
  return e.length ? l`<div>
    <h4>${o(r, "ingredients")}</h4>
    <ul>
      ${e.map((t) => l`<li>${t}</li>`)}
    </ul>
  </div>` : c;
}
function Z(r) {
  return r && typeof r == "object" && "message" in r ? String(r.message) : String(r);
}
const I = ze`
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
  .main .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    flex: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--primary-color);
    color: var(--text-primary-color, #fff);
    font-weight: 500;
  }
  .taste {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 4px 8px;
    padding: 4px 0;
  }
  .taste select {
    max-width: 10em;
    width: auto;
  }
  .taste .stars {
    display: inline-flex;
  }
  .taste button.icon.on ha-icon {
    color: var(--state-icon-active-color, var(--primary-color));
  }
  .taste .liked {
    color: var(--secondary-text-color);
    font-size: 0.85em;
  }
  details.favorites {
    margin-top: 6px;
  }
  details.favorites summary {
    cursor: pointer;
    color: var(--secondary-text-color);
    font-size: 0.9em;
  }
  .fav {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 0;
    min-width: 0;
  }
  .fav .name {
    flex: 1;
    min-width: 0;
    overflow-wrap: anywhere;
  }
  .fav img {
    width: 32px;
    height: 32px;
    border-radius: 6px;
    object-fit: cover;
    flex: none;
  }
  .fav .stars-text {
    color: var(--secondary-text-color);
    font-size: 0.85em;
    white-space: nowrap;
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
`;
function oe(r, e) {
  const t = r.user?.id;
  if (t)
    return e.find((s) => s.person && r.states[s.person]?.attributes?.user_id === t);
}
function xt(r, e) {
  const t = e.filter((s) => r.ratings[s.id]).map((s) => `${s.name} ★${r.ratings[s.id]}`).join(", ");
  return `${r.favoriteOf.length ? "♥ " : ""}${r.title}${t ? ` (${t})` : ""}`;
}
function At(r) {
  return [...r].sort((e, t) => +(t.favoriteOf.length > 0) - +(e.favoriteOf.length > 0));
}
class St extends $ {
  static {
    this.properties = {
      hass: { attribute: !1 },
      dinner: { attribute: !1 },
      _member: { state: !0 },
      _error: { state: !0 }
    };
  }
  static {
    this.styles = I;
  }
  constructor() {
    super(), this._member = "", this._error = "";
  }
  async _call(e, t) {
    this._error = "";
    try {
      await this.hass.callService(L, e, t);
    } catch (s) {
      this._error = Z(s);
    }
  }
  render() {
    const e = this.dinner;
    if (!this.hass || !e?.recipeId) return c;
    const t = this.hass, s = U(t).members;
    if (!s.length) return c;
    const i = s.find((p) => p.id === this._member) ?? oe(t, s) ?? s[0], n = e.ratings[i.id] ?? 0, a = e.favoriteOf.includes(i.id), h = e.favoriteOf.map((p) => s.find((u) => u.id === p)?.name).filter(Boolean), d = (p) => p === 1 ? o(t, "starOne") : o(t, "starsN", { n: p });
    return l`<div class="taste">
      ${s.length > 1 ? l`<select
            aria-label=${o(t, "rateAs")}
            .value=${i.id}
            @change=${(p) => this._member = p.target.value}
          >
            ${s.map((p) => l`<option value=${p.id} ?selected=${p.id === i.id}>${p.name}</option>`)}
          </select>` : c}
      <span class="stars" role="group" aria-label=${o(t, "ratingGroup")}>
        ${[1, 2, 3, 4, 5].map(
      (p) => l`<button
            class="icon ${p <= n ? "on" : ""}"
            title=${d(p)}
            aria-label=${d(p)}
            aria-pressed=${p === n ? "true" : "false"}
            @click=${() => void this._call("rate_recipe", { member: i.id, recipe_id: e.recipeId, rating: p === n ? 0 : p })}
          >
            <ha-icon icon=${p <= n ? "mdi:star" : "mdi:star-outline"}></ha-icon>
          </button>`
    )}
      </span>
      <button
        class="icon heart ${a ? "on" : ""}"
        title=${a ? o(t, "favoriteRemove") : o(t, "favoriteAdd")}
        aria-label=${a ? o(t, "favoriteRemove") : o(t, "favoriteAdd")}
        aria-pressed=${a ? "true" : "false"}
        @click=${() => void this._call("favorite_recipe", { member: i.id, recipe_id: e.recipeId, favorite: !a })}
      >
        <ha-icon icon=${a ? "mdi:heart" : "mdi:heart-outline"}></ha-icon>
      </button>
      ${h.length ? l`<span class="liked">${o(t, "favoriteOf", { names: h.join(", ") })}</span>` : c}
      ${this._error ? l`<span class="banner error">${o(t, "error", { error: this._error })}</span>` : c}
    </div>`;
  }
}
const te = new Set(Ne);
function Et(r) {
  return Object.values(r.states).filter((e) => e.entity_id.startsWith("person.")).map((e) => ({ id: e.entity_id, name: Ue(r, e.entity_id) })).sort((e, t) => e.name.localeCompare(t.name));
}
function Ue(r, e) {
  const t = r.states[e]?.attributes?.friendly_name;
  return typeof t == "string" && t ? t : e.replace(/^person\./, "").replace(/_/g, " ");
}
function Ct(r, e, t) {
  const s = t ? r.states[t]?.attributes?.entity_picture : void 0;
  return typeof s == "string" && s ? l`<img class="avatar" src=${s} alt="" />` : l`<span class="avatar" aria-hidden="true">${[...e.trim()][0]?.toUpperCase() ?? "?"}</span>`;
}
const Y = (r) => r.split(",").map((e) => e.trim()).filter(Boolean);
function be(r, e) {
  return r ? {
    id: r.id,
    name: r.name,
    person: r.person ?? "",
    hadPerson: !!r.person,
    filledName: "",
    allergies: r.allergies.filter((t) => te.has(t)),
    otherAllergies: r.allergies.filter((t) => !te.has(t)).join(", "),
    dislikes: r.dislikes.join(", "),
    likes: r.likes.join(", "),
    diet: r.diet,
    portion: r.portion,
    attends: [...r.attends],
    cookSeparately: r.cookSeparately,
    child: r.child,
    notify: r.notify
  } : {
    id: "",
    name: "",
    person: "",
    hadPerson: !1,
    filledName: "",
    allergies: [],
    otherAllergies: "",
    dislikes: "",
    likes: "",
    diet: "omnivore",
    portion: "normal",
    attends: [...e],
    cookSeparately: !0,
    child: !1,
    notify: ""
  };
}
class Nt extends $ {
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
    this.styles = I;
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
    return this.hass ? 2 + U(this.hass).members.length : 3;
  }
  // --- actions ----------------------------------------------------------------------
  _set(e) {
    this._draft && (this._draft = { ...this._draft, ...e });
  }
  /** Pick a Home Assistant person. The name follows the person unless it was typed by hand. */
  _pickPerson(e) {
    const t = this._draft;
    if (!t) return;
    const s = e ? Ue(this.hass, e) : "", i = t.name.trim() === "" || t.name === t.filledName;
    this._draft = {
      ...t,
      person: e,
      name: i && s ? s : t.name,
      filledName: i && s ? s : t.filledName
    };
  }
  _toggle(e, t) {
    if (!this._draft) return;
    const s = this._draft[e];
    this._set({ [e]: s.includes(t) ? s.filter((i) => i !== t) : [...s, t] });
  }
  async _run(e, t) {
    this._busy = !0, this._error = "";
    try {
      return await this.hass.callService(L, e, t), !0;
    } catch (s) {
      return this._error = Z(s), !1;
    } finally {
      this._busy = !1;
    }
  }
  async _save() {
    const e = this._draft;
    if (!e || !e.name.trim() || !e.attends.length) return;
    const t = {
      name: e.name.trim(),
      allergies: [...e.allergies, ...Y(e.otherAllergies)],
      dislikes: Y(e.dislikes),
      likes: Y(e.likes),
      diet: e.diet,
      portion: e.portion,
      attends: X.filter((s) => e.attends.includes(s)),
      cook_separately: e.cookSeparately,
      child: e.child,
      notify: e.notify.trim()
    };
    e.id && (t.id = e.id), e.person ? t.person = e.person : e.hadPerson && (t.person = null), await this._run("set_member", t) && (this._draft = null);
  }
  async _removeFavorite(e, t) {
    await this._run("favorite_recipe", { member: e.id, recipe_id: t, favorite: !1 });
  }
  async _remove() {
    const e = this._draft;
    !e?.id || !window.confirm(o(this.hass, "famRemoveAsk", { name: e.name })) || await this._run("remove_member", { id: e.id }) && (this._draft = null);
  }
  // --- rendering --------------------------------------------------------------------------
  render() {
    if (!this.hass) return l``;
    const e = this.hass, t = U(e), s = this._config.title ?? o(e, "familyTitle");
    if (!t.available)
      return l`<ha-card .header=${s}><div class="empty">${o(e, "famNoFamily")}</div></ha-card>`;
    const i = oe(e, t.members), n = this._config.editable !== !1 && !i?.child, a = t.dinnerDays.length ? t.dinnerDays : [...X];
    return l`<ha-card .header=${s}>
      ${this._error ? l`<div class="banner error">${o(e, "error", { error: this._error })}</div>` : c}
      ${t.members.length ? t.members.map((h) => this._renderMember(h, t.dinnerDays, n, a, i)) : l`<div class="empty">${o(e, "famNone")}</div>`}
      ${this._draft && !this._draft.id ? this._renderForm(this._draft, a) : c}
      ${n && !this._draft ? l`<div class="foot">
            <button class="primary" ?disabled=${this._busy} @click=${() => this._draft = be(void 0, a)}>
              ${o(e, "famAdd")}
            </button>
          </div>` : c}
    </ha-card>`;
  }
  _renderMember(e, t, s, i, n) {
    const a = this.hass, h = this._draft?.id === e.id, d = i.filter((u) => e.attends.includes(u)), p = d.length === i.length;
    return l`<div class="member">
      <div class="main">
        ${Ct(a, e.name, e.person)}
        <div style="flex:1;min-width:0">
          <div class="title">${e.name}</div>
          <div class="meta">
            ${e.child ? l`<span class="badge">${o(a, "famChildBadge")}</span>` : c}
            ${e.diet !== "omnivore" ? l`<span class="badge">${o(a, `diet_${e.diet}`)}</span>` : c}
            ${e.portion !== "normal" ? l`<span class="badge">${o(a, `portion_${e.portion}`)}</span>` : c}
            ${e.allergies.map((u) => l`<span class="tag allergy">${te.has(u) ? o(a, `allergen_${u}`) : u}</span>`)}
            ${e.dislikes.length ? l`<span>${e.dislikes.join(", ")}</span>` : c}
            <span>${p ? o(a, "famEveryDay") : d.map((u) => ve(a, u)).join(", ")}</span>
          </div>
          ${e.favorites.length ? this._renderFavorites(e, s || this._config.editable !== !1 && n?.id === e.id, !1) : c}
        </div>
        ${s && !h ? l`<button ?disabled=${this._busy} @click=${() => this._draft = be(e, t)}>
              ${o(a, "famEdit")}
            </button>` : c}
      </div>
      ${h && this._draft ? this._renderForm(this._draft, i, e) : c}
    </div>`;
  }
  /** A member's favorite recipes, folded out from a summary line, each with a button to remove it. */
  _renderFavorites(e, t, s) {
    const i = this.hass;
    return l`<details class="favorites" ?open=${s}>
      <summary>${o(i, "famFavorites", { n: e.favorites.length })}</summary>
      ${e.favorites.length ? e.favorites.map(
      (n) => l`<div class="fav">
              ${n.image ? l`<img src=${n.image} alt="" loading="lazy" />` : c}
              <span class="name">
                ${n.url ? l`<a href=${n.url} target="_blank" rel="noopener noreferrer" title=${o(i, "openRecipe")}>${n.title}</a>` : n.title}
              </span>
              ${n.rating ? l`<span class="stars-text">★ ${n.rating}</span>` : c}
              ${t ? l`<button
                    class="icon"
                    ?disabled=${this._busy}
                    title=${o(i, "famRemoveFavorite", { title: n.title })}
                    aria-label=${o(i, "famRemoveFavorite", { title: n.title })}
                    @click=${() => this._removeFavorite(e, n.id)}
                  >
                    <ha-icon icon="mdi:close"></ha-icon>
                  </button>` : c}
            </div>`
    ) : l`<div class="empty">${o(i, "famNoFavorites")}</div>`}
    </details>`;
  }
  _renderForm(e, t, s) {
    const i = this.hass, n = e.name.trim() !== "" && e.attends.length > 0, a = (d, p, u) => l`<label class="field">
      <span>${o(i, d)}</span>
      <input
        type="text"
        .value=${p}
        @input=${(m) => this._set({ [u]: m.target.value })}
      />
    </label>`, h = Et(i);
    return l`<form class="form" @submit=${(d) => d.preventDefault()}>
      ${h.length || e.person ? l`<label class="field">
            <span>${o(i, "famPerson")}</span>
            <select .value=${e.person} @change=${(d) => this._pickPerson(d.target.value)}>
              <option value="" ?selected=${!e.person}>${o(i, "famNoPerson")}</option>
              ${h.map((d) => l`<option value=${d.id} ?selected=${e.person === d.id}>${d.name}</option>`)}
              ${e.person && !h.some((d) => d.id === e.person) ? l`<option value=${e.person} selected>${e.person}</option>` : c}
            </select>
          </label>` : c}
      ${a("famName", e.name, "name")}
      <fieldset>
        <legend>${o(i, "famAllergies")}</legend>
        <div class="checks">
          ${Ne.map(
      (d) => l`<label class="check">
              <input type="checkbox" .checked=${e.allergies.includes(d)} @change=${() => this._toggle("allergies", d)} />
              ${o(i, `allergen_${d}`)}
            </label>`
    )}
        </div>
      </fieldset>
      ${a("famOtherAllergies", e.otherAllergies, "otherAllergies")} ${a("famDislikes", e.dislikes, "dislikes")}
      ${a("famLikes", e.likes, "likes")} ${a("famNotify", e.notify, "notify")}
      <div class="row">
        <label class="field">
          <span>${o(i, "famDiet")}</span>
          <select .value=${e.diet} @change=${(d) => this._set({ diet: d.target.value })}>
            ${mt.map((d) => l`<option value=${d} ?selected=${e.diet === d}>${o(i, `diet_${d}`)}</option>`)}
          </select>
        </label>
        <label class="field">
          <span>${o(i, "famPortion")}</span>
          <select .value=${e.portion} @change=${(d) => this._set({ portion: d.target.value })}>
            ${ft.map((d) => l`<option value=${d} ?selected=${e.portion === d}>${o(i, `portion_${d}`)}</option>`)}
          </select>
        </label>
      </div>
      <fieldset>
        <legend>${o(i, "famDays")}</legend>
        <div class="checks">
          ${t.map(
      (d) => l`<label class="check">
              <input type="checkbox" .checked=${e.attends.includes(d)} @change=${() => this._toggle("attends", d)} />
              ${ve(i, d)}
            </label>`
    )}
        </div>
        ${e.attends.length ? c : l`<small class="hint-error">${o(i, "famNoDays")}</small>`}
      </fieldset>
      <label class="check">
        <input
          type="checkbox"
          .checked=${e.child}
          @change=${(d) => this._set({ child: d.target.checked })}
        />
        ${o(i, "famChild")}
      </label>
      <label class="check">
        <input
          type="checkbox"
          .checked=${e.cookSeparately}
          @change=${(d) => this._set({ cookSeparately: d.target.checked })}
        />
        ${o(i, "famCookSeparately")}
      </label>
      ${s ? this._renderFavorites(s, !0, !0) : c}
      <small>${o(i, "famAppliesLater")}</small>
      <div class="row">
        <button class="primary" type="button" ?disabled=${this._busy || !n} @click=${() => this._save()}>${o(i, "famSave")}</button>
        <button type="button" ?disabled=${this._busy} @click=${() => this._draft = null}>${o(i, "famCancel")}</button>
        ${e.id ? l`<button type="button" ?disabled=${this._busy} @click=${() => this._remove()}>${o(i, "famRemove")}</button>` : c}
      </div>
    </form>`;
  }
}
class Tt extends $ {
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
    this.styles = I;
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
    return this.hass ? 2 + ye(this.hass).days.length : 4;
  }
  // --- actions ------------------------------------------------------------------
  async _call(e, t = {}) {
    this._busy = !0, this._error = "";
    try {
      await this.hass.callService(L, e, t);
    } catch (s) {
      this._error = Z(s);
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
    const e = this.hass, t = ye(e), s = t.status === "confirmed", i = oe(e, U(e).members)?.child === !0, n = this._config.show_actions !== !1 && !s && !i, a = [...new Set(t.warnings.map((h) => je(e, h, (d) => kt(e, d))))];
    return l`<ha-card .header=${this._config.title ?? o(e, "menuTitle")}>
      <div class="head">
        <span>${t.weekStart ? o(e, "week", { n: De(t.weekStart) }) : ""}</span>
        <span class="chip ${t.status}">${o(e, `status_${t.status}`)}</span>
      </div>
      ${a.map((h) => l`<div class="banner warning">${h}</div>`)}
      ${this._error ? l`<div class="banner error">${o(e, "error", { error: this._error })}</div>` : c}
      ${this._busy ? l`<div class="banner">${o(e, "working")}</div>` : c}
      ${t.days.length ? t.days.map((h) => this._renderDay(h, t, n)) : l`<div class="empty">${o(e, "noMenu")}</div>`}
      ${s && this._config.show_actions !== !1 && !i ? l`<div class="banner">${o(e, "confirmedNote")}</div>` : c}
      ${this._renderFooter(t, n)}
    </ha-card>`;
  }
  _renderFooter(e, t) {
    if (!t) return c;
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
          </button>` : c}
    </div>`;
  }
  _renderDay(e, t, s) {
    const i = this.hass, n = ee(i, e.date), a = this._open.has(e.date), h = e.url ? l`<a href=${e.url} target="_blank" rel="noopener noreferrer" title=${o(i, "openRecipe")}>${e.title}</a>` : e.title, d = t.days.filter((p) => p.date !== e.date && !p.locked);
    return l`<div class="day">
      <div class="when">
        <div class="wd">${n.weekday}</div>
        <div class="dt">${n.date}</div>
      </div>
      <div class="main">
        ${this._config.show_images !== !1 && e.image ? l`<img src=${e.image} alt="" loading="lazy" />` : c}
        <div>
          <div class="title">${h}</div>
          ${Me(i, e)}
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
            </button>` : c}
        <button
          class="icon"
          title=${a ? o(i, "hide") : o(i, "show")}
          aria-label=${a ? o(i, "hide") : o(i, "show")}
          aria-expanded=${a ? "true" : "false"}
          @click=${() => this._toggle(e.date)}
        >
          <ha-icon icon=${a ? "mdi:chevron-up" : "mdi:chevron-down"}></ha-icon>
        </button>
      </div>
      ${a ? this._renderMore(e, d, s) : c}
    </div>`;
  }
  _renderMore(e, t, s) {
    const i = this.hass, n = U(i).members;
    return l`<div class="more">
      ${this._config.show_actions !== !1 ? l`<weeklymenu-taste .hass=${i} .dinner=${e}></weeklymenu-taste>` : c}
      ${Oe(i, e.split)} ${Fe(i, e.ingredients)}
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
                    ${At(e.alternatives).map(
      (a) => l`<option value=${a.id}>${xt(a, n)}</option>`
    )}
                  </select>` : c}
              ${t.length && !e.locked ? l`<select
                    ?disabled=${this._busy}
                    aria-label=${o(i, "swapWith")}
                    @change=${(a) => this._swap(e, a)}
                  >
                    <option value="">${o(i, "swapWith")}</option>
                    ${t.map((a) => {
      const h = ee(i, a.date);
      return l`<option value=${a.date}>${h.weekday} ${h.date}: ${a.title}</option>`;
    })}
                  </select>` : c}
            </div>` : c}
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
class Pt extends $ {
  static {
    this.properties = {
      hass: { attribute: !1 },
      _config: { state: !0 },
      _busy: { state: !0 },
      _error: { state: !0 }
    };
  }
  static {
    this.styles = I;
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
      await this.hass.callService(L, "add_to_shopping", {});
    } catch (e) {
      this._error = Z(e);
    } finally {
      this._busy = !1;
    }
  }
  render() {
    if (!this.hass) return l``;
    const e = this.hass, t = bt(e), s = this._config.title ?? o(e, "shoppingTitle");
    if (!t.hasResult)
      return l`<ha-card .header=${s}><div class="empty">${o(e, "shopNothing")}</div></ha-card>`;
    const i = t.counts.failed + t.counts.pending, n = t.errors.some((h) => h.endsWith(": auth_failed")), a = [
      ...new Set(t.errors.filter((h) => !(n && h === "reauth_required")).map((h) => Ie(e, h)))
    ];
    return l`<ha-card .header=${s}>
      <div class="head">
        <span>
          ${t.weekStart ? o(e, "week", { n: De(t.weekStart) }) : ""}
          ${t.targets.length ? ` · ${o(e, "shopTargets", { targets: t.targets.join(", ") })}` : ""}
        </span>
      </div>
      <div class="head chips">
        ${we.filter((h) => t.counts[h.key] > 0).map(
      (h) => l`<span class="chip ${h.css === "warning" ? "draft" : ""}">${o(e, h.label)}: ${t.counts[h.key]}</span>`
    )}
      </div>
      ${a.map((h) => l`<div class="banner warning">${h}</div>`)}
      ${this._error ? l`<div class="banner error">${o(e, "error", { error: this._error })}</div>` : c}
      ${we.map((h) => this._renderGroup(h, t[h.key]))}
      ${i ? l`<div class="foot">
            <button class="primary" ?disabled=${this._busy} @click=${() => this._retry()}>${o(e, "shopRetry")}</button>
          </div>` : c}
    </ha-card>`;
  }
  _renderGroup(e, t) {
    if (!t.length || e.key === "added" && this._config.show_added === !1 || e.key === "skipped" && !this._config.show_skipped) return c;
    const s = e.key === "review" || e.key === "failed" || e.key === "pending";
    return l`<details class="group ${e.css}" ?open=${s}>
      <summary>${o(this.hass, e.label)} (${t.length})</summary>
      <ul>
        ${t.map((i) => l`<li>${i}</li>`)}
      </ul>
    </details>`;
  }
}
class Dt extends $ {
  static {
    this.properties = {
      hass: { attribute: !1 },
      _config: { state: !0 }
    };
  }
  static {
    this.styles = [
      I
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
    const e = this.hass, t = yt(e), s = this._config.title ?? o(e, "todayTitle");
    if (!t)
      return l`<ha-card .header=${s}><div class="empty">${o(e, "noDinner")}</div></ha-card>`;
    const i = t.url ? l`<a href=${t.url} target="_blank" rel="noopener noreferrer" title=${o(e, "openRecipe")}>${t.title}</a>` : t.title;
    return l`<ha-card .header=${s}>
      <div class="day" style="grid-template-columns: 1fr">
        <div class="main">
          ${this._config.show_image !== !1 && t.image ? l`<img src=${t.image} alt="" loading="lazy" style="width:72px;height:72px" />` : c}
          <div>
            <div class="title">${i}</div>
            ${Me(e, t)}
          </div>
        </div>
        <div class="more" style="padding-left:0">
          <weeklymenu-taste .hass=${e} .dinner=${t}></weeklymenu-taste>
          ${Oe(e, t.split)}
          ${this._config.show_ingredients ? Fe(e, t.ingredients) : c}
        </div>
      </div>
    </ha-card>`;
  }
}
function b(r, e) {
  customElements.get(r) || customElements.define(r, e);
}
b("weeklymenu-taste", St);
b("weeklymenu-menu-card", Tt);
b("weeklymenu-menu-card-editor", ct);
b("weeklymenu-today-card", Dt);
b("weeklymenu-today-card-editor", ht);
b("weeklymenu-shopping-card", Pt);
b("weeklymenu-shopping-card-editor", pt);
b("weeklymenu-family-card", Nt);
b("weeklymenu-family-card-editor", ut);
const k = { language: W({ language: navigator.language }) };
window.customCards = window.customCards ?? [];
window.customCards.push(
  {
    type: "weeklymenu-menu-card",
    name: o(k, "cardMenuName"),
    description: o(k, "cardMenuDescription"),
    preview: !0
  },
  {
    type: "weeklymenu-today-card",
    name: o(k, "cardTodayName"),
    description: o(k, "cardTodayDescription"),
    preview: !0
  },
  {
    type: "weeklymenu-shopping-card",
    name: o(k, "cardShoppingName"),
    description: o(k, "cardShoppingDescription"),
    preview: !0
  },
  {
    type: "weeklymenu-family-card",
    name: o(k, "cardFamilyName"),
    description: o(k, "cardFamilyDescription"),
    preview: !0
  }
);
