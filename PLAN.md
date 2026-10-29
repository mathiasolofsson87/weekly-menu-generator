# Weekly Menu Generator: HACS Integration Plan

A Home Assistant custom integration (distributed through HACS) that suggests a weekly dinner menu every Friday morning, respects each family member's allergies and preferences, lets the user swap individual recipes, and on confirmation puts the needed ingredients on a shopping list (a store provider and/or any HA to-do list). ICA is the first store provider because it is the largest in Sweden, but the integration is built so any store (Coop, Willys and others) can be added or can replace ICA.

## 1. Key risks

- **ICA Handla has no public API.** Login (BankID), product search and cart are only reachable through unofficial, reverse-engineered endpoints that may change or be restricted by ICA's terms. ICA is therefore a `ShoppingProvider` behind an abstraction, marked experimental, with the HA to-do list provider as a guaranteed fallback.
- **ICA recipes have no public API.** Likely route is the schema.org `Recipe` JSON-LD on ica.se pages. Store only title, ingredients, time, image and a link back; do not copy method text.
- **Allergies are safety-critical.** The LLM is never trusted alone: every candidate recipe from every source passes a deterministic ingredient check.
- Phase 0 is a spike to prove ICA login, recipe search, product search and cart add before committing to the ICA scope.

## 2. User flow

1. Friday 06:00 (configurable) the coordinator generates a draft menu for next week's selected weekdays.
2. A notification says the menu is ready, with actions Open / Confirm / Regenerate.
3. The user reviews on the dashboard: regenerate a single day (optional hint), lock days, swap days.
4. Confirm locks the menu, aggregates ingredients, removes pantry staples and sends them to the chosen shopping targets. A notification reports counts and unmatched items.
5. The confirmed week stays visible; "Today's dinner" is exposed for automations.

## 3. Configuration (UI only)

**Config flow:** shopping targets, AI Task entity, language (sv/en), units.

**Options flow:**
- Schedule: generation day/time, dinner weekdays.
- Family members: pick HA users; per person allergies (hard), dislikes/likes (soft), diet, portion size, per-day attendance.
- Meal styles: multi-select tags (vegetarian, quick, easy, fancy, family-friendly, budget...), defaults and per weekday; vegetarian days per week; fish at least once.
- Recipe sources: enable/disable and reorder (store recipes such as ICA, AI, curated/scraped last resort).
- Shopping targets: one or more `todo.*` entities and/or a store provider's list or cart (ICA in v1); separate "needs review" list.
- Pantry staples (never added).
- Notifications: `notify.*` targets and which events.
- Providers: each enabled recipe source and shopping provider contributes its own setup and re-auth step, owned by the provider (ICA in v1: credentials, store).

## 4. Architecture

```
custom_components/weeklymenu/
  __init__.py, manifest.json, config_flow.py, coordinator.py, scheduler.py
  planner/   generator.py, constraints.py, models.py
  sources/   base.py (RecipeSource), registry.py, ica.py, ai_task.py, curated.py
  shopping/  base.py (ShoppingProvider), registry.py, ica.py, todo.py, matcher.py
  store.py
  sensor.py, calendar.py, button.py, select.py, todo.py
  services.yaml, strings.json, translations/{en,sv}.json
frontend/    custom Lovelace cards (Lit + TypeScript)
hacs.json, README, brand assets, .github/workflows (hassfest, HACS validate, ruff, pytest)
```

### Provider-neutral design (ICA is a plugin, not the core)

ICA ships first, but nothing outside `sources/ica.py` and `shopping/ica.py` may know it exists. Another store (Coop, Willys, Hemköp, Mat.se) must be addable, or able to replace ICA completely, without touching the planner, storage, services, entities or cards.

- **Interfaces with capabilities.** `RecipeSource` and `ShoppingProvider` are the only things the core talks to. Optional features are declared as capability flags (cart, plain list, product matching, offers, prices) and the core checks the flag instead of the provider name.
- **Registry.** Providers register under an id (`ica`, later `coop`, `willys`). Config and storage hold provider ids; the source chain and shopping targets are lists of ids. Only the registry imports concrete providers.
- **Provider-owned pieces.** Each provider owns its auth (ICA: OAuth with personnummer and password; others may use BankID or API keys), its config schema and options/re-auth step, its translations, its API client, and the conversion of its recipe and ingredient formats into the neutral `Recipe` and `Ingredient` models. The core only learns "needs re-auth" and raises the repair issue.
- **Recipe and shopping providers are independent.** A user can take recipes from one store and shop at another, or use several recipe sources at once.
- **Neutral naming.** Entities, services, events, storage keys and card options never contain "ica". Provider-specific data (tokens, product match cache, store id) is namespaced by provider id.
- **Neutral models.** A `Recipe` carries `source` (provider id), `external_id` and `url`; the shopping push returns a neutral result (added, unmatched, link to the list or cart).
- **Proof it holds.** The test suite includes a fake second provider that runs through the same contract tests as ICA, so a hardcoded assumption fails a test.

### Recipe source chain (priority order)
1. Store recipe sources (ICA in v1; Coop, Willys and others later)
2. LLM through HA `ai_task` (Gemini configured) or conversation agent
3. Curated/scraped (opt-in, last resort)

Per day the planner asks sources in order for candidates, filters them through the constraint check, picks the best fit for the style tags, and falls through to the next source when nothing passes. Each entry records its source.

### Generation pipeline
1. Build context: family constraints, style tags, the last 4-6 weeks of meals, days to fill.
2. Fetch candidates from the source chain (AI uses a strict JSON schema).
3. Deterministic allergen/dislike check with sv/en synonym lists.
4. Store as `draft` with candidate lists per day (stable recipe IDs), then notify.

### Shopping pipeline on confirm
1. Merge duplicates, normalize units (dl, msk, st, g).
2. Remove pantry staples.
3. Push to each configured target. For providers that need product matching: match each item to a product, remember corrections (stored per provider).
4. Unmatched items go to the review list; nothing is dropped silently.

## 5. Entities and services

Entities: `sensor.weeklymenu_status`, `sensor.weeklymenu_today`, one sensor per weekday, `calendar.weeklymenu`, review `todo`, `button` generate/confirm, `select` style preset.

Services: `generate_menu`, `regenerate_day` (weekday, hint), `swap_days`, `lock_day`, `confirm_menu`, `add_to_shopping`, `set_recipe`.

Events: `weeklymenu_menu_ready`, `weeklymenu_confirmed`.

## 6. Dashboard cards (custom, with visual editors, HA theme aware)

1. **Menu card**: day rows with title, time, tags, source badge; regenerate / lock / hint per day; expandable ingredients; Regenerate all and Confirm buttons; status banner.
2. **Today card**: tonight's dinner, compact.
3. **Shopping result card**: added items, unmatched items, link to the store's list or cart.
4. **Family and preferences card**: edit allergies and preferences from the dashboard.
5. Stock-card YAML examples as an alternative.

## 7. Notifications

Menu ready (actionable), confirmed summary, problems (a provider's login expired, via HA repair/re-auth, AI failure, unmatched items), and a reminder if the draft is unconfirmed Saturday noon.

## 8. Language

Integration language (sv/en) is a user setting independent of HA's language. It drives UI strings, LLM prompt language, provider site/filters and allergen synonym lists.

## 9. HACS packaging

Public GitHub repo, `hacs.json`, complete `manifest.json`, CI (hassfest, HACS validate, ruff, pytest), tagged releases (zip asset for the card bundle), brand assets, README with sv/en docs and an ICA unofficial disclaimer. First as a HACS custom repository, then a PR to the default list once stable.

## 10. Phases

| Phase | Scope |
|---|---|
| 0 | ICA spike: login, recipe search, product search, cart add. Go/no-go |
| 1 | Scaffold, config/options flow, family members, schedule (**done 2026-10-29**; options flow so far has general, schedule and family; the other option pages arrive with the phase that uses them) |
| 2a | Provider interfaces, registry and fake-provider contract tests; AI Task source, generator, allergen validation, storage, `generate_menu`/`set_recipe` services, sensors (**done 2026-10-29**) |
| 2b | ICA recipe source (sitemaps, JSON-LD, local cache), calendar and button entities |
| 3 | Notifications with actions, per-day regenerate, lock, swap |
| 4 | Shopping aggregation (scaled by attendees and split shares), to-do provider, confirm flow |
| 5 | ICA shopping provider (as a plugin behind the registry), product matching, re-auth |
| 6 | Custom cards |
| 7 | Tests, translations, docs, HACS release |

## 11. Decisions made

- Recipe sources: store recipes first (ICA in v1), then ai_task/conversation, then curated/scraped last.
- ICA is the first store provider but is replaceable: Coop, Willys and others plug in through the same `RecipeSource` and `ShoppingProvider` interfaces and a registry (see "Provider-neutral design" in section 4). Nothing outside the ICA modules may hardcode ICA.
- Shopping targets are user-defined `todo.*` entities and/or a store provider (ICA list in v1).
- Custom Lovelace cards.
- Language user-defined (sv/en).
- AI backend: Gemini via Google Generative AI integration in HA.
- Voting is deferred to the roadmap.

## Phase 2a decisions (2026-10-29)

- **Allergies and diets are both hard rules** for whoever eats that day. A vegetarian member means every dinner they attend is vegetarian. Dislikes and likes are soft and only change ranking.
- **Rules check Swedish and English together**, regardless of the language setting, since a safe false positive beats a missed allergen. The title is checked as well as the ingredients. Rules live in `planner/allergens.py` with exceptions (`kokosmjölk`, `nötfärs`, `eggplant`) and free-from phrases (`glutenfri`, `laktosfri`, `växtbaserad`). It is a text filter, not a guarantee, and the README must say so.
- **Only attendees constrain a day.** With no members configured every dinner day is planned without constraints; days nobody attends are skipped.
- **Source chain:** sources are asked in registry order and the next one is only asked when the week cannot be filled with eligible recipes (at least three per day). A failing source adds a warning and the chain continues. Priority is fixed by the registry, so there is no reordering UI, only enable/disable.
- **Planner:** greedy day by day. Score = style-tag fit, repeat penalty (recipes from the last six weeks are also excluded from the request), dislike penalty, like bonus, and a reuse bonus for ingredients shared with days already picked. Vegetarian and fish quotas become hard filters only when every remaining day is needed and something qualifies. Cost and package-size terms wait for prices.
- **Each day stores up to three candidates** with stable ids (chosen recipe first), ready for regenerate/swap in phase 3 and voting later.
- **AI Task** is called through the `ai_task.generate_data` service with a structure schema, so the answer comes back as data. The structure is tested against Home Assistant's own validator.
- **Options flow** now has general, schedule, family members, meal styles (tags, vegetarian days, fish minimum) and recipe sources. Per-weekday style overrides are still to do.
- **Services:** `generate_menu` (replaces a draft, refuses a confirmed week) and `set_recipe` (pick one of a day's candidates, locks it). Events: `weeklymenu_generation_due`, `weeklymenu_menu_ready`.
- **Entities:** sensors for status, today's dinner and one per weekday, with ingredients and alternatives as attributes. Calendar and buttons come in 2b.

## Split dinners: one recipe, two proteins (2026-10-29)

A meat recipe whose only obstacle for a vegetarian is the protein still counts. Members who cannot eat it get a substitute and the others get the original.

- **Eligibility** (`planner/eligibility.py`): allergies are never split (a shared pan is not safe enough). A diet conflict can be split only if every offending ingredient line is a plain protein (meat, fish, shellfish) and not stock, fish sauce, anchovies, gelatin, dairy or egg. A conflict that exists only in the title never qualifies. At least one attendee must eat the original; otherwise the recipe is simply not eligible.
- **Substitutes** (`planner/substitutes.py`): the protein kind decides the options in order (mince: vegofärs, red lentils, chickpeas; sausage: vegokorv; cured meat: smoked tofu, portobello; poultry, fish and steak: tofu, portobello, halloumi, chickpeas). Amounts are converted by weight, and counted pieces become grams (a chicken fillet is 150 g, a steak 200 g). The first option that is safe for everyone receiving it wins. Each product declares the allergens it may contain on purpose (vegofärs: soy and gluten) because its name does not show them.
- **Stored on the day** as `MenuDay.split`: who gets the substitute, the swaps (original and replacement at full recipe scale) and the portion share, weighted by portion size. Phase 4 buys the original for the remaining share and the substitute for `share`. The weekday sensors expose it as the `split` attribute.
- **Planner:** a split is ranked below a recipe everyone can eat as is, and `max_split_days` (default 2, in Meal styles) caps how many dinners per week need two proteins. The cap gives way only to avoid an empty day, with a warning.
- **AI Task** is told to keep the protein on its own line and out of sauces and stocks, but only when family diets differ. Whether a recipe really is splittable is decided by the deterministic check, never by the model.
- **Known limits:** one substitute group per dinner (a vegan and a vegetarian with different needs are served the same substitute, or the recipe is not eligible), and the swap quantities are estimates.
- **Later:** per-person cooking instructions in the card ("for Anna: fry tofu instead"), and offering a split for dislikes.

## 12. Phase 0 findings (2026-10-25)

**ICA recipes (good news):** `https://www.ica.se/recept/<slug>-<id>/` pages return HTTP 200 with a schema.org `Recipe` JSON-LD block containing name, image, totalTime (ISO 8601), recipeYield, recipeCategory, recipeIngredient (list of strings), recipeInstructions, rating and nutrition. Category pages exist: `/recept/vegetarisk/`, `/recept/enkel/`, `/recept/under-30-minuter/`, `/recept/middag/`. `robots.txt` has no general disallow for `/recept/` (only for AI crawlers GPTBot and meta-externalagent on deep paths) and lists recipe sitemaps at `/recept/sitemaps/`. Plan: discover recipes via the sitemaps and category pages, parse the JSON-LD, cache locally, rate limit politely, send an honest User-Agent, and store only the metadata and ingredients with a link back. Ingredients are free-text strings and need parsing into amount, unit and name.

**ICA shopping (hard part):**
- The old documented API (`handla.api.ica.se`, personnummer + Buffé password) was changed by ICA in April 2024 and is no longer valid.
- A community project (`kanylbullen/ica-mcp`) shows a current route: OAuth2/OIDC with PKCE via `ims.icagruppen.se`, personnummer and password login (BankID-only accounts not supported), 15-minute access tokens with refresh, and a data API at `apimgw-pub.ica.se`, which returns HTTP 451 to non-Swedish IPs. It supports shopping lists (create, add, check, remove items) and adding recipe ingredients to a list.
- That project describes **shopping lists, not the online-shopping cart**. A cart-add endpoint for ICA Handla online is unproven, so the realistic v1 ICA target is the ICA shopping list, with the cart still to be verified.
- Needs a real ICA login to test further, so the remaining spike steps need credentials from the user.

**Your HA:** only two `todo` lists are exposed to Assist (Ellikas Poäng Redeemed rewards, Maintenance); no shopping list is exposed. No `ai_task` entity is visible through the MCP connection, but the MCP view only shows entities exposed to Assist, so this does not prove it is missing.

## 13. Decisions and ICA API details (2026-10-25)

- **ICA target for v1: the ICA shopping list** (the list in the ICA app), not the online-shopping cart.
- Login flow (from LazyTarget/ha-ica-todo via kanylbullen/ica-mcp, both MIT): OAuth2 + PKCE against `ims.icagruppen.se` using a public dynamic client registration, personnummer + password, then Bearer tokens (about 15 min) with refresh token.
- Shopping list API on `apimgw-pub.ica.se/sverige/digx/mobile/shoppinglistservice/v1/shoppinglists`: list, create, delete list; `POST .../{offlineId}/sync` with `createdRows`, `changedRows`, `deletedRows`. Rows are free text (`productName`, `quantity`, `unit`, negative `sourceId`), so there is no product matching problem for the list route.
- The app API also has recipe endpoints (`recipeservice/v1`: recipe by id, favorites, random), as an alternative to scraping ica.se.
- Risks: unofficial API, public client secret may be rotated, geo-blocked outside Sweden (HA must run with a Swedish IP), password stored in HA config entry storage, BankID-only accounts unsupported. Implement tokens via HA re-auth flow and a repair issue on failure.
- Spike script: `spikes/ica_spike.py` (needs `pip install requests`; run it yourself in a normal terminal so the password stays out of chat). It logs in, creates and deletes a temp list.
- **Spike result (2026-10-29): PASS.** Personnummer + password login works, the account's list endpoint returned (no existing lists), a temp list was created, two free-text rows (`nötfärs` 350 g, `gul lök` 2 st) were written and read back with the correct quantity and unit, and the list was deleted. The ICA shopping list route is verified for v1. The online-shopping cart is still unverified and stays out of scope. The run was from a Swedish IP, so the geo-block is not tested from outside Sweden.

## 14. Waste- and budget-aware planning (2026-10-25)

The generator plans the whole week at once rather than picking each day independently, and scores candidate menus on waste and cost as well as constraints and style.

**Waste (v1):**
- Reward menus where ingredients are reused across days, so a package bought for one recipe is finished by another (cream, feta, a whole cabbage, herbs).
- Penalize ingredients that appear once and are likely to leave a large remainder, using package-size heuristics (for example, 1 dl of cream from a 2 dl pack).
- When a day is regenerated, the replacement is scored against the rest of the week, so it does not break the overlap.
- The shopping step rounds amounts up to sensible package sizes and shows the expected remainder.

**Budget (v1):**
- Optional weekly budget (SEK) and a per-meal ceiling in the options flow, with a "cheap", "normal", "no limit" preset.
- Cost estimate per recipe: store offers from the shopping provider's optional `offers` capability (ICA: `offerservice/v1/offersdiscounts/{storeId}`, endpoint seen in ica-mcp, to be verified) for discounted items, and AI-estimated or manually maintained prices for the rest. Estimates are labelled as estimates in the UI.
- Offer-aware picks: prefer recipes using items on offer at the user's chosen store this week (when the provider supports offers).
- The menu card shows estimated total cost against budget; over-budget menus are flagged and the generator tries cheaper candidates first.

**Stock-aware planning (needs the inventory in ROADMAP v3):**
- Estimated leftover amounts per ingredient are passed to the recipe sources as "use up" ingredients and boost matching recipes.
- v1 ships a manual "I have these at home" list (free text, optional amounts) as a bridge. It feeds the same scoring and is subtracted from the shopping list.

**Implementation notes:**
- Ingredients are structured (name, amount, unit, category) from day one.
- Scoring is deterministic code in `planner/scoring.py` (waste, cost, variety, style fit). The LLM proposes candidates; code ranks and validates the menu.
- Unknown prices and package sizes degrade gracefully: the score term is skipped, not guessed silently.
