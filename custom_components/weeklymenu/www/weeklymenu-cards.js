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
    cardTodayDescription: "Today's dinner, compact."
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
    cardTodayDescription: "Dagens middag, kompakt."
  }
};
function z(r) {
  return (r?.locale?.language ?? r?.language ?? "en").slice(0, 2) === "sv" ? "sv" : "en";
}
function a(r, e, t = {}) {
  return (R[z(r)][e] ?? R.en[e]).replace(/\{(\w+)\}/g, (i, n) => String(t[n] ?? `{${n}}`));
}
function Ae(r, e, t) {
  const [s, i = ""] = e.split(":"), n = `warn_${s}`;
  if (!(n in R.en)) return e;
  const o = s === "no_recipe" || s === "split_limit_exceeded" ? t(i) : i;
  return a(r, n, { detail: o });
}
function Se(r, e) {
  const t = `tag_${e}`;
  return t in R.en ? a(r, t) : e.replace(/_/g, " ");
}
/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const O = globalThis, q = O.ShadowRoot && (O.ShadyCSS === void 0 || O.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, K = Symbol(), Y = /* @__PURE__ */ new WeakMap();
let de = class {
  constructor(e, t, s) {
    if (this._$cssResult$ = !0, s !== K) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = e, this.t = t;
  }
  get styleSheet() {
    let e = this.o;
    const t = this.t;
    if (q && e === void 0) {
      const s = t !== void 0 && t.length === 1;
      s && (e = Y.get(t)), e === void 0 && ((this.o = e = new CSSStyleSheet()).replaceSync(this.cssText), s && Y.set(t, e));
    }
    return e;
  }
  toString() {
    return this.cssText;
  }
};
const Ee = (r) => new de(typeof r == "string" ? r : r + "", void 0, K), Ce = (r, ...e) => {
  const t = r.length === 1 ? r[0] : e.reduce((s, i, n) => s + ((o) => {
    if (o._$cssResult$ === !0) return o.cssText;
    if (typeof o == "number") return o;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + o + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(i) + r[n + 1], r[0]);
  return new de(t, r, K);
}, Te = (r, e) => {
  if (q) r.adoptedStyleSheets = e.map((t) => t instanceof CSSStyleSheet ? t : t.styleSheet);
  else for (const t of e) {
    const s = document.createElement("style"), i = O.litNonce;
    i !== void 0 && s.setAttribute("nonce", i), s.textContent = t.cssText, r.appendChild(s);
  }
}, Q = q ? (r) => r : (r) => r instanceof CSSStyleSheet ? ((e) => {
  let t = "";
  for (const s of e.cssRules) t += s.cssText;
  return Ee(t);
})(r) : r;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: Ne, defineProperty: Me, getOwnPropertyDescriptor: Pe, getOwnPropertyNames: Ue, getOwnPropertySymbols: De, getPrototypeOf: Oe } = Object, j = globalThis, X = j.trustedTypes, Re = X ? X.emptyScript : "", He = j.reactiveElementPolyfillSupport, C = (r, e) => r, V = { toAttribute(r, e) {
  switch (e) {
    case Boolean:
      r = r ? Re : null;
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
} }, he = (r, e) => !Ne(r, e), ee = { attribute: !0, type: String, converter: V, reflect: !1, useDefault: !1, hasChanged: he };
Symbol.metadata ??= Symbol("metadata"), j.litPropertyMetadata ??= /* @__PURE__ */ new WeakMap();
let x = class extends HTMLElement {
  static addInitializer(e) {
    this._$Ei(), (this.l ??= []).push(e);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(e, t = ee) {
    if (t.state && (t.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(e) && ((t = Object.create(t)).wrapped = !0), this.elementProperties.set(e, t), !t.noAccessor) {
      const s = Symbol(), i = this.getPropertyDescriptor(e, s, t);
      i !== void 0 && Me(this.prototype, e, i);
    }
  }
  static getPropertyDescriptor(e, t, s) {
    const { get: i, set: n } = Pe(this.prototype, e) ?? { get() {
      return this[t];
    }, set(o) {
      this[t] = o;
    } };
    return { get: i, set(o) {
      const h = i?.call(this);
      n?.call(this, o), this.requestUpdate(e, h, s);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(e) {
    return this.elementProperties.get(e) ?? ee;
  }
  static _$Ei() {
    if (this.hasOwnProperty(C("elementProperties"))) return;
    const e = Oe(this);
    e.finalize(), e.l !== void 0 && (this.l = [...e.l]), this.elementProperties = new Map(e.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(C("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(C("properties"))) {
      const t = this.properties, s = [...Ue(t), ...De(t)];
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
      for (const i of s) t.unshift(Q(i));
    } else e !== void 0 && t.push(Q(e));
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
    return Te(e, this.constructor.elementStyles), e;
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
      const n = (s.converter?.toAttribute !== void 0 ? s.converter : V).toAttribute(t, s.type);
      this._$Em = e, n == null ? this.removeAttribute(i) : this.setAttribute(i, n), this._$Em = null;
    }
  }
  _$AK(e, t) {
    const s = this.constructor, i = s._$Eh.get(e);
    if (i !== void 0 && this._$Em !== i) {
      const n = s.getPropertyOptions(i), o = typeof n.converter == "function" ? { fromAttribute: n.converter } : n.converter?.fromAttribute !== void 0 ? n.converter : V;
      this._$Em = i;
      const h = o.fromAttribute(t, n.type);
      this[i] = h ?? this._$Ej?.get(i) ?? h, this._$Em = null;
    }
  }
  requestUpdate(e, t, s, i = !1, n) {
    if (e !== void 0) {
      const o = this.constructor;
      if (i === !1 && (n = this[e]), s ??= o.getPropertyOptions(e), !((s.hasChanged ?? he)(n, t) || s.useDefault && s.reflect && n === this._$Ej?.get(e) && !this.hasAttribute(o._$Eu(e, s)))) return;
      this.C(e, t, s);
    }
    this.isUpdatePending === !1 && (this._$ES = this._$EP());
  }
  C(e, t, { useDefault: s, reflect: i, wrapped: n }, o) {
    s && !(this._$Ej ??= /* @__PURE__ */ new Map()).has(e) && (this._$Ej.set(e, o ?? t ?? this[e]), n !== !0 || o !== void 0) || (this._$AL.has(e) || (this.hasUpdated || s || (t = void 0), this._$AL.set(e, t)), i === !0 && this._$Em !== e && (this._$Eq ??= /* @__PURE__ */ new Set()).add(e));
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
        const { wrapped: o } = n, h = this[i];
        o !== !0 || this._$AL.has(i) || h === void 0 || this.C(i, void 0, n, h);
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
x.elementStyles = [], x.shadowRootOptions = { mode: "open" }, x[C("elementProperties")] = /* @__PURE__ */ new Map(), x[C("finalized")] = /* @__PURE__ */ new Map(), He?.({ ReactiveElement: x }), (j.reactiveElementVersions ??= []).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Z = globalThis, te = (r) => r, H = Z.trustedTypes, se = H ? H.createPolicy("lit-html", { createHTML: (r) => r }) : void 0, pe = "$lit$", _ = `lit$${Math.random().toFixed(9).slice(2)}$`, ue = "?" + _, Ie = `<${ue}>`, b = document, T = () => b.createComment(""), N = (r) => r === null || typeof r != "object" && typeof r != "function", G = Array.isArray, ze = (r) => G(r) || typeof r?.[Symbol.iterator] == "function", B = `[ 	
\f\r]`, S = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, ie = /-->/g, re = />/g, y = RegExp(`>|${B}(?:([^\\s"'>=/]+)(${B}*=${B}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`, "g"), ne = /'/g, oe = /"/g, ge = /^(?:script|style|textarea|title)$/i, je = (r) => (e, ...t) => ({ _$litType$: r, strings: e, values: t }), l = je(1), k = Symbol.for("lit-noChange"), c = Symbol.for("lit-nothing"), ae = /* @__PURE__ */ new WeakMap(), v = b.createTreeWalker(b, 129);
function fe(r, e) {
  if (!G(r) || !r.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return se !== void 0 ? se.createHTML(e) : e;
}
const Le = (r, e) => {
  const t = r.length - 1, s = [];
  let i, n = e === 2 ? "<svg>" : e === 3 ? "<math>" : "", o = S;
  for (let h = 0; h < t; h++) {
    const d = r[h];
    let u, g, p = -1, f = 0;
    for (; f < d.length && (o.lastIndex = f, g = o.exec(d), g !== null); ) f = o.lastIndex, o === S ? g[1] === "!--" ? o = ie : g[1] !== void 0 ? o = re : g[2] !== void 0 ? (ge.test(g[2]) && (i = RegExp("</" + g[2], "g")), o = y) : g[3] !== void 0 && (o = y) : o === y ? g[0] === ">" ? (o = i ?? S, p = -1) : g[1] === void 0 ? p = -2 : (p = o.lastIndex - g[2].length, u = g[1], o = g[3] === void 0 ? y : g[3] === '"' ? oe : ne) : o === oe || o === ne ? o = y : o === ie || o === re ? o = S : (o = y, i = void 0);
    const m = o === y && r[h + 1].startsWith("/>") ? " " : "";
    n += o === S ? d + Ie : p >= 0 ? (s.push(u), d.slice(0, p) + pe + d.slice(p) + _ + m) : d + _ + (p === -2 ? h : m);
  }
  return [fe(r, n + (r[t] || "<?>") + (e === 2 ? "</svg>" : e === 3 ? "</math>" : "")), s];
};
class M {
  constructor({ strings: e, _$litType$: t }, s) {
    let i;
    this.parts = [];
    let n = 0, o = 0;
    const h = e.length - 1, d = this.parts, [u, g] = Le(e, t);
    if (this.el = M.createElement(u, s), v.currentNode = this.el.content, t === 2 || t === 3) {
      const p = this.el.content.firstChild;
      p.replaceWith(...p.childNodes);
    }
    for (; (i = v.nextNode()) !== null && d.length < h; ) {
      if (i.nodeType === 1) {
        if (i.hasAttributes()) for (const p of i.getAttributeNames()) if (p.endsWith(pe)) {
          const f = g[o++], m = i.getAttribute(p).split(_), U = /([.?@])?(.*)/.exec(f);
          d.push({ type: 1, index: n, name: U[2], strings: m, ctor: U[1] === "." ? Be : U[1] === "?" ? Ve : U[1] === "@" ? Fe : L }), i.removeAttribute(p);
        } else p.startsWith(_) && (d.push({ type: 6, index: n }), i.removeAttribute(p));
        if (ge.test(i.tagName)) {
          const p = i.textContent.split(_), f = p.length - 1;
          if (f > 0) {
            i.textContent = H ? H.emptyScript : "";
            for (let m = 0; m < f; m++) i.append(p[m], T()), v.nextNode(), d.push({ type: 2, index: ++n });
            i.append(p[f], T());
          }
        }
      } else if (i.nodeType === 8) if (i.data === ue) d.push({ type: 2, index: n });
      else {
        let p = -1;
        for (; (p = i.data.indexOf(_, p + 1)) !== -1; ) d.push({ type: 7, index: n }), p += _.length - 1;
      }
      n++;
    }
  }
  static createElement(e, t) {
    const s = b.createElement("template");
    return s.innerHTML = e, s;
  }
}
function A(r, e, t = r, s) {
  if (e === k) return e;
  let i = s !== void 0 ? t._$Co?.[s] : t._$Cl;
  const n = N(e) ? void 0 : e._$litDirective$;
  return i?.constructor !== n && (i?._$AO?.(!1), n === void 0 ? i = void 0 : (i = new n(r), i._$AT(r, t, s)), s !== void 0 ? (t._$Co ??= [])[s] = i : t._$Cl = i), i !== void 0 && (e = A(r, i._$AS(r, e.values), i, s)), e;
}
class We {
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
    const { el: { content: t }, parts: s } = this._$AD, i = (e?.creationScope ?? b).importNode(t, !0);
    v.currentNode = i;
    let n = v.nextNode(), o = 0, h = 0, d = s[0];
    for (; d !== void 0; ) {
      if (o === d.index) {
        let u;
        d.type === 2 ? u = new P(n, n.nextSibling, this, e) : d.type === 1 ? u = new d.ctor(n, d.name, d.strings, this, e) : d.type === 6 && (u = new qe(n, this, e)), this._$AV.push(u), d = s[++h];
      }
      o !== d?.index && (n = v.nextNode(), o++);
    }
    return v.currentNode = b, i;
  }
  p(e) {
    let t = 0;
    for (const s of this._$AV) s !== void 0 && (s.strings !== void 0 ? (s._$AI(e, s, t), t += s.strings.length - 2) : s._$AI(e[t])), t++;
  }
}
class P {
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
    e = A(this, e, t), N(e) ? e === c || e == null || e === "" ? (this._$AH !== c && this._$AR(), this._$AH = c) : e !== this._$AH && e !== k && this._(e) : e._$litType$ !== void 0 ? this.$(e) : e.nodeType !== void 0 ? this.T(e) : ze(e) ? this.k(e) : this._(e);
  }
  O(e) {
    return this._$AA.parentNode.insertBefore(e, this._$AB);
  }
  T(e) {
    this._$AH !== e && (this._$AR(), this._$AH = this.O(e));
  }
  _(e) {
    this._$AH !== c && N(this._$AH) ? this._$AA.nextSibling.data = e : this.T(b.createTextNode(e)), this._$AH = e;
  }
  $(e) {
    const { values: t, _$litType$: s } = e, i = typeof s == "number" ? this._$AC(e) : (s.el === void 0 && (s.el = M.createElement(fe(s.h, s.h[0]), this.options)), s);
    if (this._$AH?._$AD === i) this._$AH.p(t);
    else {
      const n = new We(i, this), o = n.u(this.options);
      n.p(t), this.T(o), this._$AH = n;
    }
  }
  _$AC(e) {
    let t = ae.get(e.strings);
    return t === void 0 && ae.set(e.strings, t = new M(e)), t;
  }
  k(e) {
    G(this._$AH) || (this._$AH = [], this._$AR());
    const t = this._$AH;
    let s, i = 0;
    for (const n of e) i === t.length ? t.push(s = new P(this.O(T()), this.O(T()), this, this.options)) : s = t[i], s._$AI(n), i++;
    i < t.length && (this._$AR(s && s._$AB.nextSibling, i), t.length = i);
  }
  _$AR(e = this._$AA.nextSibling, t) {
    for (this._$AP?.(!1, !0, t); e !== this._$AB; ) {
      const s = te(e).nextSibling;
      te(e).remove(), e = s;
    }
  }
  setConnected(e) {
    this._$AM === void 0 && (this._$Cv = e, this._$AP?.(e));
  }
}
class L {
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
    let o = !1;
    if (n === void 0) e = A(this, e, t, 0), o = !N(e) || e !== this._$AH && e !== k, o && (this._$AH = e);
    else {
      const h = e;
      let d, u;
      for (e = n[0], d = 0; d < n.length - 1; d++) u = A(this, h[s + d], t, d), u === k && (u = this._$AH[d]), o ||= !N(u) || u !== this._$AH[d], u === c ? e = c : e !== c && (e += (u ?? "") + n[d + 1]), this._$AH[d] = u;
    }
    o && !i && this.j(e);
  }
  j(e) {
    e === c ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, e ?? "");
  }
}
class Be extends L {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(e) {
    this.element[this.name] = e === c ? void 0 : e;
  }
}
class Ve extends L {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(e) {
    this.element.toggleAttribute(this.name, !!e && e !== c);
  }
}
class Fe extends L {
  constructor(e, t, s, i, n) {
    super(e, t, s, i, n), this.type = 5;
  }
  _$AI(e, t = this) {
    if ((e = A(this, e, t, 0) ?? c) === k) return;
    const s = this._$AH, i = e === c && s !== c || e.capture !== s.capture || e.once !== s.once || e.passive !== s.passive, n = e !== c && (s === c || i);
    i && this.element.removeEventListener(this.name, this, s), n && this.element.addEventListener(this.name, this, e), this._$AH = e;
  }
  handleEvent(e) {
    typeof this._$AH == "function" ? this._$AH.call(this.options?.host ?? this.element, e) : this._$AH.handleEvent(e);
  }
}
class qe {
  constructor(e, t, s) {
    this.element = e, this.type = 6, this._$AN = void 0, this._$AM = t, this.options = s;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(e) {
    A(this, e);
  }
}
const Ke = Z.litHtmlPolyfillSupport;
Ke?.(M, P), (Z.litHtmlVersions ??= []).push("3.3.3");
const Ze = (r, e, t) => {
  const s = t?.renderBefore ?? e;
  let i = s._$litPart$;
  if (i === void 0) {
    const n = t?.renderBefore ?? null;
    s._$litPart$ = i = new P(e.insertBefore(T(), n), n, void 0, t ?? {});
  }
  return i._$AI(r), i;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const J = globalThis;
class w extends x {
  constructor() {
    super(...arguments), this.renderOptions = { host: this }, this._$Do = void 0;
  }
  createRenderRoot() {
    const e = super.createRenderRoot();
    return this.renderOptions.renderBefore ??= e.firstChild, e;
  }
  update(e) {
    const t = this.render();
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(e), this._$Do = Ze(t, this.renderRoot, this.renderOptions);
  }
  connectedCallback() {
    super.connectedCallback(), this._$Do?.setConnected(!0);
  }
  disconnectedCallback() {
    super.disconnectedCallback(), this._$Do?.setConnected(!1);
  }
  render() {
    return k;
  }
}
w._$litElement$ = !0, w.finalized = !0, J.litElementHydrateSupport?.({ LitElement: w });
const Ge = J.litElementPolyfillSupport;
Ge?.({ LitElement: w });
(J.litElementVersions ??= []).push("4.2.2");
class me extends w {
  constructor() {
    super(...arguments), this._label = (e) => a(this.hass, `editor_${e.name}`);
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
class Je extends me {
  constructor() {
    super(...arguments), this.fields = [
      { name: "title", selector: { text: {} } },
      { name: "show_images", selector: { boolean: {} } },
      { name: "show_actions", selector: { boolean: {} } }
    ], this.defaults = { show_images: !0, show_actions: !0 };
  }
}
class Ye extends me {
  constructor() {
    super(...arguments), this.fields = [
      { name: "title", selector: { text: {} } },
      { name: "show_image", selector: { boolean: {} } },
      { name: "show_ingredients", selector: { boolean: {} } }
    ], this.defaults = { show_image: !0, show_ingredients: !1 };
  }
}
const Qe = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"], _e = "weeklymenu";
function $e(r) {
  const e = /* @__PURE__ */ new Map();
  for (const t of Object.values(r.entities ?? {}))
    t.platform === _e && t.translation_key && e.set(t.translation_key, t.entity_id);
  return e;
}
const $ = (r) => typeof r == "string" && r !== "" ? r : void 0, F = (r) => typeof r == "number" && Number.isFinite(r) ? r : void 0, I = (r) => Array.isArray(r) ? r.filter((e) => typeof e == "string") : [], E = (r) => typeof r == "object" && r !== null;
function Xe(r) {
  return (E(r) && Array.isArray(r.groups) ? r.groups : []).filter(E).map((t) => {
    const s = Array.isArray(t.substitutions) ? t.substitutions : [], i = (n) => E(n) ? $(n.raw) ?? $(n.name) ?? "" : "";
    return {
      members: I(t.members),
      share: F(t.share) ?? 0,
      separatePans: t.separate_pans === !0,
      swaps: s.filter(E).map((n) => ({
        original: i(n.original),
        replacement: i(n.replacement)
      }))
    };
  });
}
function et(r) {
  return Array.isArray(r) ? r.filter(E).filter((e) => typeof e.id == "string" && typeof e.title == "string").map((e) => ({ id: e.id, title: e.title })) : [];
}
function ye(r, e, t = "") {
  const s = e ? r.states[e] : void 0;
  if (!s || ["unknown", "unavailable", ""].includes(s.state)) return;
  const i = s.attributes, n = $(i.date);
  if (n)
    return {
      entityId: s.entity_id,
      weekday: t,
      date: n,
      title: s.state,
      recipeId: $(i.recipe_id) ?? "",
      url: $(i.url),
      image: $(i.image),
      source: $(i.source),
      totalTime: F(i.total_time),
      servings: F(i.servings),
      tags: I(i.tags),
      ingredients: I(i.ingredients),
      locked: i.locked === !0,
      alternatives: et(i.alternatives),
      split: Xe(i.split)
    };
}
function le(r) {
  const e = $e(r), t = r.states[e.get("status") ?? ""], s = t?.state, i = t?.attributes ?? {}, n = [];
  for (const o of Qe) {
    const h = ye(r, e.get(`weekday_${o}`), o);
    h && n.push(h);
  }
  return {
    status: s === "draft" || s === "confirmed" ? s : "none",
    weekStart: $(i.week_start),
    warnings: I(i.warnings),
    days: n
  };
}
function tt(r) {
  return ye(r, $e(r).get("today"));
}
function st(r) {
  const [e, t, s] = r.split("-").map(Number), i = new Date(Date.UTC(e, t - 1, s)), n = i.getUTCDay() || 7;
  i.setUTCDate(i.getUTCDate() + 4 - n);
  const o = Date.UTC(i.getUTCFullYear(), 0, 1);
  return Math.ceil(((i.getTime() - o) / 864e5 + 1) / 7);
}
function it(r) {
  return `${Math.round(r * 100)} %`;
}
function ve(r) {
  const [e, t, s] = r.split("-").map(Number);
  return new Date(Date.UTC(e, t - 1, s));
}
function ce(r, e) {
  const t = z(r), s = ve(e), i = { timeZone: "UTC" };
  return {
    weekday: new Intl.DateTimeFormat(t, { ...i, weekday: "short" }).format(s),
    date: new Intl.DateTimeFormat(t, { ...i, day: "numeric", month: "short" }).format(s)
  };
}
function rt(r, e) {
  return new Intl.DateTimeFormat(z(r), { timeZone: "UTC", weekday: "long" }).format(ve(e));
}
function nt(r, e) {
  const t = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"].indexOf(e);
  return t < 0 ? e : rt(r, `2026-11-${String(2 + t).padStart(2, "0")}`);
}
function we(r, e) {
  const t = `source_${e.source}`, s = e.source ? a(r, t) : "";
  return l`<div class="meta">
    ${e.totalTime ? l`<span>${a(r, "minutes", { n: e.totalTime })}</span>` : c}
    ${e.tags.map((i) => l`<span class="tag">${Se(r, i)}</span>`)}
    ${s && !s.startsWith("source_") ? l`<span class="badge">${s}</span>` : c}
    ${e.split.length ? l`<span class="badge split" title=${a(r, "split")}>${a(r, "split")}</span>` : c}
    ${e.locked ? l`<span class="badge">${a(r, "locked")}</span>` : c}
  </div>`;
}
function be(r, e) {
  return e.length ? l`<div class="split-note">
    <strong>${a(r, "split")}</strong>
    ${e.map(
    (t) => l`<div>
        ${t.swaps.map(
      (s) => l`<div>
              ${a(r, "splitNote", {
        members: t.members.join(", ") + ` (${it(t.share)})`,
        from: s.original,
        to: s.replacement
      })}
            </div>`
    )}
        ${t.separatePans ? l`<em>${a(r, "cleanPans")}</em>` : c}
      </div>`
  )}
  </div>` : c;
}
function xe(r, e) {
  return e.length ? l`<div>
    <h4>${a(r, "ingredients")}</h4>
    <ul>
      ${e.map((t) => l`<li>${t}</li>`)}
    </ul>
  </div>` : c;
}
function ot(r) {
  return r && typeof r == "object" && "message" in r ? String(r.message) : String(r);
}
const ke = Ce`
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
  .chip {
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
class at extends w {
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
    this.styles = ke;
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
    return this.hass ? 2 + le(this.hass).days.length : 4;
  }
  // --- actions ------------------------------------------------------------------
  async _call(e, t = {}) {
    this._busy = !0, this._error = "";
    try {
      await this.hass.callService(_e, e, t);
    } catch (s) {
      this._error = ot(s);
    } finally {
      this._busy = !1;
    }
  }
  _toggle(e) {
    const t = new Set(this._open);
    t.delete(e) || t.add(e), this._open = t;
  }
  _confirm(e) {
    window.confirm(a(this.hass, "confirmAsk")) && this._call("confirm_menu", e.weekStart ? { week_start: e.weekStart } : {});
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
    const e = this.hass, t = le(e), s = t.status === "confirmed", i = this._config.show_actions !== !1 && !s, n = [...new Set(t.warnings.map((o) => Ae(e, o, (h) => nt(e, h))))];
    return l`<ha-card .header=${this._config.title ?? a(e, "menuTitle")}>
      <div class="head">
        <span>${t.weekStart ? a(e, "week", { n: st(t.weekStart) }) : ""}</span>
        <span class="chip ${t.status}">${a(e, `status_${t.status}`)}</span>
      </div>
      ${n.map((o) => l`<div class="banner warning">${o}</div>`)}
      ${this._error ? l`<div class="banner error">${a(e, "error", { error: this._error })}</div>` : c}
      ${this._busy ? l`<div class="banner">${a(e, "working")}</div>` : c}
      ${t.days.length ? t.days.map((o) => this._renderDay(o, t, i)) : l`<div class="empty">${a(e, "noMenu")}</div>`}
      ${s && this._config.show_actions !== !1 ? l`<div class="banner">${a(e, "confirmedNote")}</div>` : c}
      ${this._renderFooter(t, i)}
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
        ${s ? a(this.hass, "generate") : a(this.hass, "regenerateAll")}
      </button>
      ${e.status === "draft" && !s ? l`<button class="primary" ?disabled=${this._busy} @click=${() => this._confirm(e)}>
            ${a(this.hass, "confirm")}
          </button>` : c}
    </div>`;
  }
  _renderDay(e, t, s) {
    const i = this.hass, n = ce(i, e.date), o = this._open.has(e.date), h = e.url ? l`<a href=${e.url} target="_blank" rel="noopener noreferrer" title=${a(i, "openRecipe")}>${e.title}</a>` : e.title, d = t.days.filter((u) => u.date !== e.date && !u.locked);
    return l`<div class="day">
      <div class="when">
        <div class="wd">${n.weekday}</div>
        <div class="dt">${n.date}</div>
      </div>
      <div class="main">
        ${this._config.show_images !== !1 && e.image ? l`<img src=${e.image} alt="" loading="lazy" />` : c}
        <div>
          <div class="title">${h}</div>
          ${we(i, e)}
        </div>
      </div>
      <div class="actions">
        ${s ? l`<button
              class="icon ${e.locked ? "on" : ""}"
              ?disabled=${this._busy}
              title=${e.locked ? a(i, "unlock") : a(i, "lock")}
              aria-label=${e.locked ? a(i, "unlock") : a(i, "lock")}
              aria-pressed=${e.locked ? "true" : "false"}
              @click=${() => this._call("lock_day", { date: e.date, locked: !e.locked })}
            >
              <ha-icon icon=${e.locked ? "mdi:lock" : "mdi:lock-open-variant-outline"}></ha-icon>
            </button>` : c}
        <button
          class="icon"
          title=${o ? a(i, "hide") : a(i, "show")}
          aria-label=${o ? a(i, "hide") : a(i, "show")}
          aria-expanded=${o ? "true" : "false"}
          @click=${() => this._toggle(e.date)}
        >
          <ha-icon icon=${o ? "mdi:chevron-up" : "mdi:chevron-down"}></ha-icon>
        </button>
      </div>
      ${o ? this._renderMore(e, d, s) : c}
    </div>`;
  }
  _renderMore(e, t, s) {
    const i = this.hass;
    return l`<div class="more">
      ${be(i, e.split)} ${xe(i, e.ingredients)}
      ${s ? l`<div class="row">
              <input
                type="text"
                .value=${this._hints[e.date] ?? ""}
                placeholder=${a(i, "hint")}
                aria-label=${a(i, "hint")}
                @input=${(n) => {
      this._hints = { ...this._hints, [e.date]: n.target.value };
    }}
              />
              <button ?disabled=${this._busy || e.locked} @click=${() => this._regenerateDay(e)}>
                ${a(i, "newDinner")}
              </button>
            </div>
            <div class="row">
              ${e.alternatives.length ? l`<select
                    ?disabled=${this._busy}
                    aria-label=${a(i, "alternatives")}
                    @change=${(n) => this._pick(e, n)}
                  >
                    <option value="">${a(i, "alternatives")}: ${a(i, "choose")}</option>
                    ${e.alternatives.map((n) => l`<option value=${n.id}>${n.title}</option>`)}
                  </select>` : c}
              ${t.length && !e.locked ? l`<select
                    ?disabled=${this._busy}
                    aria-label=${a(i, "swapWith")}
                    @change=${(n) => this._swap(e, n)}
                  >
                    <option value="">${a(i, "swapWith")}</option>
                    ${t.map((n) => {
      const o = ce(i, n.date);
      return l`<option value=${n.date}>${o.weekday} ${o.date}: ${n.title}</option>`;
    })}
                  </select>` : c}
            </div>` : c}
    </div>`;
  }
}
class lt extends w {
  static {
    this.properties = {
      hass: { attribute: !1 },
      _config: { state: !0 }
    };
  }
  static {
    this.styles = [
      ke
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
    const e = this.hass, t = tt(e), s = this._config.title ?? a(e, "todayTitle");
    if (!t)
      return l`<ha-card .header=${s}><div class="empty">${a(e, "noDinner")}</div></ha-card>`;
    const i = t.url ? l`<a href=${t.url} target="_blank" rel="noopener noreferrer" title=${a(e, "openRecipe")}>${t.title}</a>` : t.title;
    return l`<ha-card .header=${s}>
      <div class="day" style="grid-template-columns: 1fr">
        <div class="main">
          ${this._config.show_image !== !1 && t.image ? l`<img src=${t.image} alt="" loading="lazy" style="width:72px;height:72px" />` : c}
          <div>
            <div class="title">${i}</div>
            ${we(e, t)}
          </div>
        </div>
        <div class="more" style="padding-left:0">
          ${be(e, t.split)}
          ${this._config.show_ingredients ? xe(e, t.ingredients) : c}
        </div>
      </div>
    </ha-card>`;
  }
}
function W(r, e) {
  customElements.get(r) || customElements.define(r, e);
}
W("weeklymenu-menu-card", at);
W("weeklymenu-menu-card-editor", Je);
W("weeklymenu-today-card", lt);
W("weeklymenu-today-card-editor", Ye);
const D = { language: z({ language: navigator.language }) };
window.customCards = window.customCards ?? [];
window.customCards.push(
  {
    type: "weeklymenu-menu-card",
    name: a(D, "cardMenuName"),
    description: a(D, "cardMenuDescription"),
    preview: !0
  },
  {
    type: "weeklymenu-today-card",
    name: a(D, "cardTodayName"),
    description: a(D, "cardTodayDescription"),
    preview: !0
  }
);
