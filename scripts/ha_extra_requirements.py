"""Prints the packages Home Assistant's `conversation` integration needs, one per line.

tests/test_sources.py checks the AI Task structure against Home Assistant's own validator,
which imports `homeassistant.components.ai_task` and so, through it, `conversation`. Those
pinned packages are not pulled in by the test package, and the versions must match the
installed Home Assistant, so they are read from its manifest instead of being listed here.
The package is located without importing it, because importing it needs these very packages.
"""

import importlib.util
import json
from pathlib import Path

spec = importlib.util.find_spec("homeassistant.components.conversation")
assert spec and spec.submodule_search_locations, "Home Assistant is not installed"
manifest = json.loads(
    (Path(next(iter(spec.submodule_search_locations))) / "manifest.json").read_text()
)
print("\n".join(manifest["requirements"]))
