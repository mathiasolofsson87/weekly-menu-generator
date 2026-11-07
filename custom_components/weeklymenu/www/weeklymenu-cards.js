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
  return (R[W(r)][e] ?? R.en[e]).replace(/\{(\w+)\}/g, (s, a) => String(t[a] ?? `{${a}}`));
}
function Ue(r, e, t) {
  const [i, s = ""] = e.split(":"), a = `warn_${i}`;
  if (!(a in R.en)) return e;
  const n = i === "no_recipe" || i === "split_limit_exceeded" ? t(s) : s;
  return o(r, a, { detail: n });
}
function je(r, e) {
  const t = `tag_${e}`;
  return t in R.en ? o(r, t) : e.replace(/_/g, " ");
}
function Ie(r, e) {
  const [t, i] = e.includes(": ") ? e.split(": ", 2) : ["", e], s = `err_${i}`;
  return s in R.en ? o(r, s, { store: t.toUpperCase() }) : e;
}
/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const H = globalThis, se = H.ShadowRoot && (H.ShadyCSS === void 0 || H.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, ie = Symbol(), le = /* @__PURE__ */ new WeakMap();
let ke = class {
  constructor(e, t, i) {
    if (this._$cssResult$ = !0, i !== ie) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = e, this.t = t;
  }
  get styleSheet() {
    let e = this.o;
    const t = this.t;
    if (se && e === void 0) {
      const i = t !== void 0 && t.length === 1;
      i && (e = le.get(t)), e === void 0 && ((this.o = e = new CSSStyleSheet()).replaceSync(this.cssText), i && le.set(t, e));
    }
    return e;
  }
  toString() {
    return this.cssText;
  }
};
const Le = (r) => new ke(typeof r == "string" ? r : r + "", void 0, ie), He = (r, ...e) => {
  const t = r.length === 1 ? r[0] : e.reduce((i, s, a) => i + ((n) => {
    if (n._$cssResult$ === !0) return n.cssText;
    if (typeof n == "number") return n;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + n + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(s) + r[a + 1], r[0]);
  return new ke(t, r, ie);
}, ze = (r, e) => {
  if (se) r.adoptedStyleSheets = e.map((t) => t instanceof CSSStyleSheet ? t : t.styleSheet);
  else for (const t of e) {
    const i = document.createElement("style"), s = H.litNonce;
    s !== void 0 && i.setAttribute("nonce", s), i.textContent = t.cssText, r.appendChild(i);
  }
}, de = se ? (r) => r : (r) => r instanceof CSSStyleSheet ? ((e) => {
  let t = "";
  for (const i of e.cssRules) t += i.cssText;
  return Le(t);
})(r) : r;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: Be, defineProperty: We, getOwnPropertyDescriptor: Ve, getOwnPropertyNames: Ge, getOwnPropertySymbols: qe, getPrototypeOf: Ke } = Object, V = globalThis, ce = V.trustedTypes, Ze = ce ? ce.emptyScript : "", Je = V.reactiveElementPolyfillSupport, D = (r, e) => r, Q = { toAttribute(r, e) {
  switch (e) {
    case Boolean:
      r = r ? Ze : null;
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
} }, xe = (r, e) => !Be(r, e), he = { attribute: !0, type: String, converter: Q, reflect: !1, useDefault: !1, hasChanged: xe };
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
      const i = Symbol(), s = this.getPropertyDescriptor(e, i, t);
      s !== void 0 && We(this.prototype, e, s);
    }
  }
  static getPropertyDescriptor(e, t, i) {
    const { get: s, set: a } = Ve(this.prototype, e) ?? { get() {
      return this[t];
    }, set(n) {
      this[t] = n;
    } };
    return { get: s, set(n) {
      const h = s?.call(this);
      a?.call(this, n), this.requestUpdate(e, h, i);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(e) {
    return this.elementProperties.get(e) ?? he;
  }
  static _$Ei() {
    if (this.hasOwnProperty(D("elementProperties"))) return;
    const e = Ke(this);
    e.finalize(), e.l !== void 0 && (this.l = [...e.l]), this.elementProperties = new Map(e.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(D("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(D("properties"))) {
      const t = this.properties, i = [...Ge(t), ...qe(t)];
      for (const s of i) this.createProperty(s, t[s]);
    }
    const e = this[Symbol.metadata];
    if (e !== null) {
      const t = litPropertyMetadata.get(e);
      if (t !== void 0) for (const [i, s] of t) this.elementProperties.set(i, s);
    }
    this._$Eh = /* @__PURE__ */ new Map();
    for (const [t, i] of this.elementProperties) {
      const s = this._$Eu(t, i);
      s !== void 0 && this._$Eh.set(s, t);
    }
    this.elementStyles = this.finalizeStyles(this.styles);
  }
  static finalizeStyles(e) {
    const t = [];
    if (Array.isArray(e)) {
      const i = new Set(e.flat(1 / 0).reverse());
      for (const s of i) t.unshift(de(s));
    } else e !== void 0 && t.push(de(e));
    return t;
  }
  static _$Eu(e, t) {
    const i = t.attribute;
    return i === !1 ? void 0 : typeof i == "string" ? i : typeof e == "string" ? e.toLowerCase() : void 0;
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
    for (const i of t.keys()) this.hasOwnProperty(i) && (e.set(i, this[i]), delete this[i]);
    e.size > 0 && (this._$Ep = e);
  }
  createRenderRoot() {
    const e = this.shadowRoot ?? this.attachShadow(this.constructor.shadowRootOptions);
    return ze(e, this.constructor.elementStyles), e;
  }
  connectedCallback() {
    this.renderRoot ??= this.createRenderRoot(), this.enableUpdating(!0), this._$EO?.forEach((e) => e.hostConnected?.());
  }
  enableUpdating(e) {
  }
  disconnectedCallback() {
    this._$EO?.forEach((e) => e.hostDisconnected?.());
  }
  attributeChangedCallback(e, t, i) {
    this._$AK(e, i);
  }
  _$ET(e, t) {
    const i = this.constructor.elementProperties.get(e), s = this.constructor._$Eu(e, i);
    if (s !== void 0 && i.reflect === !0) {
      const a = (i.converter?.toAttribute !== void 0 ? i.converter : Q).toAttribute(t, i.type);
      this._$Em = e, a == null ? this.removeAttribute(s) : this.setAttribute(s, a), this._$Em = null;
    }
  }
  _$AK(e, t) {
    const i = this.constructor, s = i._$Eh.get(e);
    if (s !== void 0 && this._$Em !== s) {
      const a = i.getPropertyOptions(s), n = typeof a.converter == "function" ? { fromAttribute: a.converter } : a.converter?.fromAttribute !== void 0 ? a.converter : Q;
      this._$Em = s;
      const h = n.fromAttribute(t, a.type);
      this[s] = h ?? this._$Ej?.get(s) ?? h, this._$Em = null;
    }
  }
  requestUpdate(e, t, i, s = !1, a) {
    if (e !== void 0) {
      const n = this.constructor;
      if (s === !1 && (a = this[e]), i ??= n.getPropertyOptions(e), !((i.hasChanged ?? xe)(a, t) || i.useDefault && i.reflect && a === this._$Ej?.get(e) && !this.hasAttribute(n._$Eu(e, i)))) return;
      this.C(e, t, i);
    }
    this.isUpdatePending === !1 && (this._$ES = this._$EP());
  }
  C(e, t, { useDefault: i, reflect: s, wrapped: a }, n) {
    i && !(this._$Ej ??= /* @__PURE__ */ new Map()).has(e) && (this._$Ej.set(e, n ?? t ?? this[e]), a !== !0 || n !== void 0) || (this._$AL.has(e) || (this.hasUpdated || i || (t = void 0), this._$AL.set(e, t)), s === !0 && this._$Em !== e && (this._$Eq ??= /* @__PURE__ */ new Set()).add(e));
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
        for (const [s, a] of this._$Ep) this[s] = a;
        this._$Ep = void 0;
      }
      const i = this.constructor.elementProperties;
      if (i.size > 0) for (const [s, a] of i) {
        const { wrapped: n } = a, h = this[s];
        n !== !0 || this._$AL.has(s) || h === void 0 || this.C(s, void 0, a, h);
      }
    }
    let e = !1;
    const t = this._$AL;
    try {
      e = this.shouldUpdate(t), e ? (this.willUpdate(t), this._$EO?.forEach((i) => i.hostUpdate?.()), this.update(t)) : this._$EM();
    } catch (i) {
      throw e = !1, this._$EM(), i;
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
C.elementStyles = [], C.shadowRootOptions = { mode: "open" }, C[D("elementProperties")] = /* @__PURE__ */ new Map(), C[D("finalized")] = /* @__PURE__ */ new Map(), Je?.({ ReactiveElement: C }), (V.reactiveElementVersions ??= []).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const re = globalThis, pe = (r) => r, z = re.trustedTypes, ue = z ? z.createPolicy("lit-html", { createHTML: (r) => r }) : void 0, Ae = "$lit$", x = `lit$${Math.random().toFixed(9).slice(2)}$`, Se = "?" + x, Ye = `<${Se}>`, E = document, M = () => E.createComment(""), O = (r) => r === null || typeof r != "object" && typeof r != "function", ae = Array.isArray, Qe = (r) => ae(r) || typeof r?.[Symbol.iterator] == "function", J = `[ 	
\f\r]`, P = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, me = /-->/g, ge = />/g, A = RegExp(`>|${J}(?:([^\\s"'>=/]+)(${J}*=${J}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`, "g"), fe = /'/g, _e = /"/g, Ee = /^(?:script|style|textarea|title)$/i, Xe = (r) => (e, ...t) => ({ _$litType$: r, strings: e, values: t }), l = Xe(1), N = Symbol.for("lit-noChange"), c = Symbol.for("lit-nothing"), $e = /* @__PURE__ */ new WeakMap(), S = E.createTreeWalker(E, 129);
function Ce(r, e) {
  if (!ae(r) || !r.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return ue !== void 0 ? ue.createHTML(e) : e;
}
const et = (r, e) => {
  const t = r.length - 1, i = [];
  let s, a = e === 2 ? "<svg>" : e === 3 ? "<math>" : "", n = P;
  for (let h = 0; h < t; h++) {
    const d = r[h];
    let p, u, m = -1, y = 0;
    for (; y < d.length && (n.lastIndex = y, u = n.exec(d), u !== null); ) y = n.lastIndex, n === P ? u[1] === "!--" ? n = me : u[1] !== void 0 ? n = ge : u[2] !== void 0 ? (Ee.test(u[2]) && (s = RegExp("</" + u[2], "g")), n = A) : u[3] !== void 0 && (n = A) : n === A ? u[0] === ">" ? (n = s ?? P, m = -1) : u[1] === void 0 ? m = -2 : (m = n.lastIndex - u[2].length, p = u[1], n = u[3] === void 0 ? A : u[3] === '"' ? _e : fe) : n === _e || n === fe ? n = A : n === me || n === ge ? n = P : (n = A, s = void 0);
    const w = n === A && r[h + 1].startsWith("/>") ? " " : "";
    a += n === P ? d + Ye : m >= 0 ? (i.push(p), d.slice(0, m) + Ae + d.slice(m) + x + w) : d + x + (m === -2 ? h : w);
  }
  return [Ce(r, a + (r[t] || "<?>") + (e === 2 ? "</svg>" : e === 3 ? "</math>" : "")), i];
};
class F {
  constructor({ strings: e, _$litType$: t }, i) {
    let s;
    this.parts = [];
    let a = 0, n = 0;
    const h = e.length - 1, d = this.parts, [p, u] = et(e, t);
    if (this.el = F.createElement(p, i), S.currentNode = this.el.content, t === 2 || t === 3) {
      const m = this.el.content.firstChild;
      m.replaceWith(...m.childNodes);
    }
    for (; (s = S.nextNode()) !== null && d.length < h; ) {
      if (s.nodeType === 1) {
        if (s.hasAttributes()) for (const m of s.getAttributeNames()) if (m.endsWith(Ae)) {
          const y = u[n++], w = s.getAttribute(m).split(x), L = /([.?@])?(.*)/.exec(y);
          d.push({ type: 1, index: a, name: L[2], strings: w, ctor: L[1] === "." ? st : L[1] === "?" ? it : L[1] === "@" ? rt : G }), s.removeAttribute(m);
        } else m.startsWith(x) && (d.push({ type: 6, index: a }), s.removeAttribute(m));
        if (Ee.test(s.tagName)) {
          const m = s.textContent.split(x), y = m.length - 1;
          if (y > 0) {
            s.textContent = z ? z.emptyScript : "";
            for (let w = 0; w < y; w++) s.append(m[w], M()), S.nextNode(), d.push({ type: 2, index: ++a });
            s.append(m[y], M());
          }
        }
      } else if (s.nodeType === 8) if (s.data === Se) d.push({ type: 2, index: a });
      else {
        let m = -1;
        for (; (m = s.data.indexOf(x, m + 1)) !== -1; ) d.push({ type: 7, index: a }), m += x.length - 1;
      }
      a++;
    }
  }
  static createElement(e, t) {
    const i = E.createElement("template");
    return i.innerHTML = e, i;
  }
}
function T(r, e, t = r, i) {
  if (e === N) return e;
  let s = i !== void 0 ? t._$Co?.[i] : t._$Cl;
  const a = O(e) ? void 0 : e._$litDirective$;
  return s?.constructor !== a && (s?._$AO?.(!1), a === void 0 ? s = void 0 : (s = new a(r), s._$AT(r, t, i)), i !== void 0 ? (t._$Co ??= [])[i] = s : t._$Cl = s), s !== void 0 && (e = T(r, s._$AS(r, e.values), s, i)), e;
}
class tt {
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
    const { el: { content: t }, parts: i } = this._$AD, s = (e?.creationScope ?? E).importNode(t, !0);
    S.currentNode = s;
    let a = S.nextNode(), n = 0, h = 0, d = i[0];
    for (; d !== void 0; ) {
      if (n === d.index) {
        let p;
        d.type === 2 ? p = new U(a, a.nextSibling, this, e) : d.type === 1 ? p = new d.ctor(a, d.name, d.strings, this, e) : d.type === 6 && (p = new at(a, this, e)), this._$AV.push(p), d = i[++h];
      }
      n !== d?.index && (a = S.nextNode(), n++);
    }
    return S.currentNode = E, s;
  }
  p(e) {
    let t = 0;
    for (const i of this._$AV) i !== void 0 && (i.strings !== void 0 ? (i._$AI(e, i, t), t += i.strings.length - 2) : i._$AI(e[t])), t++;
  }
}
class U {
  get _$AU() {
    return this._$AM?._$AU ?? this._$Cv;
  }
  constructor(e, t, i, s) {
    this.type = 2, this._$AH = c, this._$AN = void 0, this._$AA = e, this._$AB = t, this._$AM = i, this.options = s, this._$Cv = s?.isConnected ?? !0;
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
    e = T(this, e, t), O(e) ? e === c || e == null || e === "" ? (this._$AH !== c && this._$AR(), this._$AH = c) : e !== this._$AH && e !== N && this._(e) : e._$litType$ !== void 0 ? this.$(e) : e.nodeType !== void 0 ? this.T(e) : Qe(e) ? this.k(e) : this._(e);
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
    const { values: t, _$litType$: i } = e, s = typeof i == "number" ? this._$AC(e) : (i.el === void 0 && (i.el = F.createElement(Ce(i.h, i.h[0]), this.options)), i);
    if (this._$AH?._$AD === s) this._$AH.p(t);
    else {
      const a = new tt(s, this), n = a.u(this.options);
      a.p(t), this.T(n), this._$AH = a;
    }
  }
  _$AC(e) {
    let t = $e.get(e.strings);
    return t === void 0 && $e.set(e.strings, t = new F(e)), t;
  }
  k(e) {
    ae(this._$AH) || (this._$AH = [], this._$AR());
    const t = this._$AH;
    let i, s = 0;
    for (const a of e) s === t.length ? t.push(i = new U(this.O(M()), this.O(M()), this, this.options)) : i = t[s], i._$AI(a), s++;
    s < t.length && (this._$AR(i && i._$AB.nextSibling, s), t.length = s);
  }
  _$AR(e = this._$AA.nextSibling, t) {
    for (this._$AP?.(!1, !0, t); e !== this._$AB; ) {
      const i = pe(e).nextSibling;
      pe(e).remove(), e = i;
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
  constructor(e, t, i, s, a) {
    this.type = 1, this._$AH = c, this._$AN = void 0, this.element = e, this.name = t, this._$AM = s, this.options = a, i.length > 2 || i[0] !== "" || i[1] !== "" ? (this._$AH = Array(i.length - 1).fill(new String()), this.strings = i) : this._$AH = c;
  }
  _$AI(e, t = this, i, s) {
    const a = this.strings;
    let n = !1;
    if (a === void 0) e = T(this, e, t, 0), n = !O(e) || e !== this._$AH && e !== N, n && (this._$AH = e);
    else {
      const h = e;
      let d, p;
      for (e = a[0], d = 0; d < a.length - 1; d++) p = T(this, h[i + d], t, d), p === N && (p = this._$AH[d]), n ||= !O(p) || p !== this._$AH[d], p === c ? e = c : e !== c && (e += (p ?? "") + a[d + 1]), this._$AH[d] = p;
    }
    n && !s && this.j(e);
  }
  j(e) {
    e === c ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, e ?? "");
  }
}
class st extends G {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(e) {
    this.element[this.name] = e === c ? void 0 : e;
  }
}
class it extends G {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(e) {
    this.element.toggleAttribute(this.name, !!e && e !== c);
  }
}
class rt extends G {
  constructor(e, t, i, s, a) {
    super(e, t, i, s, a), this.type = 5;
  }
  _$AI(e, t = this) {
    if ((e = T(this, e, t, 0) ?? c) === N) return;
    const i = this._$AH, s = e === c && i !== c || e.capture !== i.capture || e.once !== i.once || e.passive !== i.passive, a = e !== c && (i === c || s);
    s && this.element.removeEventListener(this.name, this, i), a && this.element.addEventListener(this.name, this, e), this._$AH = e;
  }
  handleEvent(e) {
    typeof this._$AH == "function" ? this._$AH.call(this.options?.host ?? this.element, e) : this._$AH.handleEvent(e);
  }
}
class at {
  constructor(e, t, i) {
    this.element = e, this.type = 6, this._$AN = void 0, this._$AM = t, this.options = i;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(e) {
    T(this, e);
  }
}
const nt = re.litHtmlPolyfillSupport;
nt?.(F, U), (re.litHtmlVersions ??= []).push("3.3.3");
const ot = (r, e, t) => {
  const i = t?.renderBefore ?? e;
  let s = i._$litPart$;
  if (s === void 0) {
    const a = t?.renderBefore ?? null;
    i._$litPart$ = s = new U(e.insertBefore(M(), a), a, void 0, t ?? {});
  }
  return s._$AI(r), s;
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
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(e), this._$Do = ot(t, this.renderRoot, this.renderOptions);
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
const lt = ne.litElementPolyfillSupport;
lt?.({ LitElement: $ });
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
class dt extends q {
  constructor() {
    super(...arguments), this.fields = [
      { name: "title", selector: { text: {} } },
      { name: "show_images", selector: { boolean: {} } },
      { name: "show_actions", selector: { boolean: {} } }
    ], this.defaults = { show_images: !0, show_actions: !0 };
  }
}
class ct extends q {
  constructor() {
    super(...arguments), this.fields = [
      { name: "title", selector: { text: {} } },
      { name: "show_image", selector: { boolean: {} } },
      { name: "show_ingredients", selector: { boolean: {} } }
    ], this.defaults = { show_image: !0, show_ingredients: !1 };
  }
}
class ht extends q {
  constructor() {
    super(...arguments), this.fields = [
      { name: "title", selector: { text: {} } },
      { name: "show_added", selector: { boolean: {} } },
      { name: "show_skipped", selector: { boolean: {} } }
    ], this.defaults = { show_added: !0, show_skipped: !1 };
  }
}
class pt extends q {
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
], ut = ["omnivore", "vegetarian", "vegan", "pescatarian"], mt = ["small", "normal", "large"], j = "weeklymenu";
function K(r) {
  const e = /* @__PURE__ */ new Map();
  for (const t of Object.values(r.entities ?? {}))
    t.platform === j && t.translation_key && e.set(t.translation_key, t.entity_id);
  return e;
}
const f = (r) => typeof r == "string" && r !== "" ? r : void 0, _ = (r) => typeof r == "number" && Number.isFinite(r) ? r : void 0, g = (r) => Array.isArray(r) ? r.filter((e) => typeof e == "string") : [], v = (r) => typeof r == "object" && r !== null;
function gt(r) {
  return (v(r) && Array.isArray(r.groups) ? r.groups : []).filter(v).map((t) => {
    const i = Array.isArray(t.substitutions) ? t.substitutions : [], s = _(t.share) ?? 0, a = (n) => {
      if (!v(n)) return "";
      const h = _(n.amount), d = f(n.name);
      return h === void 0 || !d || s <= 0 || s >= 1 ? f(n.raw) ?? d ?? "" : [Math.round(h * s * 10) / 10, f(n.unit), d].filter((u) => u !== void 0).join(" ");
    };
    return {
      members: g(t.members),
      share: s,
      separatePans: t.separate_pans === !0,
      swaps: i.filter(v).map((n) => ({
        original: a(n.original),
        replacement: a(n.replacement)
      }))
    };
  });
}
function ft(r) {
  return Array.isArray(r) ? r.filter(v).filter((e) => typeof e.id == "string" && typeof e.title == "string").map((e) => ({ id: e.id, title: e.title })) : [];
}
function _t(r) {
  const e = {};
  if (v(r))
    for (const [t, i] of Object.entries(r))
      typeof i == "number" && i >= 1 && i <= 5 && (e[t] = i);
  return e;
}
function $t(r) {
  return Array.isArray(r) ? r.filter(v).filter((e) => typeof e.id == "string" && typeof e.title == "string").map((e) => ({
    id: e.id,
    title: e.title,
    image: f(e.image),
    url: f(e.url),
    rating: _(e.rating)
  })) : [];
}
function Te(r, e, t = "") {
  const i = e ? r.states[e] : void 0;
  if (!i || ["unknown", "unavailable", ""].includes(i.state)) return;
  const s = i.attributes, a = f(s.date);
  if (a)
    return {
      entityId: i.entity_id,
      weekday: t,
      date: a,
      title: i.state,
      recipeId: f(s.recipe_id) ?? "",
      url: f(s.url),
      image: f(s.image),
      source: f(s.source),
      totalTime: _(s.total_time),
      servings: _(s.servings),
      tags: g(s.tags),
      ingredients: g(s.ingredients),
      locked: s.locked === !0,
      alternatives: ft(s.alternatives),
      split: gt(s.split),
      ratings: _t(s.ratings),
      favoriteOf: g(s.favorite_of)
    };
}
function ye(r) {
  const e = K(r), t = r.states[e.get("status") ?? ""], i = t?.state, s = t?.attributes ?? {}, a = [];
  for (const n of X) {
    const h = Te(r, e.get(`weekday_${n}`), n);
    h && a.push(h);
  }
  return {
    status: i === "draft" || i === "confirmed" ? i : "none",
    weekStart: f(s.week_start),
    warnings: g(s.warnings),
    days: a
  };
}
function yt(r) {
  return Te(r, K(r).get("today"));
}
function Pe(r) {
  const [e, t, i] = r.split("-").map(Number), s = new Date(Date.UTC(e, t - 1, i)), a = s.getUTCDay() || 7;
  s.setUTCDate(s.getUTCDate() + 4 - a);
  const n = Date.UTC(s.getUTCFullYear(), 0, 1);
  return Math.ceil(((s.getTime() - n) / 864e5 + 1) / 7);
}
function vt(r) {
  return `${Math.round(r * 100)} %`;
}
function bt(r) {
  const e = r.states[K(r).get("shopping") ?? ""], t = e?.attributes ?? {}, i = v(t.counts) ? t.counts : {};
  return {
    hasResult: !!e && !["unknown", "unavailable", ""].includes(e.state),
    weekStart: f(t.week_start),
    counts: {
      added: _(i.added) ?? 0,
      review: _(i.review) ?? 0,
      failed: _(i.failed) ?? 0,
      skipped: _(i.skipped) ?? 0,
      pending: _(i.pending) ?? 0
    },
    added: g(t.added),
    review: g(t.review),
    failed: g(t.failed),
    pending: g(t.pending),
    skipped: g(t.skipped),
    targets: g(t.targets),
    errors: g(t.errors)
  };
}
function B(r) {
  const e = r.states[K(r).get("family") ?? ""];
  return !e || ["unknown", "unavailable", ""].includes(e.state) ? { available: !1, members: [], dinnerDays: [] } : {
    available: !0,
    members: (Array.isArray(e.attributes.members) ? e.attributes.members : []).filter(v).map((s) => ({
      id: f(s.id) ?? "",
      name: f(s.name) ?? "",
      person: f(s.person),
      allergies: g(s.allergies),
      dislikes: g(s.dislikes),
      likes: g(s.likes),
      diet: f(s.diet) ?? "omnivore",
      portion: f(s.portion) ?? "normal",
      attends: g(s.attends),
      cookSeparately: s.cook_separately !== !1,
      child: s.child === !0,
      favorites: $t(s.favorites)
    })).filter((s) => s.id && s.name),
    dinnerDays: g(e.attributes.dinner_days)
  };
}
function De(r) {
  const [e, t, i] = r.split("-").map(Number);
  return new Date(Date.UTC(e, t - 1, i));
}
function ee(r, e) {
  const t = W(r), i = De(e), s = { timeZone: "UTC" };
  return {
    weekday: new Intl.DateTimeFormat(t, { ...s, weekday: "short" }).format(i),
    date: new Intl.DateTimeFormat(t, { ...s, day: "numeric", month: "short" }).format(i)
  };
}
function wt(r, e) {
  return new Intl.DateTimeFormat(W(r), { timeZone: "UTC", weekday: "long" }).format(De(e));
}
function kt(r, e) {
  const t = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"].indexOf(e);
  return t < 0 ? e : wt(r, `2026-11-${String(2 + t).padStart(2, "0")}`);
}
function ve(r, e) {
  const t = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"].indexOf(e);
  return t < 0 ? e : ee(r, `2026-11-${String(2 + t).padStart(2, "0")}`).weekday;
}
function Re(r, e) {
  const t = `source_${e.source}`, i = e.source ? o(r, t) : "";
  return l`<div class="meta">
    ${e.totalTime ? l`<span>${o(r, "minutes", { n: e.totalTime })}</span>` : c}
    ${e.tags.map((s) => l`<span class="tag">${je(r, s)}</span>`)}
    ${i && !i.startsWith("source_") ? l`<span class="badge">${i}</span>` : c}
    ${e.split.length ? l`<span class="badge split" title=${o(r, "split")}>${o(r, "split")}</span>` : c}
    ${e.locked ? l`<span class="badge">${o(r, "locked")}</span>` : c}
  </div>`;
}
function Me(r, e) {
  return e.length ? l`<div class="split-note">
    <strong>${o(r, "split")}</strong>
    ${e.map(
    (t) => l`<div>
        ${t.swaps.map(
      (i) => l`<div>
              ${o(r, "splitNote", {
        members: t.members.join(", ") + ` (${vt(t.share)})`,
        from: i.original,
        to: i.replacement
      })}
            </div>`
    )}
        ${t.separatePans ? l`<em>${o(r, "cleanPans")}</em>` : c}
      </div>`
  )}
  </div>` : c;
}
function Oe(r, e) {
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
const I = He`
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
    return e.find((i) => i.person && r.states[i.person]?.attributes?.user_id === t);
}
class xt extends $ {
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
      await this.hass.callService(j, e, t);
    } catch (i) {
      this._error = Z(i);
    }
  }
  render() {
    const e = this.dinner;
    if (!this.hass || !e?.recipeId) return c;
    const t = this.hass, i = B(t).members;
    if (!i.length) return c;
    const s = i.find((p) => p.id === this._member) ?? oe(t, i) ?? i[0], a = e.ratings[s.id] ?? 0, n = e.favoriteOf.includes(s.id), h = e.favoriteOf.map((p) => i.find((u) => u.id === p)?.name).filter(Boolean), d = (p) => p === 1 ? o(t, "starOne") : o(t, "starsN", { n: p });
    return l`<div class="taste">
      ${i.length > 1 ? l`<select
            aria-label=${o(t, "rateAs")}
            .value=${s.id}
            @change=${(p) => this._member = p.target.value}
          >
            ${i.map((p) => l`<option value=${p.id} ?selected=${p.id === s.id}>${p.name}</option>`)}
          </select>` : c}
      <span class="stars" role="group" aria-label=${o(t, "ratingGroup")}>
        ${[1, 2, 3, 4, 5].map(
      (p) => l`<button
            class="icon ${p <= a ? "on" : ""}"
            title=${d(p)}
            aria-label=${d(p)}
            aria-pressed=${p === a ? "true" : "false"}
            @click=${() => void this._call("rate_recipe", { member: s.id, recipe_id: e.recipeId, rating: p === a ? 0 : p })}
          >
            <ha-icon icon=${p <= a ? "mdi:star" : "mdi:star-outline"}></ha-icon>
          </button>`
    )}
      </span>
      <button
        class="icon heart ${n ? "on" : ""}"
        title=${n ? o(t, "favoriteRemove") : o(t, "favoriteAdd")}
        aria-label=${n ? o(t, "favoriteRemove") : o(t, "favoriteAdd")}
        aria-pressed=${n ? "true" : "false"}
        @click=${() => void this._call("favorite_recipe", { member: s.id, recipe_id: e.recipeId, favorite: !n })}
      >
        <ha-icon icon=${n ? "mdi:heart" : "mdi:heart-outline"}></ha-icon>
      </button>
      ${h.length ? l`<span class="liked">${o(t, "favoriteOf", { names: h.join(", ") })}</span>` : c}
      ${this._error ? l`<span class="banner error">${o(t, "error", { error: this._error })}</span>` : c}
    </div>`;
  }
}
const te = new Set(Ne);
function At(r) {
  return Object.values(r.states).filter((e) => e.entity_id.startsWith("person.")).map((e) => ({ id: e.entity_id, name: Fe(r, e.entity_id) })).sort((e, t) => e.name.localeCompare(t.name));
}
function Fe(r, e) {
  const t = r.states[e]?.attributes?.friendly_name;
  return typeof t == "string" && t ? t : e.replace(/^person\./, "").replace(/_/g, " ");
}
function St(r, e, t) {
  const i = t ? r.states[t]?.attributes?.entity_picture : void 0;
  return typeof i == "string" && i ? l`<img class="avatar" src=${i} alt="" />` : l`<span class="avatar" aria-hidden="true">${[...e.trim()][0]?.toUpperCase() ?? "?"}</span>`;
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
    child: r.child
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
    child: !1
  };
}
class Et extends $ {
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
    return this.hass ? 2 + B(this.hass).members.length : 3;
  }
  // --- actions ----------------------------------------------------------------------
  _set(e) {
    this._draft && (this._draft = { ...this._draft, ...e });
  }
  /** Pick a Home Assistant person. The name follows the person unless it was typed by hand. */
  _pickPerson(e) {
    const t = this._draft;
    if (!t) return;
    const i = e ? Fe(this.hass, e) : "", s = t.name.trim() === "" || t.name === t.filledName;
    this._draft = {
      ...t,
      person: e,
      name: s && i ? i : t.name,
      filledName: s && i ? i : t.filledName
    };
  }
  _toggle(e, t) {
    if (!this._draft) return;
    const i = this._draft[e];
    this._set({ [e]: i.includes(t) ? i.filter((s) => s !== t) : [...i, t] });
  }
  async _run(e, t) {
    this._busy = !0, this._error = "";
    try {
      return await this.hass.callService(j, e, t), !0;
    } catch (i) {
      return this._error = Z(i), !1;
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
      attends: X.filter((i) => e.attends.includes(i)),
      cook_separately: e.cookSeparately,
      child: e.child
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
    const e = this.hass, t = B(e), i = this._config.title ?? o(e, "familyTitle");
    if (!t.available)
      return l`<ha-card .header=${i}><div class="empty">${o(e, "famNoFamily")}</div></ha-card>`;
    const s = oe(e, t.members), a = this._config.editable !== !1 && !s?.child, n = t.dinnerDays.length ? t.dinnerDays : [...X];
    return l`<ha-card .header=${i}>
      ${this._error ? l`<div class="banner error">${o(e, "error", { error: this._error })}</div>` : c}
      ${t.members.length ? t.members.map((h) => this._renderMember(h, t.dinnerDays, a, n, s)) : l`<div class="empty">${o(e, "famNone")}</div>`}
      ${this._draft && !this._draft.id ? this._renderForm(this._draft, n) : c}
      ${a && !this._draft ? l`<div class="foot">
            <button class="primary" ?disabled=${this._busy} @click=${() => this._draft = be(void 0, n)}>
              ${o(e, "famAdd")}
            </button>
          </div>` : c}
    </ha-card>`;
  }
  _renderMember(e, t, i, s, a) {
    const n = this.hass, h = this._draft?.id === e.id, d = s.filter((u) => e.attends.includes(u)), p = d.length === s.length;
    return l`<div class="member">
      <div class="main">
        ${St(n, e.name, e.person)}
        <div style="flex:1;min-width:0">
          <div class="title">${e.name}</div>
          <div class="meta">
            ${e.child ? l`<span class="badge">${o(n, "famChildBadge")}</span>` : c}
            ${e.diet !== "omnivore" ? l`<span class="badge">${o(n, `diet_${e.diet}`)}</span>` : c}
            ${e.portion !== "normal" ? l`<span class="badge">${o(n, `portion_${e.portion}`)}</span>` : c}
            ${e.allergies.map((u) => l`<span class="tag allergy">${te.has(u) ? o(n, `allergen_${u}`) : u}</span>`)}
            ${e.dislikes.length ? l`<span>${e.dislikes.join(", ")}</span>` : c}
            <span>${p ? o(n, "famEveryDay") : d.map((u) => ve(n, u)).join(", ")}</span>
          </div>
          ${e.favorites.length ? this._renderFavorites(e, i || this._config.editable !== !1 && a?.id === e.id, !1) : c}
        </div>
        ${i && !h ? l`<button ?disabled=${this._busy} @click=${() => this._draft = be(e, t)}>
              ${o(n, "famEdit")}
            </button>` : c}
      </div>
      ${h && this._draft ? this._renderForm(this._draft, s, e) : c}
    </div>`;
  }
  /** A member's favorite recipes, folded out from a summary line, each with a button to remove it. */
  _renderFavorites(e, t, i) {
    const s = this.hass;
    return l`<details class="favorites" ?open=${i}>
      <summary>${o(s, "famFavorites", { n: e.favorites.length })}</summary>
      ${e.favorites.length ? e.favorites.map(
      (a) => l`<div class="fav">
              ${a.image ? l`<img src=${a.image} alt="" loading="lazy" />` : c}
              <span class="name">
                ${a.url ? l`<a href=${a.url} target="_blank" rel="noopener noreferrer" title=${o(s, "openRecipe")}>${a.title}</a>` : a.title}
              </span>
              ${a.rating ? l`<span class="stars-text">★ ${a.rating}</span>` : c}
              ${t ? l`<button
                    class="icon"
                    ?disabled=${this._busy}
                    title=${o(s, "famRemoveFavorite", { title: a.title })}
                    aria-label=${o(s, "famRemoveFavorite", { title: a.title })}
                    @click=${() => this._removeFavorite(e, a.id)}
                  >
                    <ha-icon icon="mdi:close"></ha-icon>
                  </button>` : c}
            </div>`
    ) : l`<div class="empty">${o(s, "famNoFavorites")}</div>`}
    </details>`;
  }
  _renderForm(e, t, i) {
    const s = this.hass, a = e.name.trim() !== "" && e.attends.length > 0, n = (d, p, u) => l`<label class="field">
      <span>${o(s, d)}</span>
      <input
        type="text"
        .value=${p}
        @input=${(m) => this._set({ [u]: m.target.value })}
      />
    </label>`, h = At(s);
    return l`<form class="form" @submit=${(d) => d.preventDefault()}>
      ${h.length || e.person ? l`<label class="field">
            <span>${o(s, "famPerson")}</span>
            <select .value=${e.person} @change=${(d) => this._pickPerson(d.target.value)}>
              <option value="" ?selected=${!e.person}>${o(s, "famNoPerson")}</option>
              ${h.map((d) => l`<option value=${d.id} ?selected=${e.person === d.id}>${d.name}</option>`)}
              ${e.person && !h.some((d) => d.id === e.person) ? l`<option value=${e.person} selected>${e.person}</option>` : c}
            </select>
          </label>` : c}
      ${n("famName", e.name, "name")}
      <fieldset>
        <legend>${o(s, "famAllergies")}</legend>
        <div class="checks">
          ${Ne.map(
      (d) => l`<label class="check">
              <input type="checkbox" .checked=${e.allergies.includes(d)} @change=${() => this._toggle("allergies", d)} />
              ${o(s, `allergen_${d}`)}
            </label>`
    )}
        </div>
      </fieldset>
      ${n("famOtherAllergies", e.otherAllergies, "otherAllergies")} ${n("famDislikes", e.dislikes, "dislikes")}
      ${n("famLikes", e.likes, "likes")}
      <div class="row">
        <label class="field">
          <span>${o(s, "famDiet")}</span>
          <select .value=${e.diet} @change=${(d) => this._set({ diet: d.target.value })}>
            ${ut.map((d) => l`<option value=${d} ?selected=${e.diet === d}>${o(s, `diet_${d}`)}</option>`)}
          </select>
        </label>
        <label class="field">
          <span>${o(s, "famPortion")}</span>
          <select .value=${e.portion} @change=${(d) => this._set({ portion: d.target.value })}>
            ${mt.map((d) => l`<option value=${d} ?selected=${e.portion === d}>${o(s, `portion_${d}`)}</option>`)}
          </select>
        </label>
      </div>
      <fieldset>
        <legend>${o(s, "famDays")}</legend>
        <div class="checks">
          ${t.map(
      (d) => l`<label class="check">
              <input type="checkbox" .checked=${e.attends.includes(d)} @change=${() => this._toggle("attends", d)} />
              ${ve(s, d)}
            </label>`
    )}
        </div>
        ${e.attends.length ? c : l`<small class="hint-error">${o(s, "famNoDays")}</small>`}
      </fieldset>
      <label class="check">
        <input
          type="checkbox"
          .checked=${e.child}
          @change=${(d) => this._set({ child: d.target.checked })}
        />
        ${o(s, "famChild")}
      </label>
      <label class="check">
        <input
          type="checkbox"
          .checked=${e.cookSeparately}
          @change=${(d) => this._set({ cookSeparately: d.target.checked })}
        />
        ${o(s, "famCookSeparately")}
      </label>
      ${i ? this._renderFavorites(i, !0, !0) : c}
      <small>${o(s, "famAppliesLater")}</small>
      <div class="row">
        <button class="primary" type="button" ?disabled=${this._busy || !a} @click=${() => this._save()}>${o(s, "famSave")}</button>
        <button type="button" ?disabled=${this._busy} @click=${() => this._draft = null}>${o(s, "famCancel")}</button>
        ${e.id ? l`<button type="button" ?disabled=${this._busy} @click=${() => this._remove()}>${o(s, "famRemove")}</button>` : c}
      </div>
    </form>`;
  }
}
class Ct extends $ {
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
      await this.hass.callService(j, e, t);
    } catch (i) {
      this._error = Z(i);
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
    const i = t.target, s = i.value;
    i.value = "", s && this._call("set_recipe", { date: e.date, recipe_id: s });
  }
  _swap(e, t) {
    const i = t.target, s = i.value;
    i.value = "", s && this._call("swap_days", { date: e.date, other_date: s });
  }
  // --- rendering -------------------------------------------------------------------
  render() {
    if (!this.hass) return l``;
    const e = this.hass, t = ye(e), i = t.status === "confirmed", s = oe(e, B(e).members)?.child === !0, a = this._config.show_actions !== !1 && !i && !s, n = [...new Set(t.warnings.map((h) => Ue(e, h, (d) => kt(e, d))))];
    return l`<ha-card .header=${this._config.title ?? o(e, "menuTitle")}>
      <div class="head">
        <span>${t.weekStart ? o(e, "week", { n: Pe(t.weekStart) }) : ""}</span>
        <span class="chip ${t.status}">${o(e, `status_${t.status}`)}</span>
      </div>
      ${n.map((h) => l`<div class="banner warning">${h}</div>`)}
      ${this._error ? l`<div class="banner error">${o(e, "error", { error: this._error })}</div>` : c}
      ${this._busy ? l`<div class="banner">${o(e, "working")}</div>` : c}
      ${t.days.length ? t.days.map((h) => this._renderDay(h, t, a)) : l`<div class="empty">${o(e, "noMenu")}</div>`}
      ${i && this._config.show_actions !== !1 && !s ? l`<div class="banner">${o(e, "confirmedNote")}</div>` : c}
      ${this._renderFooter(t, a)}
    </ha-card>`;
  }
  _renderFooter(e, t) {
    if (!t) return c;
    const i = e.days.length === 0;
    return l`<div class="foot">
      <button
        class=${i ? "primary" : ""}
        ?disabled=${this._busy}
        @click=${() => this._call("generate_menu", e.weekStart && !i ? { week_start: e.weekStart } : {})}
      >
        ${i ? o(this.hass, "generate") : o(this.hass, "regenerateAll")}
      </button>
      ${e.status === "draft" && !i ? l`<button class="primary" ?disabled=${this._busy} @click=${() => this._confirm(e)}>
            ${o(this.hass, "confirm")}
          </button>` : c}
    </div>`;
  }
  _renderDay(e, t, i) {
    const s = this.hass, a = ee(s, e.date), n = this._open.has(e.date), h = e.url ? l`<a href=${e.url} target="_blank" rel="noopener noreferrer" title=${o(s, "openRecipe")}>${e.title}</a>` : e.title, d = t.days.filter((p) => p.date !== e.date && !p.locked);
    return l`<div class="day">
      <div class="when">
        <div class="wd">${a.weekday}</div>
        <div class="dt">${a.date}</div>
      </div>
      <div class="main">
        ${this._config.show_images !== !1 && e.image ? l`<img src=${e.image} alt="" loading="lazy" />` : c}
        <div>
          <div class="title">${h}</div>
          ${Re(s, e)}
        </div>
      </div>
      <div class="actions">
        ${i ? l`<button
              class="icon ${e.locked ? "on" : ""}"
              ?disabled=${this._busy}
              title=${e.locked ? o(s, "unlock") : o(s, "lock")}
              aria-label=${e.locked ? o(s, "unlock") : o(s, "lock")}
              aria-pressed=${e.locked ? "true" : "false"}
              @click=${() => this._call("lock_day", { date: e.date, locked: !e.locked })}
            >
              <ha-icon icon=${e.locked ? "mdi:lock" : "mdi:lock-open-variant-outline"}></ha-icon>
            </button>` : c}
        <button
          class="icon"
          title=${n ? o(s, "hide") : o(s, "show")}
          aria-label=${n ? o(s, "hide") : o(s, "show")}
          aria-expanded=${n ? "true" : "false"}
          @click=${() => this._toggle(e.date)}
        >
          <ha-icon icon=${n ? "mdi:chevron-up" : "mdi:chevron-down"}></ha-icon>
        </button>
      </div>
      ${n ? this._renderMore(e, d, i) : c}
    </div>`;
  }
  _renderMore(e, t, i) {
    const s = this.hass;
    return l`<div class="more">
      ${this._config.show_actions !== !1 ? l`<weeklymenu-taste .hass=${s} .dinner=${e}></weeklymenu-taste>` : c}
      ${Me(s, e.split)} ${Oe(s, e.ingredients)}
      ${i ? l`<div class="row">
              <input
                type="text"
                .value=${this._hints[e.date] ?? ""}
                placeholder=${o(s, "hint")}
                aria-label=${o(s, "hint")}
                @input=${(a) => {
      this._hints = { ...this._hints, [e.date]: a.target.value };
    }}
              />
              <button ?disabled=${this._busy || e.locked} @click=${() => this._regenerateDay(e)}>
                ${o(s, "newDinner")}
              </button>
            </div>
            <div class="row">
              ${e.alternatives.length ? l`<select
                    ?disabled=${this._busy}
                    aria-label=${o(s, "alternatives")}
                    @change=${(a) => this._pick(e, a)}
                  >
                    <option value="">${o(s, "alternatives")}: ${o(s, "choose")}</option>
                    ${e.alternatives.map((a) => l`<option value=${a.id}>${a.title}</option>`)}
                  </select>` : c}
              ${t.length && !e.locked ? l`<select
                    ?disabled=${this._busy}
                    aria-label=${o(s, "swapWith")}
                    @change=${(a) => this._swap(e, a)}
                  >
                    <option value="">${o(s, "swapWith")}</option>
                    ${t.map((a) => {
      const n = ee(s, a.date);
      return l`<option value=${a.date}>${n.weekday} ${n.date}: ${a.title}</option>`;
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
class Nt extends $ {
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
      await this.hass.callService(j, "add_to_shopping", {});
    } catch (e) {
      this._error = Z(e);
    } finally {
      this._busy = !1;
    }
  }
  render() {
    if (!this.hass) return l``;
    const e = this.hass, t = bt(e), i = this._config.title ?? o(e, "shoppingTitle");
    if (!t.hasResult)
      return l`<ha-card .header=${i}><div class="empty">${o(e, "shopNothing")}</div></ha-card>`;
    const s = t.counts.failed + t.counts.pending, a = t.errors.some((h) => h.endsWith(": auth_failed")), n = [
      ...new Set(t.errors.filter((h) => !(a && h === "reauth_required")).map((h) => Ie(e, h)))
    ];
    return l`<ha-card .header=${i}>
      <div class="head">
        <span>
          ${t.weekStart ? o(e, "week", { n: Pe(t.weekStart) }) : ""}
          ${t.targets.length ? ` · ${o(e, "shopTargets", { targets: t.targets.join(", ") })}` : ""}
        </span>
      </div>
      <div class="head chips">
        ${we.filter((h) => t.counts[h.key] > 0).map(
      (h) => l`<span class="chip ${h.css === "warning" ? "draft" : ""}">${o(e, h.label)}: ${t.counts[h.key]}</span>`
    )}
      </div>
      ${n.map((h) => l`<div class="banner warning">${h}</div>`)}
      ${this._error ? l`<div class="banner error">${o(e, "error", { error: this._error })}</div>` : c}
      ${we.map((h) => this._renderGroup(h, t[h.key]))}
      ${s ? l`<div class="foot">
            <button class="primary" ?disabled=${this._busy} @click=${() => this._retry()}>${o(e, "shopRetry")}</button>
          </div>` : c}
    </ha-card>`;
  }
  _renderGroup(e, t) {
    if (!t.length || e.key === "added" && this._config.show_added === !1 || e.key === "skipped" && !this._config.show_skipped) return c;
    const i = e.key === "review" || e.key === "failed" || e.key === "pending";
    return l`<details class="group ${e.css}" ?open=${i}>
      <summary>${o(this.hass, e.label)} (${t.length})</summary>
      <ul>
        ${t.map((s) => l`<li>${s}</li>`)}
      </ul>
    </details>`;
  }
}
class Tt extends $ {
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
    const e = this.hass, t = yt(e), i = this._config.title ?? o(e, "todayTitle");
    if (!t)
      return l`<ha-card .header=${i}><div class="empty">${o(e, "noDinner")}</div></ha-card>`;
    const s = t.url ? l`<a href=${t.url} target="_blank" rel="noopener noreferrer" title=${o(e, "openRecipe")}>${t.title}</a>` : t.title;
    return l`<ha-card .header=${i}>
      <div class="day" style="grid-template-columns: 1fr">
        <div class="main">
          ${this._config.show_image !== !1 && t.image ? l`<img src=${t.image} alt="" loading="lazy" style="width:72px;height:72px" />` : c}
          <div>
            <div class="title">${s}</div>
            ${Re(e, t)}
          </div>
        </div>
        <div class="more" style="padding-left:0">
          <weeklymenu-taste .hass=${e} .dinner=${t}></weeklymenu-taste>
          ${Me(e, t.split)}
          ${this._config.show_ingredients ? Oe(e, t.ingredients) : c}
        </div>
      </div>
    </ha-card>`;
  }
}
function b(r, e) {
  customElements.get(r) || customElements.define(r, e);
}
b("weeklymenu-taste", xt);
b("weeklymenu-menu-card", Ct);
b("weeklymenu-menu-card-editor", dt);
b("weeklymenu-today-card", Tt);
b("weeklymenu-today-card-editor", ct);
b("weeklymenu-shopping-card", Nt);
b("weeklymenu-shopping-card-editor", ht);
b("weeklymenu-family-card", Et);
b("weeklymenu-family-card-editor", pt);
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
