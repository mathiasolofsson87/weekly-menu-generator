"""What can stand in for an ingredient someone cannot eat.

Each `SwapKind` recognises a kind of ingredient line (mince, chicken, stock...) and
lists candidate replacements in preference order. The table is data: add a kind or
a candidate here and the planner and the shopping list pick it up.

Choosing one (`eligibility._replacement`):
1. Only candidates that are safe for everyone who gets them: by name through the
   allergen and diet rules, and by what the product declares (`contains` for diets
   and allergies, `traces` for allergies only), since "vegofärs" does not say it is
   made of soy.
2. The dish decides the order: a candidate whose `fits` matches the recipe title goes
   first (beans in tacos, mushrooms in a stew), one whose `unfit` matches goes last
   and is only used when nothing else is safe (lentils do not make burgers).
3. Variety: a candidate already used elsewhere in the week is passed over when an
   unused one fits as well, so a week with three chicken dinners does not become
   tofu, tofu, tofu. It is deterministic: same week, same choices.

Names are generic product descriptions ("vegofärs", "vegetariska kycklingbitar"),
because the line goes to a grocery list. Brands appear only in `examples`, which the
shopping list shows as a note. `{name}` is filled in with the original ("laktosfri
{name}" -> "laktosfri grädde") and `{stock}` with its kind of stock ("buljongtärning",
"fond"). Amounts are converted by `factor`; counted pieces become grams through the
kind's `piece_grams` unless the replacement is counted too (`pieces`).

Product facts (checked 2026-11 on handla.ica.se and Open Food Facts; recipes change,
so contents are declared over-cautiously for the whole category, not one brand):
- Anamma (Orkla): Vegofärs 450 g / 1 kg, Vegobullar 300 g / 900 g and Vegokorv
  840 g are soy based and labelled gluten free; Formbar färs av ärta 750 g may hold
  soy.
- Hälsans Kök (Nomad Foods): Färs 850 g (soy flour, wheat protein, barley malt;
  traces of celery, egg, mustard, sesame), Filébitar 320 g (soy; traces of gluten,
  egg, sesame, celery, mustard), Soja bacon, Vegostrimlor, Veganska bullar 300 g,
  schnitzel and nuggets (soy and wheat). Some products (the OVO fillets) hold egg.
- Quorn: Bitar 300 / 600 g and Färs are mycoprotein with egg white; strimlor hold
  wheat, some products milk protein.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .allergens import (
    ALLERGEN_RULES,
    DAIRY_EXCEPTIONS,
    MEAT,
    PLANT_BASED,
    Rule,
)

# Ingredients that carry meat or fish flavour and have no stand-in: a recipe with
# anchovies or fish sauce is not "fine apart from the steak". Stock is swapped.
FLAVOURING = Rule(
    terms=(
        "extrakt", "extract", "ister", "ansjovis", "anchov", "sardell", "worcester",
        "fisksås", "fish sauce", "ostronsås", "oyster sauce", "skmalz", "fett", "tallow",
        "lard", "gelatin",
    ),
)  # fmt: skip

_STOCK = re.compile(r"buljongtärning|buljong|fond|bouillon|kraft|stock|broth")


@dataclass(frozen=True)
class Replacement:
    name: str
    factor: float = 1.0
    # Allergens the product holds, declared on purpose and over-cautiously for the
    # whole category. They count for allergies and for a vegan diet (milk, egg).
    contains: tuple[str, ...] = ()
    # Allergens some products of the category may hold or carry as traces. They count
    # for allergies only: a vegan can pick a vegan brand, an allergic person cannot
    # tell from "vegofärs" which brand is safe.
    traces: tuple[str, ...] = ()
    fits: str = ""  # regex on the recipe title: this candidate first
    unfit: str = ""  # regex on the recipe title: only when nothing else is safe
    pieces: bool = False  # bought in pieces too, so "6 st korv" -> "6 st vegokorv"
    examples: str = ""  # brands, for the shopping note; never in the name
    packs: tuple[int, ...] = ()  # usual pack sizes in grams, for reference

    def render(self, original: str) -> str:
        """The shopping name for replacing `original`."""
        stock = ""
        if "{stock}" in self.name:
            found = _STOCK.search(original)
            word = found.group(0) if found else "buljong"
            stock = word if word in ("buljongtärning", "fond") else "buljong"
            if "konc" in original:
                return "konc " + self.name.format(name=original, stock=stock)
        return self.name.format(name=original, stock=stock)

    def rank(self, title: str) -> int:
        """0 when it suits the dish, 1 when nothing is said, 2 when it does not suit."""
        title = title.casefold()
        if self.unfit and re.search(self.unfit, title):
            return 2
        return 0 if self.fits and re.search(self.fits, title) else 1


@dataclass(frozen=True)
class SwapKind:
    key: str
    rule: Rule
    replacements: tuple[Replacement, ...]
    piece_grams: float | None = None  # grams per counted piece, for converting "st"


# --- dish words (matched in the casefolded title) ---------------------------------
_SHAPED = (
    r"biff|burgare|bullar|järpar|frikadell|köfte|kebab|färslimpa|dolm|pirog|nugget"
)
_MEXICAN = r"taco|burrito|chili|enchilada|quesadilla|nacho|fajita|mexi"
_STEW = (
    r"gryta|kalops|bourguignon|stroganoff|ragu|ragù|goulash|gulasch|chili|stew|"
    r"tagine|curry|soppa|carbonnade|kebabgryta"
)
_GRILLED = r"biff|stek|grill|entrecote|ryggbiff|filé|kotlett|plank|steak|spett"
_PULLED = r"pulled|taco|burrito|bbq|barbecue|wrap|burgare"
_STRIPS = r"wok|strimlor|fajita|stroganoff|teriyaki|bulgogi|nudlar|pad thai|stir"
_ASIAN = r"wok|curry|nudl|ramen|pad thai|thai|asia|teriyaki|bang bang|sushi|poke|bowl"
_ONLY = r"^(?!.*(?:{}))"  # unfit unless the title has one of the words

# --- products ------------------------------------------------------------------
# Traces and "some brands hold" for processed meat substitutes, from the facts above.
_PROCESSED_TRACES = ("egg", "milk", "celery", "mustard", "sesame", "gluten")

_VEGOFARS = Replacement(
    "vegofärs",
    contains=("soy", "gluten"),
    traces=_PROCESSED_TRACES,
    examples="t.ex. Anamma Vegofärs eller Hälsans Kök Färs",
    packs=(450, 850, 1000),
)
_RED_LENTILS = Replacement("röda linser", 0.5, unfit=_SHAPED)  # dry: half the weight
_BLACK_BEANS = Replacement(
    "svarta bönor", fits=_MEXICAN, unfit=_ONLY.format(_MEXICAN)
)  # cooked
_CHICKPEAS = Replacement("kikärtor", unfit=_SHAPED + r"|bolognese|köttfärssås|lasagne")
_TOFU = Replacement("tofu", contains=("soy",), fits=_ASIAN)
_SMOKED_TOFU = Replacement("rökt tofu", 0.7, contains=("soy",))
_PORTOBELLO = Replacement("portobellosvamp", fits=_GRILLED)
_HALLOUMI = Replacement(
    "halloumi",
    0.6,  # rich: about 100 g a portion where meat would be 150-180 g
    contains=("milk",),
    fits=r"grill|spett|sallad|bowl|wrap|taco|burgare|pita|souvlaki|ugn|plåt|halloumi",
    unfit=r"soppa|wok|nudl|ramen|pad thai|sushi|poke|gratäng|gryta",
)
_CHICKEN_PIECES = Replacement(
    "vegetariska kycklingbitar",
    contains=("soy", "gluten"),
    traces=_PROCESSED_TRACES,
    examples="t.ex. Hälsans Kök Filébitar eller Quorn Bitar (Quorn innehåller ägg)",
    packs=(300, 320, 600),
)

_LACTOSE_FREE = Replacement("laktosfri {name}")
_PLANT = Replacement("växtbaserad {name}", contains=("soy", "gluten", "tree_nuts"))

_DAIRY_FREE_FROM = PLANT_BASED + ("mjölkfri", "dairy-free")
_GLUTEN = ALLERGEN_RULES["gluten"]


def _dairy(*terms: str) -> Rule:
    return Rule(terms=terms, exceptions=DAIRY_EXCEPTIONS, free_from=_DAIRY_FREE_FROM)


def _gluten(*terms: str) -> Rule:
    return Rule(terms=terms, exceptions=_GLUTEN.exceptions, free_from=_GLUTEN.free_from)


# Order matters: the first kind that matches wins, so stock is tested before meat
# ("köttbuljong") and meatballs before mince.
KINDS: tuple[SwapKind, ...] = (
    # --- meat and fish
    SwapKind(
        "stock",
        Rule(terms=(_STOCK.pattern,)),
        (Replacement("grönsaks{stock}", contains=("celery",)),),
    ),
    SwapKind(
        "meatballs",
        Rule(terms=("köttbull", "meatball")),
        (
            Replacement(
                "vegobullar",
                contains=("soy", "gluten"),
                traces=_PROCESSED_TRACES,
                pieces=True,
                examples="t.ex. Anamma Vegobullar eller Hälsans Kök Veganska bullar",
                packs=(300, 900),
            ),
            Replacement(
                "falafel",
                traces=("gluten", "sesame", "soy"),
                pieces=True,
                fits=r"pita|sallad|bowl|wrap|bröd",
                unfit=r"gräddsås|mos|lingon|spaghetti|pasta",
            ),
        ),
        piece_grams=15,
    ),
    SwapKind(
        "mince",
        Rule(terms=(r"färs(?!k)", "mince")),  # not "färsk" (fresh): färsk laxfilé
        (_VEGOFARS, _RED_LENTILS, _BLACK_BEANS, _CHICKPEAS),
    ),
    SwapKind(
        "sausage",
        Rule(terms=("korv", "sausage", "salsiccia")),
        (
            Replacement(
                "vegokorv",
                contains=("soy", "gluten"),
                traces=_PROCESSED_TRACES,
                pieces=True,
                examples="t.ex. Anamma Vegokorv",
                packs=(840,),
            ),
            Replacement(
                "rökt tofu",
                0.7,
                contains=("soy",),
                                unfit=r"korv med|hot ?dog|grill|korvbröd|mos\b",
            ),
        ),
        piece_grams=80,
    ),
    SwapKind(
        "bacon",
        Rule(terms=("bacon", "pancetta", "guanciale", "sidfläsk", r"rimmat fläsk", r"\bfläsk\b")),
        (
            Replacement(
                "vegetariskt bacon",
                contains=("soy", "gluten"),
                traces=_PROCESSED_TRACES,
                examples="t.ex. Hälsans Kök Soja bacon",
            ),
            _SMOKED_TOFU,
            Replacement("portobellosvamp", 0.7),
        ),
    ),
    SwapKind(
        "cured",
        Rule(terms=("skinka", "prosciutto", "salami", "chorizo", "kassler", "serrano", r"\bham\b")),
        (_SMOKED_TOFU, Replacement("portobellosvamp", 0.7)),
    ),
    SwapKind(
        "poultry",
        Rule(terms=("kyckling", "kalkon", r"\bank|anka\b", "chicken", "turkey", "duck")),
        (
            _CHICKEN_PIECES,
            _TOFU,
            _HALLOUMI,
            Replacement(
                "kikärtor",
                fits=r"gryta|curry|tagine|marock|indisk|tikka|korma|sallad|soppa",
                unfit=r"panerad|schnitzel|nugget|burgare|spett|club|sandwich|macka|klubb",
            ),
        ),
        piece_grams=150,
    ),
    # Fish fingers: halloumi sticks. A "vegetarian fish finger" is not listed: its
    # name says "fisk", which the fish rule rightly refuses.
    SwapKind(
        "fish_fingers",
        Rule(terms=("fiskpinn", "fish finger", "fish stick")),
        (_HALLOUMI, _TOFU),
        piece_grams=25,
    ),
    SwapKind(
        "fish",
        ALLERGEN_RULES["fish"],
        (
            Replacement("tofu", contains=("soy",), fits=_ASIAN + r"|soppa|gryta"),
            _HALLOUMI,
            Replacement(
                "blomkål",
                fits=r"gratäng|ugn|plåt|rostad",
                unfit=r"soppa|taco|sushi|poke|burgare|wok|ceviche|gryta",
            ),
            Replacement(
                "kikärtor",
                fits=r"soppa|gryta|curry",
                unfit=r"ugn|grill|sushi|poke|burgare|plank",
            ),
        ),
        piece_grams=150,
    ),
    SwapKind(
        "shellfish",
        Rule(terms=ALLERGEN_RULES["crustaceans"].terms + ALLERGEN_RULES["molluscs"].terms),
        (_TOFU, Replacement("kikärtor", unfit=r"sushi|poke|toast|smörgås|macka")),
    ),
    SwapKind(
        "meat",
        MEAT,
        (
            _PORTOBELLO,
            Replacement("champinjoner", fits=_STEW, unfit=_PULLED),
            Replacement(
                "vegetariska strimlor",
                contains=("soy", "gluten"),
                traces=_PROCESSED_TRACES,
                fits=_STRIPS,
                examples="t.ex. Hälsans Kök Vegostrimlor",
            ),
            Replacement("jackfrukt", fits=_PULLED, unfit=_ONLY.format(_PULLED)),
            _HALLOUMI,
            _TOFU,
            Replacement("kikärtor", fits=_STEW, unfit=_GRILLED),
            Replacement("svarta bönor", fits=_MEXICAN, unfit=_ONLY.format(_MEXICAN)),
        ),
        piece_grams=200,
    ),
    # --- dairy (lactose-free first: it suits lactose intolerance but not milk allergy)
    SwapKind(
        "cream",
        _dairy("grädde", "cream", "gräddfil", "crème fraîche", "creme fraiche", "crème fraiche", "mascarpone"),
        (_LACTOSE_FREE, Replacement("havregrädde"), _PLANT),
    ),
    SwapKind(
        "milk",
        _dairy("mjölk", "milk", "kefir", "vassle"),
        (_LACTOSE_FREE, Replacement("havredryck"), Replacement("sojadryck", contains=("soy",))),
    ),
    SwapKind(
        "butter",
        _dairy("smör", "butter", "ghee"),
        (Replacement("laktosfritt smör"), Replacement("växtbaserat margarin", contains=("soy",))),
    ),
    SwapKind(
        "yoghurt",
        _dairy("yoghurt", "yogurt", "kvarg", "quark", "keso", "cottage"),
        (_LACTOSE_FREE, Replacement("sojayoghurt", contains=("soy",)), Replacement("havreyoghurt")),
    ),
    SwapKind("dairy", ALLERGEN_RULES["milk"], (_LACTOSE_FREE, _PLANT)),  # cheese and the rest
    # --- gluten
    SwapKind(
        "grain",
        _gluten("couscous", "bulgur"),
        (Replacement("quinoa"), Replacement("ris")),
    ),
    SwapKind("noodles", _gluten("nudl", "noodle"), (Replacement("risnudlar"),)),
    SwapKind(
        "flour",
        _gluten("mjöl", "flour"),
        (Replacement("glutenfritt mjöl"), Replacement("majsmjöl")),
    ),
    SwapKind("gluten", _GLUTEN, (Replacement("glutenfri {name}"),)),  # pasta, bread, tortilla
)  # fmt: skip


def kind_of(text: str) -> SwapKind | None:
    """The kind of swap an ingredient text calls for."""
    return next((k for k in KINDS if k.rule.match(text)), None)


_EXAMPLES = {r.name: r.examples for k in KINDS for r in k.replacements if r.examples}


def substitute_note(name: str) -> str:
    """Brand examples for a replacement product, for the shopping note ("" if none)."""
    return _EXAMPLES.get(name.casefold(), "")
