# Roadmap

Ideas after the v1 release described in `PLAN.md`.

## Next: Favorites and ratings
Let each family member tell the planner what they liked, and let the planner listen.

- **Per member:** every family member has their own ratings and their own favorites. There is no single household rating. A member is linked to a Home Assistant person (already on the family card), which lets someone rate from their own dashboard or notification.
- **Favorite a recipe:** a star on the Menu and Today cards (and a `favorite_recipe` service with a member) marks a recipe as that member's favorite. Favorites are stored with the full recipe, so they can come back even when the source (ICA, AI Task) would not offer them again. A recipe can be a favorite of several members, and the cards show whose.
- **Rate a recipe:** 1 to 5 stars per member, from the cards (for example on today's dinner after it has been cooked) or through a `rate_recipe` service. An optional "How was it?" notification after a dinner asks each person who ate it. A rating can be changed later.
- **Who is asked:** the card and the notification only show a member their own stars. Setting a rating for someone else is allowed from the card (a parent rating for a small child), since not everyone has a login.
- **Planner weighting (extends `planner/scoring.py`):** the score for a day is built from the people who eat that day, using the family's attendance and portion setup that already exists.
  - A favorite adds a bonus for each attendee who has it as a favorite. A rating adds or subtracts for each attendee: high ratings add, low ratings subtract. The result is averaged over the attendees, so a dinner is not decided by one person.
  - A 1-star rating from someone who eats that day is a strong penalty, and the recipe is left out if anything else fits. Ratings from people who are not eating that day do not count that day.
  - A child's rating has half the weight of an adult's. A member gets an adult/child setting for this (a new field on the family card and in the options, set by hand and never guessed from the portion size).
  - A favorite is never served in two weeks in a row: after it has been on a menu, it is kept out of the following calendar week, so the earliest return is two weeks later (at least 14 days for the same weekday). The gap is a setting (default 1 week skipped, up to 4), and the existing repeat penalty still applies. When different people have different favorites, the planner spreads them over the week so everyone gets one now and then.
  - Unrated recipes are neutral, so new recipes still get a fair chance. A small "explore" share keeps the menu from only repeating known dishes.
  - The hard rules do not change: allergies and diets are checked first, so a favorite is never suggested to someone who cannot eat it, and a favorite that only fits through a split dinner still counts against the split limit.
  - Ratings feed next week's menu and also "new dinner" for a single day.
- **Favorites as a candidate source:** a source that offers favorite and well-rated recipes from the local store, ahead of the other sources, so the planner can mix known good dinners with new ones. Like every source it is untrusted until the planner has run its checks.
- **A member's own favorites list:** in the Family card, each member has a fold-out list of their favorited recipes (title, picture, their rating), under their name and also inside their edit form. Each row has a button to remove the favorite and a link to open the recipe. Removing a favorite only takes it off that member's list: the recipe, other members' favorites and the ratings all stay. The list works through the same `favorite_recipe` service (with a remove option), so the card needs no separate storage. If the recipe's source has gone, the stored copy still shows.
- **Entities and cards:** each member's favorites and the family's ratings per recipe appear on the family sensor and in a card section. The Menu card shows who likes a recipe, and its alternatives list shows the attendees' ratings so a choice is informed.
- **Data:** a store of recipe id, member id, favorite flag and rating, plus last cooked date and times cooked per recipe. History comes from confirmed menus, which the store already keeps. When a member is removed, their ratings and favorites go with them. Ratings survive a restart.
- **Related:** this feeds the v2 voting idea, where a member's rating can be the starting point for their vote.
- **Combining ratings for a day (decided):** a weighted average over the people eating, where an adult counts 1 and a child 0.5, and a dislike counts 1.5 times as much as a like of the same size. A 1-star rating from anyone eating that day is close to a veto (the recipe is left out if anything else fits).
- **Open questions:** whether to drop low-rated recipes from the cache of known recipes.

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
