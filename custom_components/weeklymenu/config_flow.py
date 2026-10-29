"""Config and options flow for Weekly Menu."""

from __future__ import annotations

from collections.abc import Mapping
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
    BooleanSelector,
    EntitySelector,
    EntitySelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
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
    CONF_FISH_MIN,
    CONF_GENERATION_DAY,
    CONF_GENERATION_TIME,
    CONF_LANGUAGE,
    CONF_MAX_SPLIT_DAYS,
    CONF_MEMBERS,
    CONF_NOTIFY_EVENTS,
    CONF_NOTIFY_TARGETS,
    CONF_OPEN_PATH,
    CONF_PANTRY,
    CONF_REVIEW_LIST,
    CONF_SHOPPING_TARGETS,
    CONF_SOURCES,
    CONF_STYLE_TAGS,
    CONF_UNITS,
    CONF_VEGETARIAN_DAYS,
    DEFAULT_DINNER_DAYS,
    DEFAULT_FISH_MIN,
    DEFAULT_GENERATION_DAY,
    DEFAULT_GENERATION_TIME,
    DEFAULT_LANGUAGE,
    DEFAULT_MAX_SPLIT_DAYS,
    DEFAULT_OPEN_PATH,
    DEFAULT_UNITS,
    DEFAULT_VEGETARIAN_DAYS,
    DIETS,
    DOMAIN,
    LANGUAGES,
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
    NOTIFY_EVENTS,
    PORTIONS,
    STYLE_TAGS,
    UNITS,
    WEEKDAYS,
)
from .planner.models import FamilyMember, clean_terms, dinner_days_from_options
from .shopping.aggregate import DEFAULT_PANTRY
from .shopping.base import ProviderSetup


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


def _todo_lists() -> EntitySelector:
    return EntitySelector(EntitySelectorConfig(domain="todo", multiple=True))


def _general_schema(with_targets: bool = False) -> vol.Schema:
    """The settings asked at setup. Shopping lists are asked there too, and edited later
    on their own page."""
    fields: dict[Any, Any] = {
        vol.Required(CONF_LANGUAGE, default=DEFAULT_LANGUAGE): _select(
            LANGUAGES, "language"
        ),
        vol.Required(CONF_UNITS, default=DEFAULT_UNITS): _select(UNITS, "units"),
    }
    if with_targets:
        fields[vol.Optional(CONF_SHOPPING_TARGETS)] = _todo_lists()
    fields[vol.Optional(CONF_AI_TASK)] = EntitySelector(
        EntitySelectorConfig(domain="ai_task")
    )
    return vol.Schema(fields)


SHOPPING_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_SHOPPING_TARGETS): _todo_lists(),
        vol.Optional(CONF_REVIEW_LIST): EntitySelector(
            EntitySelectorConfig(domain="todo")
        ),
        vol.Optional(CONF_PANTRY): SelectSelector(
            SelectSelectorConfig(options=[], multiple=True, custom_value=True)
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


def _days_selector() -> NumberSelector:
    return NumberSelector(
        NumberSelectorConfig(min=0, max=7, step=1, mode=NumberSelectorMode.SLIDER)
    )


STYLES_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_STYLE_TAGS): _select(STYLE_TAGS, "style", multiple=True),
        vol.Required(CONF_VEGETARIAN_DAYS): _days_selector(),
        vol.Required(CONF_FISH_MIN): _days_selector(),
        vol.Required(CONF_MAX_SPLIT_DAYS): _days_selector(),
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
        vol.Required(MEMBER_COOK_SEPARATELY): BooleanSelector(),
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

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """A provider's login stopped working."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Ask again for what the provider needs, checked by the provider itself."""
        entry = self._get_reauth_entry()
        setups = self.hass.data[DOMAIN]["shopping_registry"].setups
        setup = setups.get(self.context.get("provider_id", ""))
        if setup is None:
            return self.async_abort(reason="no_account")
        config = dict(entry.data)
        errors: dict[str, str] = {}
        if user_input is not None:
            current = {key: config.get(key) for key in setup.keys}
            changes, errors = await setup.validate(
                self.hass, config, {**current, **user_input}
            )
            if not errors:
                return self.async_update_reload_and_abort(entry, data_updates=changes)
        fields = {
            marker: selector
            for marker, selector in setup.schema(config).schema.items()
            if marker.schema in setup.reauth_keys
        }
        shown = {
            k: v
            for k, v in config.items()
            if k in setup.reauth_keys and k not in setup.secret_keys
        }
        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=self.add_suggested_values_to_schema(vol.Schema(fields), shown),
            errors=errors,
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Ask for the general settings."""
        if user_input is not None:
            return self.async_create_entry(
                title="Weekly Menu Generator", data=user_input
            )

        suggested = {
            CONF_LANGUAGE: self.hass.config.language
            if self.hass.config.language in LANGUAGES
            else DEFAULT_LANGUAGE
        }
        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                _general_schema(with_targets=True), suggested
            ),
        )


class WeeklyMenuOptionsFlow(OptionsFlow):
    """Edit settings. Each form saves immediately, so closing the dialog loses nothing."""

    def __init__(self) -> None:
        self._options: dict[str, Any] | None = None
        self._editing_id: str | None = None
        self._account = ""

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
        menu = ["general", "schedule", "family", "styles", "sources", "shopping"]
        if self._setups():
            menu.append("accounts")
        return self.async_show_menu(
            step_id="init", menu_options=[*menu, "notifications", "finish"]
        )

    def _setups(self) -> dict[str, ProviderSetup]:
        return self.hass.data[DOMAIN]["shopping_registry"].setups

    async def async_step_accounts(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Pick the store account to set up (skipped when there is only one)."""
        setups = self._setups()
        if user_input is not None:
            self._account = user_input["provider"]
            return await self.async_step_account()
        if len(setups) == 1:
            self._account = next(iter(setups))
            return await self.async_step_account()
        schema = vol.Schema(
            {vol.Required("provider"): _select(list(setups), "provider")}
        )
        return self.async_show_form(step_id="accounts", data_schema=schema)

    async def async_step_account(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """One provider's account form, built and checked by the provider itself."""
        setup = self._setups()[self._account]
        config = self._config()
        errors: dict[str, str] = {}
        if user_input is not None:
            changes, errors = await setup.validate(self.hass, config, user_input)
            if not errors:
                data = {**self.config_entry.data}
                for key, value in changes.items():
                    if value is None:
                        data.pop(key, None)
                    else:
                        data[key] = value
                self.hass.config_entries.async_update_entry(
                    self.config_entry, data=data
                )
                return await self.async_step_init()
            shown = user_input
        else:  # secrets are never shown again; leaving them empty keeps the stored one
            shown = {
                k: v
                for k, v in config.items()
                if k in setup.keys and k not in setup.secret_keys
            }
        return self.async_show_form(
            step_id="account",
            data_schema=self.add_suggested_values_to_schema(
                setup.schema(config), shown
            ),
            errors=errors,
        )

    async def async_step_finish(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Close the dialog."""
        return self.async_create_entry(title="", data=self._current())

    async def async_step_general(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Language, units and AI Task entity."""
        if user_input is not None:
            # Write every key, so a cleared field overrides the value from setup.
            self._save(
                **{
                    CONF_LANGUAGE: user_input[CONF_LANGUAGE],
                    CONF_UNITS: user_input[CONF_UNITS],
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

    async def async_step_styles(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Style tags and weekly quotas for vegetarian and fish dinners."""
        if user_input is not None:
            self._save(
                **{
                    CONF_STYLE_TAGS: user_input.get(CONF_STYLE_TAGS, []),
                    CONF_VEGETARIAN_DAYS: int(user_input[CONF_VEGETARIAN_DAYS]),
                    CONF_FISH_MIN: int(user_input[CONF_FISH_MIN]),
                    CONF_MAX_SPLIT_DAYS: int(user_input[CONF_MAX_SPLIT_DAYS]),
                }
            )
            return await self.async_step_init()
        config = self._config()
        current = {
            CONF_STYLE_TAGS: config.get(CONF_STYLE_TAGS, []),
            CONF_VEGETARIAN_DAYS: config.get(
                CONF_VEGETARIAN_DAYS, DEFAULT_VEGETARIAN_DAYS
            ),
            CONF_FISH_MIN: config.get(CONF_FISH_MIN, DEFAULT_FISH_MIN),
            CONF_MAX_SPLIT_DAYS: config.get(
                CONF_MAX_SPLIT_DAYS, DEFAULT_MAX_SPLIT_DAYS
            ),
        }
        return self.async_show_form(
            step_id="styles",
            data_schema=self.add_suggested_values_to_schema(STYLES_SCHEMA, current),
        )

    async def async_step_shopping(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Where the shopping goes, where items needing a look go, and what is never bought."""
        if user_input is not None:
            self._save(
                **{
                    CONF_SHOPPING_TARGETS: user_input.get(CONF_SHOPPING_TARGETS, []),
                    CONF_REVIEW_LIST: user_input.get(CONF_REVIEW_LIST),
                    CONF_PANTRY: clean_terms(user_input.get(CONF_PANTRY)),
                }
            )
            return await self.async_step_init()
        config = self._config()
        current = {
            CONF_SHOPPING_TARGETS: config.get(CONF_SHOPPING_TARGETS, []),
            CONF_REVIEW_LIST: config.get(CONF_REVIEW_LIST),
            CONF_PANTRY: config[CONF_PANTRY]
            if config.get(CONF_PANTRY) is not None
            else list(DEFAULT_PANTRY),
        }
        return self.async_show_form(
            step_id="shopping",
            data_schema=self.add_suggested_values_to_schema(SHOPPING_SCHEMA, current),
        )

    async def async_step_notifications(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Who gets notified, about what, and where "Open" leads."""
        services = self.hass.services.async_services_for_domain("notify")
        targets = sorted(set(services) - {"send_message", "persistent_notification"})
        schema = vol.Schema(
            {
                vol.Optional(CONF_NOTIFY_TARGETS): SelectSelector(
                    SelectSelectorConfig(
                        options=targets,
                        multiple=True,
                        custom_value=True,
                        mode=SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Required(CONF_NOTIFY_EVENTS): _select(
                    NOTIFY_EVENTS, "notify_event", multiple=True
                ),
                vol.Required(CONF_OPEN_PATH): TextSelector(),
            }
        )
        if user_input is not None:
            self._save(
                **{
                    CONF_NOTIFY_TARGETS: [
                        t.removeprefix("notify.")
                        for t in user_input.get(CONF_NOTIFY_TARGETS, [])
                    ],
                    CONF_NOTIFY_EVENTS: user_input[CONF_NOTIFY_EVENTS],
                    CONF_OPEN_PATH: user_input[CONF_OPEN_PATH].strip()
                    or DEFAULT_OPEN_PATH,
                }
            )
            return await self.async_step_init()
        config = self._config()
        current = {
            CONF_NOTIFY_TARGETS: config.get(CONF_NOTIFY_TARGETS, []),
            CONF_NOTIFY_EVENTS: config.get(CONF_NOTIFY_EVENTS, NOTIFY_EVENTS),
            CONF_OPEN_PATH: config.get(CONF_OPEN_PATH, DEFAULT_OPEN_PATH),
        }
        return self.async_show_form(
            step_id="notifications",
            data_schema=self.add_suggested_values_to_schema(schema, current),
        )

    async def async_step_sources(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Which recipe sources are used. Priority is fixed by the registry."""
        available: list[str] = self.hass.data[DOMAIN]["registry"].ids
        if user_input is not None:
            self._save(**{CONF_SOURCES: user_input[CONF_SOURCES]})
            return await self.async_step_init()
        enabled = [
            s for s in self._config().get(CONF_SOURCES, available) if s in available
        ]
        schema = vol.Schema(
            {vol.Required(CONF_SOURCES): _select(available, "source", multiple=True)}
        )
        return self.async_show_form(
            step_id="sources",
            data_schema=self.add_suggested_values_to_schema(
                schema, {CONF_SOURCES: enabled}
            ),
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
                MEMBER_COOK_SEPARATELY: True,
                MEMBER_ATTENDS: dinner_days_from_options(self._config())
                or list(DEFAULT_DINNER_DAYS),
            }

        return self.async_show_form(
            step_id="member_form",
            data_schema=self.add_suggested_values_to_schema(MEMBER_SCHEMA, current),
            errors=errors,
        )
