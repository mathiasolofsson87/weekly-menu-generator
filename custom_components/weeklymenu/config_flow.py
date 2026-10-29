"""Config and options flow for Weekly Menu."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TimeSelector,
)

from .const import (
    ALLERGENS,
    CONF_AI_TASK,
    CONF_DINNER_DAYS,
    CONF_GENERATION_DAY,
    CONF_GENERATION_TIME,
    CONF_LANGUAGE,
    CONF_MEMBERS,
    CONF_SHOPPING_TARGETS,
    CONF_UNITS,
    DEFAULT_DINNER_DAYS,
    DEFAULT_GENERATION_DAY,
    DEFAULT_GENERATION_TIME,
    DEFAULT_LANGUAGE,
    DEFAULT_UNITS,
    DIETS,
    DOMAIN,
    LANGUAGES,
    MEMBER_ALLERGIES,
    MEMBER_ATTENDS,
    MEMBER_DIET,
    MEMBER_DISLIKES,
    MEMBER_ID,
    MEMBER_LIKES,
    MEMBER_NAME,
    MEMBER_PERSON,
    MEMBER_PORTION,
    PORTIONS,
    UNITS,
    WEEKDAYS,
)
from .planner.models import FamilyMember, dinner_days_from_options


def _select(options: list[str], key: str, *, multiple: bool = False) -> SelectSelector:
    """Dropdown whose labels come from the `selector.<key>` translations."""
    return SelectSelector(
        SelectSelectorConfig(
            options=options,
            multiple=multiple,
            translation_key=key,
            mode=SelectSelectorMode.DROPDOWN,
        )
    )


def _free_terms() -> SelectSelector:
    """Multi-select for free-text terms such as dislikes."""
    return SelectSelector(
        SelectSelectorConfig(options=[], multiple=True, custom_value=True)
    )


def _general_schema() -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(CONF_LANGUAGE, default=DEFAULT_LANGUAGE): _select(
                LANGUAGES, "language"
            ),
            vol.Required(CONF_UNITS, default=DEFAULT_UNITS): _select(UNITS, "units"),
            vol.Optional(CONF_SHOPPING_TARGETS): EntitySelector(
                EntitySelectorConfig(domain="todo", multiple=True)
            ),
            vol.Optional(CONF_AI_TASK): EntitySelector(
                EntitySelectorConfig(domain="ai_task")
            ),
        }
    )


SCHEDULE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_GENERATION_DAY): _select(WEEKDAYS, "weekday"),
        vol.Required(CONF_GENERATION_TIME): TimeSelector(),
        vol.Required(CONF_DINNER_DAYS): _select(WEEKDAYS, "weekday", multiple=True),
    }
)

MEMBER_SCHEMA = vol.Schema(
    {
        vol.Required(MEMBER_NAME): TextSelector(),
        vol.Optional(MEMBER_PERSON): EntitySelector(
            EntitySelectorConfig(domain="person")
        ),
        vol.Optional(MEMBER_ALLERGIES): SelectSelector(
            SelectSelectorConfig(
                options=ALLERGENS,
                multiple=True,
                custom_value=True,
                translation_key="allergen",
                mode=SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Optional(MEMBER_DISLIKES): _free_terms(),
        vol.Optional(MEMBER_LIKES): _free_terms(),
        vol.Required(MEMBER_DIET): _select(DIETS, "diet"),
        vol.Required(MEMBER_PORTION): _select(PORTIONS, "portion"),
        vol.Required(MEMBER_ATTENDS): _select(WEEKDAYS, "weekday", multiple=True),
    }
)


class WeeklyMenuConfigFlow(ConfigFlow, domain=DOMAIN):
    """Initial setup. Everything else lives in the options flow."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> WeeklyMenuOptionsFlow:
        """Return the options flow."""
        return WeeklyMenuOptionsFlow()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Ask for the general settings."""
        if user_input is not None:
            return self.async_create_entry(title="Weekly Menu", data=user_input)

        suggested = {
            CONF_LANGUAGE: self.hass.config.language
            if self.hass.config.language in LANGUAGES
            else DEFAULT_LANGUAGE
        }
        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                _general_schema(), suggested
            ),
        )


class WeeklyMenuOptionsFlow(OptionsFlow):
    """Edit settings. Each form saves immediately, so closing the dialog loses nothing."""

    def __init__(self) -> None:
        self._options: dict[str, Any] | None = None
        self._editing_id: str | None = None

    def _current(self) -> dict[str, Any]:
        if self._options is None:
            self._options = dict(self.config_entry.options)
        return self._options

    def _save(self, **changes: Any) -> None:
        # Always hand HA a new dict; mutating the stored one would hide the change.
        self._options = {**self._current(), **changes}
        self.hass.config_entries.async_update_entry(
            self.config_entry, options=self._options
        )

    def _config(self) -> dict[str, Any]:
        return {**self.config_entry.data, **self._current()}

    def _members(self) -> list[dict[str, Any]]:
        return list(self._current().get(CONF_MEMBERS, []))

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Top-level menu."""
        return self.async_show_menu(
            step_id="init", menu_options=["general", "schedule", "family", "finish"]
        )

    async def async_step_finish(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Close the dialog."""
        return self.async_create_entry(title="", data=self._current())

    async def async_step_general(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Language, units, shopping targets and AI Task entity."""
        if user_input is not None:
            # Write every key, so a cleared field overrides the value from setup.
            self._save(
                **{
                    CONF_LANGUAGE: user_input[CONF_LANGUAGE],
                    CONF_UNITS: user_input[CONF_UNITS],
                    CONF_SHOPPING_TARGETS: user_input.get(CONF_SHOPPING_TARGETS, []),
                    CONF_AI_TASK: user_input.get(CONF_AI_TASK),
                }
            )
            return await self.async_step_init()
        return self.async_show_form(
            step_id="general",
            data_schema=self.add_suggested_values_to_schema(
                _general_schema(), self._config()
            ),
        )

    async def async_step_schedule(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Generation day and time, and which weekdays get a dinner."""
        errors: dict[str, str] = {}
        if user_input is not None:
            if not user_input[CONF_DINNER_DAYS]:
                errors[CONF_DINNER_DAYS] = "no_days"
            else:
                self._save(**user_input)
                return await self.async_step_init()
            current = user_input
        else:
            config = self._config()
            current = {
                CONF_GENERATION_DAY: config.get(
                    CONF_GENERATION_DAY, DEFAULT_GENERATION_DAY
                ),
                CONF_GENERATION_TIME: config.get(
                    CONF_GENERATION_TIME, DEFAULT_GENERATION_TIME
                ),
                CONF_DINNER_DAYS: dinner_days_from_options(config),
            }
        return self.async_show_form(
            step_id="schedule",
            data_schema=self.add_suggested_values_to_schema(SCHEDULE_SCHEMA, current),
            errors=errors,
        )

    async def async_step_family(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Family member menu."""
        menu = ["member_add"]
        if self._members():
            menu += ["member_edit", "member_remove"]
        menu.append("init")
        return self.async_show_menu(step_id="family", menu_options=menu)

    def _pick_member_schema(self) -> vol.Schema:
        options = [
            SelectOptionDict(value=m[MEMBER_ID], label=m[MEMBER_NAME])
            for m in self._members()
        ]
        return vol.Schema(
            {
                vol.Required(MEMBER_ID): SelectSelector(
                    SelectSelectorConfig(options=options)
                )
            }
        )

    async def async_step_member_add(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Start adding a member."""
        self._editing_id = None
        return await self.async_step_member_form()

    async def async_step_member_edit(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Choose a member to edit."""
        if user_input is not None:
            self._editing_id = user_input[MEMBER_ID]
            return await self.async_step_member_form()
        return self.async_show_form(
            step_id="member_edit", data_schema=self._pick_member_schema()
        )

    async def async_step_member_remove(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Choose a member to remove."""
        if user_input is not None:
            self._save(
                **{
                    CONF_MEMBERS: [
                        m
                        for m in self._members()
                        if m[MEMBER_ID] != user_input[MEMBER_ID]
                    ]
                }
            )
            return await self.async_step_family()
        return self.async_show_form(
            step_id="member_remove", data_schema=self._pick_member_schema()
        )

    async def async_step_member_form(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Add or edit one member (`_editing_id` says which)."""
        members = self._members()
        errors: dict[str, str] = {}

        if user_input is not None:
            name = user_input[MEMBER_NAME].strip()
            if not name:
                errors[MEMBER_NAME] = "name_required"
            elif any(
                m[MEMBER_NAME].casefold() == name.casefold()
                and m[MEMBER_ID] != self._editing_id
                for m in members
            ):
                errors[MEMBER_NAME] = "name_exists"
            if not user_input[MEMBER_ATTENDS]:
                errors[MEMBER_ATTENDS] = "no_days"

            if not errors:
                member = FamilyMember.from_dict(
                    {**user_input, MEMBER_NAME: name, MEMBER_ID: self._editing_id}
                ).as_dict()
                if self._editing_id:
                    members = [
                        member if m[MEMBER_ID] == self._editing_id else m
                        for m in members
                    ]
                else:
                    members.append(member)
                self._editing_id = None
                self._save(**{CONF_MEMBERS: members})
                return await self.async_step_family()
            current: dict[str, Any] = user_input
        elif self._editing_id:
            current = next(m for m in members if m[MEMBER_ID] == self._editing_id)
        else:
            current = {
                MEMBER_DIET: "omnivore",
                MEMBER_PORTION: "normal",
                MEMBER_ATTENDS: dinner_days_from_options(self._config())
                or list(DEFAULT_DINNER_DAYS),
            }

        return self.async_show_form(
            step_id="member_form",
            data_schema=self.add_suggested_values_to_schema(MEMBER_SCHEMA, current),
            errors=errors,
        )
