"""Constants for the Weekly Menu integration."""

from __future__ import annotations

DOMAIN = "weeklymenu"

# Config entry data / options keys
CONF_LANGUAGE = "language"
CONF_UNITS = "units"
CONF_SHOPPING_TARGETS = "shopping_targets"
CONF_AI_TASK = "ai_task_entity"
CONF_GENERATION_DAY = "generation_day"
CONF_GENERATION_TIME = "generation_time"
CONF_DINNER_DAYS = "dinner_days"
CONF_MEMBERS = "members"

# Family member keys
MEMBER_ID = "id"
MEMBER_NAME = "name"
MEMBER_PERSON = "person"
MEMBER_ALLERGIES = "allergies"
MEMBER_DISLIKES = "dislikes"
MEMBER_LIKES = "likes"
MEMBER_DIET = "diet"
MEMBER_PORTION = "portion"
MEMBER_ATTENDS = "attends"

LANGUAGES = ["sv", "en"]
UNITS = ["swedish", "metric"]  # swedish: dl, msk, tsk. metric: ml, g.

# Index matches datetime.weekday()
WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

# The 14 EU allergens plus lactose intolerance, which is common and distinct from milk allergy.
ALLERGENS = [
    "gluten",
    "milk",
    "lactose",
    "egg",
    "fish",
    "crustaceans",
    "molluscs",
    "peanuts",
    "tree_nuts",
    "soy",
    "sesame",
    "celery",
    "mustard",
    "lupin",
    "sulphites",
]
DIETS = ["omnivore", "vegetarian", "vegan", "pescatarian"]
PORTIONS = ["small", "normal", "large"]

DEFAULT_LANGUAGE = "sv"
DEFAULT_UNITS = "swedish"
DEFAULT_GENERATION_DAY = "fri"
DEFAULT_GENERATION_TIME = "06:00:00"
DEFAULT_DINNER_DAYS = ["mon", "tue", "wed", "thu", "fri"]

EVENT_GENERATION_DUE = "weeklymenu_generation_due"
