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
| 2b | ICA recipe source (dish-type pages, JSON-LD, persistent cache), calendar and generate button (**done 2026-10-29**) |
| 3 | Notifications with actions, per-day regenerate, lock, swap, confirm (**done 2026-10-29**) |
| 4 | Shopping aggregation (scaled by attendees and split shares), to-do provider, confirm flow (**done 2026-10-29**) |
| 5 | ICA shopping provider (as a plugin behind the registry), re-auth (**done 2026-10-29**, with open checks below); product matching waits for the cart |
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

## Phase 5: ICA shopping list (2026-10-29)

Code is in `shopping/ica/` (`auth.py` login, `api.py` list API, `provider.py`, `setup.py` account form). Only `shopping/registry.py` imports it.

- **Target:** the ICA app's shopping list, with free-text rows (name, quantity, unit). **No product matching**: that only matters for the online cart, which is still unproven, so the `product_matching` capability and the review-list path stay unused by ICA for now (the path is covered by a fake provider in the tests).
- **Login:** the flow proven by the Phase 0 spike (OAuth2 + PKCE through `ims.icagruppen.se`, personnummer and password, a dedicated cookie jar), ported to async. **Nothing is kept between uses:** tokens last ~15 minutes and shopping happens once a week, so each push logs in fresh. That removes refresh handling, which could not be verified without credentials.
- **Credentials** (personnummer and password) are stored in the config entry, as Home Assistant integrations usually do. Leaving the password empty when editing keeps the saved one. BankID-only accounts do not work. ICA answers connections from outside Sweden with HTTP 451, which is reported as such.
- **Lists:** either a new list for each week (`Veckomeny vecka 45`) or one fixed, named list, found by title (case-insensitive) or created. Rows already on the list are skipped, so retrying `add_to_shopping` never duplicates anything. Counted things are written in pieces (`st`); a row without an amount is written as quantity 1 with no unit.
- **Setup is provider-owned.** A `ProviderSetup` (form, validation, config keys, which fields re-auth asks for) is registered next to the provider. The options flow shows a *Store accounts* page and the config flow a re-auth step, both generic: neither knows ICA exists. Leaving the personnummer empty switches ICA off.
- **When the login stops working** the items stay `failed` (retryable), the menu stays confirmed, the confirmed notification says so in plain language, and Home Assistant starts its re-authentication flow for the provider. Entering the password again checks it, updates the entry and reloads. Then `add_to_shopping` delivers what waited. HA's re-auth flow is the "repair" the plan asked for; a separate repair issue would only repeat it.
- **Verified with the user's login (2026-10-29, `spikes/ica_rows_spike.py`):** ICA accepts every row shape written here: g, dl, msk, förp, st and kg, no unit, and a long name. A list answer has `id` and `offlineId`; `offlineId` is the one that matches the id we create and use in URLs, and lists are found by title. An empty-string unit and a missing unit both read back as none. **A quantity of 0 reads back as no quantity** (the row shows just its name), whereas 1 with no unit would show a stray "1", so rows without an amount are written with quantity 0.
- **Known limits:** the app interface is unofficial and may change; the DCR client secret in `auth.py` is the app's public one and may be rotated; an ICA list is not read back to see whether a family member ticked things off.

## Phase 4: shopping (2026-10-29)

Confirming a menu now builds the shopping lists. Code is in `shopping/`: `aggregate.py` (pure), `delivery.py`, `base.py` + `registry.py` (the provider interface, like the recipe side) and `todo.py` (the first provider).

- **Scaling:** each dinner is scaled by the portions eaten that day over the recipe's servings (a normal portion counts 1, small 0.6, large 1.4). With no members, or no stated servings, the recipe is bought as written.
- **Split dinners:** a swapped ingredient is bought for the share of portions that keeps it, and its replacement for each group's share. Replacements are marked `special`, so a pantry staple like flour can never swallow "gluten-free flour".
- **Merging:** the same name is added up across recipes after converting to a common unit (ml and g), then rounded up to something you can buy: grams to 5, kilograms and litres to 0.1, dl and msk to 0.5, whole pieces for counted things, half teaspoons for small spice amounts. Units that cannot be converted (1 förp vs 2 dl) stay separate lines, so nothing is lost. Swedish units (dl, msk, tsk) or metric (ml) follow the Units setting.
- **Names:** ICA's wording is cut at "gärna", "eller", "alt.", a percentage and so on ("nötfärs gärna ICAs nötfärs 12% eller hushållsfärs" becomes "nötfärs"), and the original text is kept as the item's note and shown as the to-do description when the list supports descriptions.
- **Pantry staples** are never added but are listed as skipped, matched on whole words. Options hold the list (default: salt, pepper, water, oil, sugar, flour and a few more); an empty list means "buy everything".
- **Delivery:** every item ends in exactly one state: `added` (any provider took it), `review` (a provider could not place it, so it went to the review list), `failed` (nobody could deliver it; retry with `add_to_shopping`), `skipped` (pantry), or `pending` (no list is set up yet). Confirmation is saved before shopping starts, so shopping trouble never undoes it.
- **Services:** `add_to_shopping` retries what failed or waited, or with `everything` sends the whole list again (which can duplicate lines).
- **Entities and events:** `sensor.…_shopping` (items added, with added, review, failed, skipped, targets and errors as attributes, for the phase 6 card), `weeklymenu_confirmed` now carries the counts, and the confirmed notification says how many items were added, need review, failed or were skipped.
- **Options:** a Shopping page (lists, review list, pantry); the lists moved there from General, which previously would have been overwritten on save.
- **Known limits:** plurals are not merged ("gul lök" and "gula lökar" stay two lines), the lists get no store-aisle sorting, package-size rounding beyond the steps above and "I have this at home" subtraction (section 14) are still to do, and the to-do provider cannot tell when a line is already on the list.

## Phase 3: editing the menu and notifications (2026-10-29)

- **Services:** `regenerate_day` (optional hint), `swap_days`, `lock_day`, `set_recipe` (pick one of a day's alternatives, which also locks it) and `confirm_menu`, besides `generate_menu`. All operations live in the coordinator and run under one lock, so a notification button and a dashboard click cannot collide.
- **Regenerating a day** plans the new dinner around the rest of the week: the others count for variety, shared ingredients, the vegetarian and fish quotas and the split limit. The day's old alternatives are excluded so the result is genuinely new. If nothing better is found, the old dinner stays and an error says so. Locked days refuse it.
- **Regenerating the whole menu** keeps locked days (recipe and split) and plans only the rest. A kept day whose weekday is no longer a dinner day is dropped.
- **Swap** needs two unlocked dinners in the same week. Each recipe is re-checked against who eats on its new day (allergies, diets, new split). If either does not suit, nothing changes.
- **Confirm** marks the latest draft (or a given week) as confirmed, stores `confirmed_at` and fires `weeklymenu_confirmed`. A confirmed menu refuses every edit, including regenerating the week. Building the shopping lists on confirm is phase 4. Missing days are allowed through confirm and are reported in the warnings.
- **Notifications** go through `notify.<target>` services chosen in Options (the mobile app, for example) and are driven by the integration's own events, so automations see the same things:
  - *Menu ready* (`weeklymenu_menu_ready`): a day-by-day summary, a note on dinners cooked in several versions, and the buttons Open (a dashboard path from Options), Confirm and Regenerate.
  - *Problems*, sent separately: a recipe source failed, a day got no recipe, no source is active.
  - *Confirmed*, and a *reminder* on Saturday at 12:00 when next week's draft is still unconfirmed.
  - Each of the four can be switched off. Text follows the integration language, not Home Assistant's, including error messages from the buttons.
- **Buttons** on a notification arrive as `mobile_app_notification_action` events with the action `WEEKLYMENU_CONFIRM:<week>` or `WEEKLYMENU_REGENERATE:<week>`. Other actions are ignored. Using Confirm on an already confirmed week sends a problem notification instead of failing silently.
- **Entities:** a *Confirm menu* button next to *Generate menu*.
- **Not done:** the dashboard cards (phase 6) will call these services; notification text for ICA login problems arrives with phase 5; the hint is only used by AI Task (ICA ignores it).

## Phase 2b: ICA recipe source (2026-10-29)

Checked against ica.se on 2026-10-29. Code is in `sources/ica/` (`parser.py` is pure, `source.py` does the requests and the cache), and the registry puts it first in the chain.

- **What ica.se offers:** the recipe sitemaps list ~30,000 recipes but only as slugs, and category pages do not paginate (query parameters are ignored; "load more" is client-side). Instead, `/recept/middag/` embeds ~680 filter paths, ~200 of them single-level dish types (`/recept/middag/pasta/`, `gryta`, `soppa`, `kottbullar`...), and each page lists the ~20 most popular matching recipes. Recipe pages carry a schema.org `Recipe` with title, image, `totalTime`, `recipeYield`, `recipeCategory` (for example "Huvudrätt,Middag"), cuisine and ingredient lines.
- **Discovery:** each run reads the dish-type list (cached 30 days), then a few random dish-type pages (cached 14 days) for recipe URLs, so the pool changes week to week without crawling. Recipe pages are read once and cached for 90 days (up to 600 dinners). Desserts, baking, drinks and holiday pages are skipped by path, and by `recipeCategory` on the recipe itself (must say Middag or Huvudrätt).
- **Politeness:** an honest `User-Agent` with the repo URL, one request per second, at most 6 listing pages and 40 recipe pages per run, a single failed page is skipped, and three failures in a row end the run. Pages are ~300-550 KB, so the first run costs a few MB and later runs usually cost nothing. `robots.txt` has no disallow for general crawlers on `/recept/` (only for AI crawlers on deep paths).
- **What is stored:** title, image URL, time, servings, ingredient lines and a link back. Method text is not stored or shown. Add a note to the README that this uses ica.se pages without an API, may stop working, and that ICA's terms apply.
- **Planner hook:** `CandidateRequest.accept` is a predicate from the planner. A source may use it to skip candidates nobody could eat, so it does not spend its quota on hopeless ones. The planner still re-checks every recipe.
- **Tags:** `quick` (30 minutes or less), `easy`, `fancy`, `family_friendly`, `budget`, `vegetarian`, `fish`, derived from ICA's own labels.
- **Known limits:** recipes are Swedish whatever the language setting; ingredient names keep ICA's trailing remarks ("nötfärs gärna ICAs nötfärs 12% eller hushållsfärs"), which phase 4 must clean before shopping; only the ~20 most popular recipes per dish type are reachable; if ica.se changes its layout the source reports it and the chain falls through to AI.
- **Found by running it live:** `sojayoghurt` was treated as dairy, so milk-allergic members could not get a yoghurt swap. Fixed, with plant-based yoghurts added to the dairy exceptions.
- **Entities added:** `calendar.weekly_menu_generator_dinner_menu` (all-day events, the ingredients as description) and `button.weekly_menu_generator_generate_menu`.

## Split dinners: one recipe, more than one version (2026-10-29)

If the only thing in the way for some members is an ingredient that can be swapped, the dinner is still served. Those members get an adjusted version, cooked separately, and everyone else eats the recipe as written. This covers diets (meat for a vegetarian) and allergies (cream for a milk allergy, pasta for gluten, salmon for a fish allergy), because the allergen can be swapped and cooked in clean, separate pans.

- **Eligibility** (`planner/eligibility.py`): each member who breaks a rule is matched to the exact ingredient lines that break it. Members with the same lines share a version, with at most two alternative versions per dinner. At least one attendee must eat the original. A conflict that exists only in the title never qualifies (the listing may be incomplete). Stock, fish sauce, anchovies and gelatin block the split, and so does any line with no known swap (egg, soy, nuts, sesame, mustard, celery...). After swapping, the adjusted version is checked again for the group; anything left over rejects the recipe.
- **Swaps** (`planner/substitutes.py`), tried in order and taken only if safe for the whole group:
  - mince: vegofärs, red lentils, chickpeas; sausage: vegokorv; cured meat: smoked tofu, portobello; poultry, fish, shellfish and other meat: tofu, portobello, halloumi, chickpeas;
  - dairy: lactose-free first (right for lactose intolerance, wrong for milk allergy or vegans), then oat cream, oat drink, plant-based margarine, plant-based `{name}`;
  - gluten: gluten-free `{name}`, rice noodles, quinoa or rice for couscous and bulgur, gluten-free flour.
  Amounts are converted by weight and counted pieces become grams. Each product declares the allergens it may contain on purpose (vegofärs: soy and gluten) because its name does not show them.
- **Per-member switch** "Allergens can be cooked separately" (default on). Off means recipes containing that person's allergen are never suggested; it is meant for severe allergies. It does not affect diets.
- **Stored on the day** as `MenuDay.split`: a list of groups, each with members, swaps (original and replacement at full recipe scale), portion share (weighted by portion size) and `separate_pans`, which is set whenever an allergy is involved so the card can say "clean pan and utensils". Phase 4 buys the replacement for each group's share and the original for the remainder. The weekday sensors expose it as the `split` attribute.
- **Planner:** a split ranks below a recipe everyone can eat as is, and `max_split_days` (default 2, in Meal styles) caps how many dinners per week need more than one version. The cap gives way only to avoid an empty day, with a warning.
- **AI Task** is told to keep meat, fish, dairy and gluten on their own ingredient lines when diets differ or allergies exist. Whether a recipe really is splittable is decided by the deterministic check, never by the model.
- **Known limits:** swap amounts are estimates, an adjusted version for several people with different needs is limited to two groups, and the filter only sees what the recipe lists.
- **Later:** per-person cooking instructions on the menu card ("for Anna: fry tofu instead, in a clean pan"), swaps for egg, soy and nuts, and splits for dislikes.

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
