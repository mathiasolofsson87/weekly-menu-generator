# Changelog

All notable changes to Weekly Menu Generator. Versions match the git tags and the GitHub releases.

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
