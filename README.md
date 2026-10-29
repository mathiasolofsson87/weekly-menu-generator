<p align="center"><img src="custom_components/weeklymenu/brand/logo@2x.png" alt="Weekly Menu Generator" width="480"></p>

# Weekly Menu Generator

A Home Assistant integration that plans the family's dinners for the coming week, respects every family member's allergies and diet, lets you change any single dinner, and on confirmation puts the ingredients on your shopping lists (Home Assistant to-do lists and/or the ICA app).

*Svenska: [README.sv.md](README.sv.md)*  ·  License: [MIT](LICENSE)  ·  Third-party notices: [NOTICE.md](NOTICE.md)

> **Status:** version 0.1.0, not released yet. It has been tested with automated tests only, not yet in a live Home Assistant. Expect rough edges.

## Please read first

- **Allergies.** The integration filters recipes by reading ingredient lists, in Swedish and English. This is a **best-effort text filter, not a guarantee**: it can only see what a recipe lists, and it is deliberately cautious (it would rather drop a safe recipe than allow an unsafe one). **Always check ingredient labels and recipes yourself**, especially for severe allergies. Do not rely on this for medical decisions.
- **ICA is unofficial.** There is no public ICA API. The integration reads recipe pages on ica.se and uses the interface of the ICA app for the shopping list. ICA can change or block either at any time, and ICA's own terms apply to your use of their services. This project is not affiliated with or endorsed by ICA.
- **ICA only answers connections from Sweden**, so Home Assistant needs a Swedish IP address for the ICA shopping list.
- **Your ICA personnummer and password are stored in Home Assistant's configuration** (as most integrations store credentials). Accounts that only use BankID cannot be used.

## What it does

Every Friday morning (configurable) it drafts a menu for next week, for the weekdays you choose, and notifies you. You review it on your dashboard: regenerate one dinner (with an optional wish), lock the ones you like, swap two days, or pick one of the alternatives. Confirming locks the menu and builds the shopping lists.

- **Recipes** come from, in this order: **ICA recipes** (popular dinner recipes from ica.se, Swedish) and an **AI Task** entity of your choice (for example Gemini). The AI is never trusted with safety: every recipe from every source passes the same checks.
- **Family:** each person has allergies (hard rules), diet (hard rule), dislikes and likes (soft), portion size, and the days they eat dinner. Only people eating that day constrain that day.
- **One recipe, more than one version.** If the only thing in the way for some people is an ingredient that can be swapped, the dinner is still used: the steak recipe stays, and the vegetarian gets tofu; the pasta dish stays, and the milk-allergic person gets oat cream, cooked in clean, separate pans. A dinner can have up to two extra versions, and a per-person setting lets you say that someone's allergy must **never** be handled this way. Recipes with stock, anchovies, egg, soy or nuts in the way are not split.
- **Variety and waste:** recipes from the last six weeks are avoided, vegetarian and fish dinners per week are honoured, and recipes that share ingredients with the rest of the week rank higher so packages get finished.
- **Shopping:** amounts are scaled by who eats each day, merged across recipes, rounded up to something you can buy, and cleaned of wording like "gärna ICAs nötfärs 12% eller hushållsfärs". Pantry staples (salt, oil...) are skipped but listed. Items a store cannot place go to a review list; nothing is dropped silently.
- **Notifications** (through the Home Assistant app): menu ready with **Open / Confirm / Regenerate** buttons, problems, confirmed, and a Saturday-noon reminder.
- **Dashboard cards:** menu, today's dinner, shopping result and family, all with visual editors and in Swedish or English.

## Install

Through HACS: add this repository as a **custom repository** (category *Integration*), install **Weekly Menu Generator**, restart Home Assistant. Manually: copy `custom_components/weeklymenu` into your configuration's `custom_components` folder and restart.

Needs Home Assistant 2025.8 or newer.

## Set up

1. *Settings → Devices & services → Add integration → Weekly Menu Generator.* Choose language (Swedish or English, independent of Home Assistant's language), units, the to-do list(s) for shopping and, optionally, an AI Task entity.
2. Open the integration and choose **Configure**:
   - **Schedule:** the day and time to draft the menu, and which weekdays need a dinner.
   - **Family members:** add everyone, with allergies, diet and the days they eat.
   - **Meal styles:** preferred styles, vegetarian days, fish dinners, and how many dinners per week may have more than one version.
   - **Recipe sources:** switch ICA recipes and AI Task on or off.
   - **Shopping:** to-do lists, a list for items needing a look, and your pantry staples.
   - **Store accounts:** your ICA login, to use an ICA shopping list (a new list each week, or one fixed list).
   - **Notifications:** `notify` services (for example `mobile_app_your_phone`), what to notify about, and where *Open* leads.
3. Add the cards to a dashboard (see below), and press **Generate menu** to try it before Friday.

If ICA stops accepting your login, Home Assistant asks you to sign in again, and what could not be delivered waits until you do (`add_to_shopping` delivers it).

## Dashboard cards

The cards are added to your dashboards automatically; they appear in the card picker as **Weekly menu**, **Tonight's dinner**, **Shopping result** and **Family**. They find the integration's sensors themselves, so no entity needs to be configured.

```yaml
type: custom:weeklymenu-menu-card
title: Dinner this week   # optional
show_images: true
show_actions: true        # false makes it read-only
```

More examples, including stock cards and automations, are in [docs/dashboard-examples.md](docs/dashboard-examples.md). If a card does not show up, reload the page without cache; the cards are registered when Home Assistant starts, and need the Home Assistant frontend.

## Services

| Service | What it does |
|---|---|
| `generate_menu` | Draft the menu for a week (default: next week). Locked days are kept. |
| `regenerate_day` | A new dinner for one day, planned around the rest of the week. Optional wish. |
| `lock_day` | Lock or unlock a dinner. |
| `swap_days` | Swap two dinners of the same week. |
| `set_recipe` | Pick one of a day's alternatives (also locks the day). |
| `confirm_menu` | Lock the menu and build the shopping lists. A confirmed menu cannot be changed. |
| `add_to_shopping` | Retry what could not be delivered (or resend everything). |
| `set_member`, `remove_member` | Edit the family. Applies to menus made from now on. |

Events: `weeklymenu_generation_due`, `weeklymenu_menu_ready`, `weeklymenu_confirmed` (with shopping counts). Entities: sensors for status, tonight's dinner, each weekday, shopping and family; a calendar of planned dinners; buttons to generate and confirm.

## Privacy

Home Assistant talks to: **ica.se** (recipe pages), **ICA's app interface** (only if you set up an ICA list, with your login) and your **AI Task** provider. The AI is sent a request that names allergies, dislikes, diets and style wishes as plain words, **not** the names of your family members. Menus, the family and cached recipes are stored locally in Home Assistant.

## Known limits

- ICA recipes are Swedish, and only about the twenty most popular recipes per dish type are reachable.
- Plurals are not merged in shopping ("gul lök" and "gula lökar" stay two lines), and the lists are not sorted by store aisle.
- The wish for a regenerated dinner is only used by AI Task.
- Swap amounts for split dinners are estimates.

## Troubleshooting

- **No menu was made, or days are empty.** Open the *Status* sensor: its attributes list warnings, for example that no recipe source is active, or that no recipe fits everyone on a day. Check *Configure → Recipe sources* and that an AI Task entity is set.
- **ICA says it is blocked.** It only answers connections from Sweden.
- **Notification buttons do nothing.** They need the Home Assistant app and a `notify.mobile_app_…` service.

## Development

```
pip install -r requirements-test.txt && pip install $(python scripts/ha_extra_requirements.py)
pytest && ruff check . && ruff format --check .

cd frontend && npm ci && npm test && npm run build   # commit the rebuilt bundle
```

`PLAN.md` holds the design and decisions, `ROADMAP.md` what may come later, and `CLAUDE.md` the working notes.

## License

[MIT](LICENSE). The ICA login flow was ported from [LazyTarget/ha-ica-todo](https://github.com/LazyTarget/ha-ica-todo) via [kanylbullen/ica-mcp](https://github.com/kanylbullen/ica-mcp) (both MIT; thank you), and the dashboard bundle contains Lit (BSD-3-Clause). Their notices are in [NOTICE.md](NOTICE.md).
