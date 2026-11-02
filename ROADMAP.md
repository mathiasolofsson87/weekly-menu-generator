# Roadmap

Ideas after the v1 release described in `PLAN.md`.

## Favorites and ratings: built, with these left over
Per-member ratings and favorites are in (see `PLAN.md`, "Favorites and ratings"). Still open:

- **Spreading favorites over the week** when members have different favorites, so everyone gets one now and then. Today a recipe's bonus follows the share of the table that has it as a favorite, which tends to do this by itself but does not guarantee it.
- **An explicit "explore" share**, so the menu never ends up only repeating known dishes. Today unrated recipes are neutral and ties are broken at random.
- **A "How was it?" notification** after a dinner day, asking each person who ate it for stars.
- **Dropping low-rated recipes** from the cache of known recipes.
- **Favorites in the menu card's alternatives list**, with each attendee's rating next to the alternative.

## Own recipes
Let the family write their own recipes, kept in a recipe list inside the integration.

- **A recipe list:** a "My recipes" list stored by the integration (its own storage file, like favorites). Each recipe has a title, ingredients with amounts and units, time, servings, tags (the same style tags the planner already uses), an optional picture and link, and notes (method, tips).
- **Create and edit:** from a dashboard card (a form like the family card's) and through services (`add_recipe`, `update_recipe`, `remove_recipe`). Ingredients are typed one per line, such as "350 g nötfärs", and read by the same parser as other sources, with the parsed result shown so a typo is easy to see.
- **A recipe source:** the list is a recipe source like ICA and AI Task, asked first or alongside the favorites source, with its own on/off switch and a setting for how big a share of a menu may come from it. The planner treats it exactly as any other source: allergy and diet checks, split dinners, scoring, ratings and favorites all apply, and a family recipe can be rated and favorited.
- **Allergens are not trusted from the author:** a person writing a recipe may leave an allergen out of the ingredient list or write it as a brand name. The filter only sees the text, so the card shows which allergens and diets the recipe was recognised as containing or fitting, and a recipe with no ingredients, or with ingredients the parser could not read, is flagged instead of treated as safe.
- **Bringing recipes in:** add a recipe from an ICA recipe (copy it to edit), from a pasted block of text, or from a link when the page has structured recipe data. Starting from a favorite or a menu dinner ("save a copy and change it") is the common case.
- **Sharing in the family:** every member can add and edit recipes, with "added by" shown. Whether a recipe can be private to one member is an open question.
- **Shopping:** nothing special; ingredients flow through the same scaling, merging and shopping lists as any recipe.
- **Open questions:** whether to keep a version history for edits, what happens to a recipe that is on a confirmed menu when it is edited (the menu keeps its copy), and a size limit for the list.

## v2: Family voting
- Each menu day offers several candidate recipes (v1 already stores candidate lists with stable recipe IDs).
- Family members (linked to HA user IDs) vote from the dashboard card or through notification actions.
- The top-voted recipe wins; if the voting deadline passes, the planner auto-picks.
- Optional veto per person and weighting by who is eating that day.

## v3: Pantry and leftover awareness
The integration gradually learns what is in the kitchen and uses it when planning.

- **Inventory model:** every confirmed shopping list adds items with their package size (e.g. 500 g minced meat, 1 L cream, 10 eggs). Each recipe's required amount is subtracted when the meal is cooked, so the estimated remainder is tracked per ingredient (e.g. 150 g left of a 500 g pack).
- **Package sizes:** where known, from the ICA product data (name, volume, weight); otherwise inferred from the shopping list text or entered by the user.
- **Leftover prompts:** after confirming the menu, or when generating the next one, the generator asks "Do you still have about 150 g of cream and half a pack of feta?" and the user confirms, corrects or dismisses it. Answers refine the inventory.
- **Planning use (builds on the manual "at home" list from v1; see PLAN.md section 14):** confirmed leftovers are passed to the recipe sources as ingredients to use up, preferably within their shelf life. Recipes that use them rank higher.
- **Shopping use:** when building the list, subtract what is already at home so the same item is not bought twice.
- **Shelf life:** optional expiry estimates per ingredient type (fresh produce, dairy, frozen), with a nudge to use things up first.
- **Corrections:** a dashboard card to view and edit the inventory, plus a quick "I'm out of this" action.
- **Data model groundwork in v1:** ingredients are stored as structured data (name, amount, unit) rather than raw strings, and each shopping push records what was bought, so the inventory can be built from history later.

## v4: Other stores and recipe sources (Coop, Willys, ...)
ICA is the v1 provider because it is the largest chain. The v1 architecture keeps providers pluggable (see "Provider-neutral design" in `PLAN.md` section 4), so a new store is a new provider module and not a rewrite.

- **Candidates:** Coop, Willys, Hemköp, Mat.se. Each needs its own spike first (like Phase 0 for ICA): is there a usable recipe source, a way to log in, and a list or cart to write to.
- **Replace or combine:** a store can fully replace ICA (recipes and shopping from Coop, say) or be mixed, for example ICA recipes with a Willys shopping list.
- **Per provider:** its own auth and re-auth flow, config step, translations, parsing into the neutral `Recipe` and `Ingredient` models, and capability flags (cart, list, product matching, offers, prices).
- **Done when:** a second provider passes the same contract tests as ICA with no change to the planner, entities, services or cards.

## Later ideas
- Rating-based learning beyond favorites: for example, noticing which ingredients or styles score well across ratings and nudging the style tags.
- Budget tracking over time: weekly spend history based on actual purchases, and trends. (v1 already includes budget-aware planning with estimated costs.)
- Nutrition summary per day and week.
- Additional languages.
- Voice announcements and Assist intents ("what's for dinner?").
