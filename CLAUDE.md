# Weekly Menu: project notes for Claude

HACS Home Assistant integration that suggests a weekly dinner menu. Read `PLAN.md` (design and decisions) and `ROADMAP.md` (later versions) before doing anything.


## Dev notes

- Frontend: `cd frontend && npm install && npm test` (vitest), `npm run build` writes `custom_components/weeklymenu/www/weeklymenu-cards.js`. **Commit the rebuilt bundle** with any change in `frontend/src` (a Python test checks that it exists). To look at the cards, serve the bundle with a page that defines stand-ins for `ha-card` and `ha-icon` and screenshot it with Chrome headless; headless Chrome has a minimum window width, so constrain the cards' column width in the page instead of the window.

- Tests need Python 3.13 and `pytest-homeassistant-custom-component`; the system Python is 3.9. Create a venv with `uv venv --python 3.13 .venv && uv pip install --python .venv/bin/python pytest-homeassistant-custom-component ruff`, then run `.venv/bin/python -m pytest` and `.venv/bin/ruff check custom_components tests`.
- Phases 0, 1 and 2 are done (see `PLAN.md`). The scheduler fires `weeklymenu_generation_due`, the coordinator listens and generates a draft menu from the source registry (ICA recipes, then AI Task). Phase 3 (menu editing, confirm, notifications) is done too. Phases 4 and 5 are done (shopping on confirm, ICA list provider, re-auth). The ICA row formats were verified against the real app with `spikes/ica_rows_spike.py` (see `PLAN.md`, Phase 5). Phase 6 is half done: the Menu and Today cards are built (`frontend/`), the Shopping result and Family cards are not. Next: those two, then phase 7 (CI, README, release).
- Tests never touch the network: ICA is mocked with `aioclient_mock` and fixtures in `tests/fixtures/` saved from real ica.se pages. To check the parsers against the live site, fetch a few pages with the `User-Agent` from `sources/ica/source.py`, one per second.
- All menu changes go through `WeeklyMenuCoordinator` (one lock); services, buttons and notification actions only call it. Shared test fixtures are in `tests/conftest.py`, helpers in `tests/helpers.py`.
- Provider rule: only `sources/registry.py` and `shopping/registry.py` may import a concrete provider, and nothing outside an ICA package may mention ICA. Account forms and re-auth are generic (`ProviderSetup`). The tests include a fake second provider and a shared contract (`tests/test_sources.py`); keep both passing.
- The allergen filter in `planner/allergens.py` is safety-critical: any change needs a test case in `tests/test_constraints.py`.
- Test extras: the AI Task schema test needs `hassil==3.5.0` and `home-assistant-intents==2026.1.28` (the versions pinned by HA's `conversation` manifest).
- The GitHub repo is `mathiasolofsson87/weekly-menu-generator` (private until release). The integration is called "Weekly Menu Generator" but the domain and folder stay `weeklymenu`. There is no README yet (phase 7).
