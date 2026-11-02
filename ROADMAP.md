# Roadmap

Ideas after the v1 release described in `PLAN.md`.

## Next: Favorites and ratings
Let the family tell the planner what they liked, and let the planner listen.

- **Favorite a recipe:** a star on the Menu and Today cards (and a service, `favorite_recipe`) marks a recipe as a favorite. Favorites are stored with the full recipe, so they can come back even when the source (ICA, AI Task) would not offer them again.
- **Rate a recipe:** 1 to 5 stars, set from the cards (for example on today's dinner after it has been cooked) or through a service (`rate_recipe`). A short "How was it?" prompt after a dinner day, as a notification action, is optional.
- **Whose rating:** start with one household rating per recipe. Later, a rating per family member (linked to the Home Assistant person already on the family card), combined by who eats on the day, so a recipe one person dislikes counts less on days they are home. This sits well with the voting idea in v2.
- **Planner weighting (extends `planner/scoring.py`):**
  - A favorite gets a bonus, and a high rating adds to it. A low rating is a penalty, and a very low rating (1 star) keeps the recipe out unless nothing else fits.
  - Favorites are not served every week: a cool-down (say 3 to 4 weeks) stops the same ones from dominating, and the existing repeat penalty still applies.
  - Unrated recipes are neutral, so new recipes still get a fair chance. A small "explore" share keeps the menu from only repeating known dishes.
  - The hard rules do not change: allergies and diets are checked first, so a favorite is never suggested to someone who cannot eat it, and a favorite that only fits through a split dinner still counts against the split limit.
  - Ratings feed the next week's menu and also "new dinner" for a single day.
- **Favorites as a candidate source:** a source that offers rated and favorite recipes from the local store, ahead of the other sources, so the planner can mix known good dinners with new ones. Like every source it is untrusted until the planner has run its checks.
- **Entities and cards:** a favorites list (sensor attributes or a card section) and the rating shown on the recipe in the Menu card. The Menu card's alternatives list shows stars so a choice is informed.
- **Data:** a store of recipe id, favorite flag, rating(s), last cooked date and times cooked. History comes from confirmed menus, which the store already keeps. Ratings survive a restart and are included in any later backup or export.
- **Open questions:** one rating or one per person; whether a rating can be changed later (yes); how long before a favorite comes back; whether to drop low-rated recipes from the cache of known recipes.

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
