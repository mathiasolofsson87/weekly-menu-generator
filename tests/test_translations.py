"""The translations are complete, in step, and cover everything the code refers to."""

import json
import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent / "custom_components" / "weeklymenu"
LANGUAGES = ["en", "sv"]


def load(language: str) -> dict:
    return json.loads(
        (ROOT / "translations" / f"{language}.json").read_text(encoding="utf-8")
    )


def keys(node, prefix=""):
    """Every dotted path to a leaf."""
    if isinstance(node, dict):
        for key, value in node.items():
            yield from keys(value, f"{prefix}{key}.")
    else:
        yield prefix.rstrip(".")


def source(*names: str) -> str:
    return "\n".join((ROOT / name).read_text(encoding="utf-8") for name in names)


def placeholders(text: str) -> set[str]:
    return set(re.findall(r"\{(\w+)\}", text))


def leaves(node, prefix=""):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from leaves(value, f"{prefix}{key}.")
    else:
        yield prefix.rstrip("."), node


def test_swedish_and_english_have_the_same_keys() -> None:
    en, sv = set(keys(load("en"))), set(keys(load("sv")))
    assert sorted(en - sv) == [] and sorted(sv - en) == []


def test_no_translation_is_empty_and_placeholders_match() -> None:
    en = dict(leaves(load("en")))
    for key, swedish in leaves(load("sv")):
        assert str(swedish).strip(), key
        assert str(en[key]).strip(), key
        assert placeholders(str(swedish)) == placeholders(str(en[key])), key


@pytest.mark.parametrize("language", LANGUAGES)
def test_every_service_is_described(language: str) -> None:
    services = yaml.safe_load((ROOT / "services.yaml").read_text(encoding="utf-8"))
    translated = load(language)["services"]
    assert set(services) == set(translated)
    for name, definition in services.items():
        described = translated[name]
        assert described["name"] and described["description"], name
        assert set(definition.get("fields", {})) == set(described.get("fields", {})), (
            name
        )


@pytest.mark.parametrize("language", LANGUAGES)
def test_every_error_the_code_raises_has_a_message(language: str) -> None:
    code = source("coordinator.py", "family.py", "services.py")
    used = set(re.findall(r'translation_key=\s*"(\w+)"', code)) | set(
        re.findall(r'_error\(\s*"(\w+)"', code)
    )
    assert used, "found no translated errors"
    assert used <= set(load(language)["exceptions"]), used - set(
        load(language)["exceptions"]
    )


@pytest.mark.parametrize("language", LANGUAGES)
def test_every_entity_has_a_name(language: str) -> None:
    code = source("sensor.py", "button.py", "calendar.py")
    used = set(
        re.findall(
            r'(?:super\(\).__init__\(coordinator, |_attr_translation_key = )"(\w+)"',
            code,
        )
    )
    used |= {f"weekday_{d}" for d in ("mon", "tue", "wed", "thu", "fri", "sat", "sun")}
    named = {k for group in load(language)["entity"].values() for k in group}
    assert used <= named, used - named


@pytest.mark.parametrize("language", LANGUAGES)
def test_every_dropdown_has_labels(language: str) -> None:
    """Each translation_key given to a selector needs its options translated."""
    code = source("config_flow.py", "shopping/ica/setup.py")
    used = set(re.findall(r'_select\([^)]*?"(\w+)"(?:,\s*multiple=\w+)?\)', code))
    used |= {"allergen", "ica_list_mode"}
    labels = load(language)["selector"]
    assert used <= set(labels), used - set(labels)
    assert {
        "weekday",
        "diet",
        "portion",
        "language",
        "units",
        "style",
        "source",
        "provider",
    } <= set(labels)


@pytest.mark.parametrize("language", LANGUAGES)
def test_every_options_step_and_menu_entry_is_translated(language: str) -> None:
    code = source("config_flow.py")
    steps = set(re.findall(r"async def async_step_(\w+)", code))
    translated = load(language)["options"]["step"]
    for step in steps - {
        "user",
        "reauth",
        "reauth_confirm",
        "member_add",
        "finish",
        "init",
    }:
        assert step in translated, step
    menus = translated["init"]["menu_options"]
    for entry in (
        "general",
        "schedule",
        "family",
        "styles",
        "sources",
        "shopping",
        "accounts",
        "notifications",
        "finish",
    ):
        assert entry in menus, entry
    assert {"member_add", "member_edit", "member_remove", "init"} <= set(
        translated["family"]["menu_options"]
    )


@pytest.mark.parametrize("language", LANGUAGES)
def test_every_form_error_is_translated(language: str) -> None:
    code = source("config_flow.py", "shopping/ica/setup.py")
    used = set(re.findall(r'errors\[[\w.]+\] = "(\w+)"', code)) | set(
        re.findall(r'\{[^{}]*?: "(\w+)"\}, ', source("shopping/ica/setup.py"))
    )
    used |= {"no_days", "name_required", "name_exists"}
    translated = load(language)["options"]["error"]
    assert used <= set(translated), used - set(translated)


def test_manifest_keys_are_in_the_order_hassfest_requires() -> None:
    """hassfest: "domain, name, then alphabetical order"."""
    keys = list(json.loads((ROOT / "manifest.json").read_text(encoding="utf-8")))
    assert keys[:2] == ["domain", "name"]
    assert keys[2:] == sorted(keys[2:])
