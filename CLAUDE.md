# Weekly Menu: project notes for Claude

HACS Home Assistant integration that suggests a weekly dinner menu. Read `PLAN.md` (design and decisions) and `ROADMAP.md` (later versions) before doing anything.


## Dev notes

- Tests need Python 3.13 and `pytest-homeassistant-custom-component`; the system Python is 3.9. Create a venv with `uv venv --python 3.13 .venv && uv pip install --python .venv/bin/python pytest-homeassistant-custom-component ruff`, then run `.venv/bin/python -m pytest` and `.venv/bin/ruff check custom_components tests`.
- Phase 1 and 2a are done (see `PLAN.md`). The scheduler fires `weeklymenu_generation_due`, the coordinator listens and generates a draft menu from the source registry. Next is 2b: the ICA recipe source.
- Provider rule: only `sources/registry.py` may import a concrete source, and nothing outside an ICA module may mention ICA. The tests include a fake second provider and a shared contract (`tests/test_sources.py`); keep both passing.
- The allergen filter in `planner/allergens.py` is safety-critical: any change needs a test case in `tests/test_constraints.py`.
- Test extras: the AI Task schema test needs `hassil==3.5.0` and `home-assistant-intents==2026.1.28` (the versions pinned by HA's `conversation` manifest).
- The GitHub repo is `mathiasolofsson87/weekly-menu-generator` (private until release). The integration is called "Weekly Menu Generator" but the domain and folder stay `weeklymenu`. There is no README yet (phase 7).
