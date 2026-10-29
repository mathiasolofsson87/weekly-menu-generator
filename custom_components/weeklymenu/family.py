"""Editing the family from services (and so from the dashboard card).

The family lives in the config entry's options, exactly as the options flow stores it, so
both ways of editing agree. Saving reloads the entry, which is how the planner picks the
change up for the next menu. Menus that already exist are not touched.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError

from .const import (
    CONF_MEMBERS,
    DOMAIN,
    MEMBER_ALLERGIES,
    MEMBER_ATTENDS,
    MEMBER_COOK_SEPARATELY,
    MEMBER_DIET,
    MEMBER_DISLIKES,
    MEMBER_ID,
    MEMBER_LIKES,
    MEMBER_NAME,
    MEMBER_PERSON,
    MEMBER_PORTION,
)
from .planner.models import FamilyMember, dinner_days_from_options

# The fields a service call may change; anything it leaves out keeps its value.
EDITABLE = (
    MEMBER_PERSON,
    MEMBER_ALLERGIES,
    MEMBER_DISLIKES,
    MEMBER_LIKES,
    MEMBER_DIET,
    MEMBER_PORTION,
    MEMBER_ATTENDS,
    MEMBER_COOK_SEPARATELY,
)


def _error(key: str, **placeholders: str) -> ServiceValidationError:
    return ServiceValidationError(
        translation_domain=DOMAIN,
        translation_key=key,
        translation_placeholders=placeholders or None,
    )


def _save(
    hass: HomeAssistant, entry: ConfigEntry, members: list[dict[str, Any]]
) -> None:
    hass.config_entries.async_update_entry(
        entry, options={**entry.options, CONF_MEMBERS: members}
    )


def async_set_member(
    hass: HomeAssistant, entry: ConfigEntry, data: Mapping[str, Any]
) -> dict[str, str]:
    """Add a member, or change one. A member is found by `id`, else by name (any case).
    Returns the member's id and name."""
    members: list[dict[str, Any]] = list(entry.options.get(CONF_MEMBERS, []))
    name = str(data.get(MEMBER_NAME) or "").strip()
    member_id = data.get(MEMBER_ID)

    if member_id:
        current = next((m for m in members if m[MEMBER_ID] == member_id), None)
        if current is None:
            raise _error("member_not_found", member=str(member_id))
    else:
        current = next(
            (m for m in members if m[MEMBER_NAME].casefold() == name.casefold()), None
        )
    if current is not None and (not name or not member_id):
        name = current[MEMBER_NAME]  # found by name: keep how it is written
    if not name:
        raise _error("member_name_required")
    if any(
        m[MEMBER_NAME].casefold() == name.casefold() and m is not current
        for m in members
    ):
        raise _error("member_name_exists", name=name)

    fields = {key: data[key] for key in EDITABLE if key in data}
    if current is None:
        fields.setdefault(MEMBER_ATTENDS, dinner_days_from_options(entry.options))
        base: dict[str, Any] = {}
    else:
        base = current
    member = FamilyMember.from_dict(
        {**base, **fields, MEMBER_NAME: name, MEMBER_ID: base.get(MEMBER_ID)}
    )
    if not member.attends:
        raise _error("member_no_days", name=name)

    stored = member.as_dict()
    _save(
        hass,
        entry,
        [stored if m is current else m for m in members]
        if current is not None
        else [*members, stored],
    )
    return {MEMBER_ID: member.id, MEMBER_NAME: member.name}


def async_remove_member(
    hass: HomeAssistant, entry: ConfigEntry, data: Mapping[str, Any]
) -> None:
    """Remove a member by `id` or by name."""
    members: list[dict[str, Any]] = list(entry.options.get(CONF_MEMBERS, []))
    member_id, name = data.get(MEMBER_ID), str(data.get(MEMBER_NAME) or "").strip()
    found = next(
        (
            m
            for m in members
            if (member_id and m[MEMBER_ID] == member_id)
            or (not member_id and name and m[MEMBER_NAME].casefold() == name.casefold())
        ),
        None,
    )
    if found is None:
        raise _error("member_not_found", member=str(member_id or name))
    _save(hass, entry, [m for m in members if m is not found])
