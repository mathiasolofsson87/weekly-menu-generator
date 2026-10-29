# Roadmap

Ideas after the v1 release described in `PLAN.md`.

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

## Later ideas
- Recipe ratings and history feeding back into the planner.
- Budget tracking over time: weekly spend history based on actual purchases, and trends. (v1 already includes budget-aware planning with estimated costs.)
- Nutrition summary per day and week.
- Additional shopping providers (Willys, Coop, Mat.se).
- Additional languages.
- Voice announcements and Assist intents ("what's for dinner?").
