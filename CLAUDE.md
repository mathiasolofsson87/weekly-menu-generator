# Weekly Menu: project notes for Claude

HACS Home Assistant integration that suggests a weekly dinner menu. Read `PLAN.md` (design and decisions) and `ROADMAP.md` (later versions) before doing anything.


## Dev notes

- Tests need Python 3.13 and `pytest-homeassistant-custom-component`; the system Python is 3.9. Create a venv with `uv venv --python 3.13 .venv && uv pip install --python .venv/bin/python pytest-homeassistant-custom-component ruff`, then run `.venv/bin/python -m pytest` and `.venv/bin/ruff check custom_components tests`.
- Phase 1 is done: scaffold, config flow, options flow (general, schedule, family members) and the weekly scheduler, which fires the `weeklymenu_generation_due` event. The generator that listens for it is phase 2.
- `manifest.json` has `OWNER` placeholders in the GitHub URLs until the repo exists. There is no README yet (phase 7).
