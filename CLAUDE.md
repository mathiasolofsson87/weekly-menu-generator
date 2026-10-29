# Weekly Menu: project notes for Claude

HACS Home Assistant integration that suggests a weekly dinner menu. Read `PLAN.md` (design and decisions) and `ROADMAP.md` (later versions) before doing anything.


## Dev notes

- Frontend: `cd frontend && npm install && npm test` (vitest), `npm run build` writes `custom_components/weeklymenu/www/weeklymenu-cards.js`. **Commit the rebuilt bundle** with any change in `frontend/src` (a Python test checks that it exists). To look at the cards, serve the bundle with a page that defines stand-ins for `ha-card` and `ha-icon` and screenshot it with Chrome headless; headless Chrome has a minimum window width, so constrain the cards' column width in the page instead of the window.

- Tests need Python 3.13 and `pytest-homeassistant-custom-component`; the system Python is 3.9. Create a venv with `uv venv --python 3.13 .venv && uv pip install --python .venv/bin/python pytest-homeassistant-custom-component ruff`, then run `.venv/bin/python -m pytest` and `.venv/bin/ruff check custom_components tests`.
- Phases 0, 1 and 2 are done (see `PLAN.md`). The scheduler fires `weeklymenu_generation_due`, the coordinator listens and generates a draft menu from the source registry (ICA recipes, then AI Task). Phase 3 (menu editing, confirm, notifications) is done too. Phases 4 and 5 are done (shopping on confirm, ICA list provider, re-auth). The ICA row formats were verified against the real app with `spikes/ica_rows_spike.py` (see `PLAN.md`, Phase 5). Phase 6 is done (four cards, `frontend/`), and phase 7 is done except the release (CI, README, translation checks; see `PLAN.md`, "Before a release" and "Left over from the v1 plan"). **Release only when the user says "release"** (see the Release section below). Do not open a HACS default-list pull request unless the user asks. The next useful step is the user running it in a real Home Assistant and reporting what breaks.
- Tests never touch the network: ICA is mocked with `aioclient_mock` and fixtures in `tests/fixtures/` saved from real ica.se pages. To check the parsers against the live site, fetch a few pages with the `User-Agent` from `sources/ica/source.py`, one per second.
- All menu changes go through `WeeklyMenuCoordinator` (one lock); services, buttons and notification actions only call it. Shared test fixtures are in `tests/conftest.py`, helpers in `tests/helpers.py`.
- Provider rule: only `sources/registry.py` and `shopping/registry.py` may import a concrete provider, and nothing outside an ICA package may mention ICA. Account forms and re-auth are generic (`ProviderSetup`). The tests include a fake second provider and a shared contract (`tests/test_sources.py`); keep both passing.
- The allergen filter in `planner/allergens.py` is safety-critical: any change needs a test case in `tests/test_constraints.py`.
- The GitHub repo is `mathiasolofsson87/weekly-menu-generator` (public). The integration is called "Weekly Menu Generator" but the domain and folder stay `weeklymenu`.
- **Never put real personal data in the repository, tests included**: no real personnummer, password, token, name or address, even if the user pasted it into the chat while debugging. Use invented values (the tests use 900101-1234). The repository is meant to become public.
- Licence: MIT (`LICENSE`), with third-party notices in `NOTICE.md`. If you add code ported from another project, or a bundled dependency, add its notice there.


## Release

When the user says "release":

1. Make sure the working tree is clean and on `main`, and that `main` is up to date with `origin`.
2. Run the checks: `.venv/bin/python -m pytest`, `.venv/bin/ruff check .`, `.venv/bin/ruff format --check .`, and in `frontend/`: `npm test`, `npm run typecheck`, `npm run build`. The rebuilt `custom_components/weeklymenu/www/weeklymenu-cards.js` must have no diff (otherwise commit it first). Stop and report if anything fails.
3. Pick the version from the commits since the last tag: patch for fixes, minor for features (while on 0.x, breaking changes are also minor). Bump `version` in `custom_components/weeklymenu/manifest.json`.
4. Add a section to `CHANGELOG.md` (newest first, `## X.Y.Z – YYYY-MM-DD`, with Added / Changed / Fixed lists, written for users).
5. Commit ("Release vX.Y.Z", with the usual trailer), push, create the tag `vX.Y.Z`, push the tag, and create a GitHub release with the same notes (`gh release create`) so HACS picks it up.
6. Check that the CI and Validate runs on the release commit pass and report the result and the release link.

Ask before pushing if the user said "don't push yet". Never include real personal data in the changelog or release notes.
