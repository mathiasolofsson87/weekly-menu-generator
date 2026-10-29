# Changelog

All notable changes to Weekly Menu Generator. Versions match the git tags and the GitHub releases.

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
