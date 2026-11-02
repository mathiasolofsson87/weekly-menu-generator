# Changelog

All notable changes to Weekly Menu Generator. Versions match the git tags and the GitHub releases.

## 0.3.0 – 2026-11-02

### Added
- **Ratings and favorites, per family member.** Give a dinner 1 to 5 stars and a heart from the Menu card (in an opened day, also after the menu is confirmed) and the Tonight's dinner card. You act as the family member linked to your Home Assistant person, or pick who you rate as, for example a child. The services `rate_recipe` and `favorite_recipe` do the same.
- **The planner uses them.** Only the people eating a day count for that day. A child's rating counts half of an adult's, a dislike weighs more than a like, and a 1-star rating from anyone eating keeps the recipe out unless nothing else fits. Favorites get a bonus in proportion to how much of the table has them as a favorite. Allergies and diets are still checked first.
- **Favorites and well-rated recipes come back.** They are kept in a local store and offered again, at most a third of the candidates, mixed with new recipes. A favorite is never served in two weeks in a row; the gap is a new setting under *Meal styles* (1 to 4 weeks, default 1).
- **Favorites list in the Family card.** Each member has a fold-out list of their favorites, under their name and in their edit form, with a link to each recipe, their rating and a button to remove it.
- **Child setting.** Mark a member as a child (options, the Family card, or `set_member`). A child, when logged in as the linked Home Assistant user, can rate and favorite but cannot generate, change, lock, swap or confirm the menu, add to the shopping list or edit the family. The cards hide those controls and the services refuse them. Users not linked to a member, automations, the schedule and the notification buttons are not restricted.
- The README explains how recipes are chosen: favorites, then ICA recipes, then AI Task if one is set up, with the same safety checks for every source.

### Changed
- Removing a family member now also removes their ratings and favorites.

## 0.2.0 – 2026-10-29

### Added
- The family card can link a person to a Home Assistant person. A dropdown lists the people in Home Assistant and fills in the name, and the person's profile picture shows next to their name (a round badge with the initial when there is no picture).
- Wishes now work with every recipe source. Typing "not fish", "inte fisk" or "utan skaldjur" when asking for a new dinner rules those dishes out, and "gärna pasta" ranks matching dishes higher. Before, only the AI Task source read the wish.

### Changed
- "New dinner" for a day remembers everything that day has already offered, so it no longer cycles through the same few dishes. Dishes that score the same now take turns at random, and a bigger pool is read when one day is replaced.
- Vegetarian and fish days are now filled earlier in the week.

### Fixed
- Fresh herbs and vegetables with "färsk" in the name (färsk timjan, färsk oregano and so on) were treated as minced meat, so recipes with them were blocked for vegetarians.

## 0.1.0 – 2026-10-29

First public version.

### Added
- Suggests a weekly dinner menu from ICA recipes (and Home Assistant AI Task as a fallback), with variety, style and like/dislike scoring.
- Per-person allergies and diets as hard rules, checked in Swedish and English. When someone needs a different version of a dinner, it can be cooked in separate pans with a substitute (limit per week is configurable).
- Edit the menu: regenerate or swap days, lock a day, pick another recipe, and confirm the week.
- Shopping on confirm: ingredients are scaled to who eats, merged, and added to Home Assistant to-do lists and the ICA shopping list. Pantry staples are skipped, and failed items can be retried.
- Notifications with actions, a calendar, sensors and buttons, and services for everything above.
- Four dashboard cards (menu, today, shopping, family) with visual editors, in Swedish and English.
- Providers are replaceable: recipe sources and shopping lists go through registries, so other stores can be added later.

### Notes
- Not yet tested in a real Home Assistant. Please report problems as issues.
- The allergen filter is a best-effort text check. Always read the recipe and the packaging.
