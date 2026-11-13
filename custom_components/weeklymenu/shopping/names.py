"""Shopping names: drop how a thing is cut or cooked, and match singular and plural.

Conservative by design: only words in the tables below are touched, so an unknown
word is kept as written rather than guessed at.
"""

from __future__ import annotations

import re

# How the cook prepares something; you buy the thing itself ("hackad dill" -> "dill").
PREPARATION = frozenset(
    {
        "hackad", "hackade", "hackat", "finhackad", "finhackade", "finhackat",
        "grovhackad", "grovhackade", "grovhackat", "skivad", "skivade", "skivat",
        "strimlad", "strimlade", "strimlat", "tärnad", "tärnade", "tärnat",
        "skuren", "skurna", "skuret", "finskuren", "finskurna", "finskuret",
        "riven", "rivna", "rivet", "finriven", "finrivna", "finrivet", "grovriven",
        "grovrivna", "rostad", "rostade", "rostat", "stekt", "stekta", "smulad", "smulade", "smulat",
        "pressad", "pressade", "pressat", "kokt", "kokta", "mosad", "mosade",
        "skalad", "skalade", "skalat", "grovskuren", "grovskurna", "grovskuret",
        "nymalen", "nymald", "nymalet", "nymalda", "färskmalen", "färskmald", "urkärnad", "delad", "delade", "halverad",
        "halverade", "klyftad", "klyftade", "sköljd", "sköljda", "avrunnen", "avrunna",
        "chopped", "sliced", "diced", "grated", "minced", "crushed", "shredded", "toasted",
    }
)  # fmt: skip
_ADVERBS = frozenset({"fint", "grovt", "tunt", "finely", "thinly", "roughly"})
# Sizes: "1 liten gul lök" is bought with the other onions (the note keeps the size).
_SIZES = frozenset(
    {"liten", "litet", "små", "stor", "stort", "stora", "medelstor", "medelstort",
     "medelstora", "mellanstor", "mellanstora", "small", "medium", "large"}
)  # fmt: skip
# Where it comes from, not what it is: "salt från kvarnen", "peppar ur kvarnen".
_FROM = re.compile(r"\s+(?:från|ur)\s+(?:kvarnen|burk(?:en)?)\b")
# "nöt- eller blandfärs": the alternatives share the last word's head ("nötfärs").
_SHARED_HEAD = re.compile(
    r"^(\w+)-\s+(?:eller|or)\s+\w*?(färs|nudlar|filé|filéer|kött|bönor|lök)\b"
)
# "citron i klyftor", "ost i skivor". Product forms such as "i lake" or "i tomatsås" stay.
_CUT_INTO = re.compile(
    r"\s+i\s+(?:(?:små|mindre|stora|tunna|grova|fina)\s+)?"
    r"(?:klyftor|tärningar|skivor|bitar|strimlor|ringar|kuber|halvor|stavar|stänger)\b"
)
# Whole names where the preparation is the product: you buy fried onion, not onion.
_PRODUCTS = frozenset(
    {"rostad lök", "stekt lök", "riven ost", "kokt skinka", "krossade tomater"}
)

# Singular -> plural, also matched at the end of a compound ("salladslök", "kålrot").
_NOUNS = {
    "citron": "citroner", "tomat": "tomater", "lök": "lökar", "rot": "rötter",
    "aubergine": "auberginer", "paprika": "paprikor", "gurka": "gurkor",
    "klyfta": "klyftor", "huvud": "huvuden", "avokado": "avokador", "äpple": "äpplen",
    "banan": "bananer", "potatis": "potatisar", "frö": "frön", "böna": "bönor",
    "ärta": "ärtor", "beta": "betor", "räka": "räkor", "oliv": "oliver",
    "squash": "squashar", "frukt": "frukter", "filé": "filéer", "nacka": "nackor", "stång": "stänger",
}  # fmt: skip
_ADJECTIVES = {
    "gul": "gula",
    "röd": "röda",
    "vit": "vita",
    "grön": "gröna",
    "stor": "stora",
}
_SINGULAR = {plural: singular for singular, plural in (_NOUNS | _ADJECTIVES).items()}
_PLURAL_ENDINGS = sorted(_SINGULAR, key=len, reverse=True)
_SINGULAR_ENDINGS = sorted(_NOUNS, key=len, reverse=True)


def strip_preparation(name: str) -> str:
    """The name without preparation words; unchanged if nothing would be left."""
    if name.casefold() in _PRODUCTS:
        return name
    name = _SHARED_HEAD.sub(r"\1\2", _FROM.sub("", name))
    words = _CUT_INTO.sub("", name).split()
    kept = [
        word
        for index, word in enumerate(words)
        if word.casefold() not in PREPARATION
        and word.casefold() not in _SIZES
        and not (
            word.casefold() in _ADVERBS
            and index + 1 < len(words)
            and words[index + 1].casefold() in PREPARATION
        )
    ]
    return " ".join(kept) or name


def _singular(word: str) -> str:
    if word in _SINGULAR:
        return _SINGULAR[word]
    for ending in _PLURAL_ENDINGS:
        if word.endswith(ending) and ending not in _ADJECTIVES.values():
            return word[: -len(ending)] + _SINGULAR[ending]
    return word


def _plural(word: str) -> str:
    for single in _SINGULAR_ENDINGS:
        if word.endswith(single):
            return word[: -len(single)] + _NOUNS[single]
    return word


def singular(name: str) -> str:
    """Known plural words made singular: the key that merges "citron" and "citroner"."""
    return " ".join(_singular(word) for word in name.casefold().split())


def counted(name: str, amount: float) -> str:
    """`name` in the number that fits `amount` when its words are known: "2 citroner"."""
    words = singular(name).split()
    if words and amount > 1:
        words = [_ADJECTIVES.get(word, word) for word in words[:-1]] + [
            _plural(words[-1])
        ]
    text = " ".join(words)
    return name if text == name.casefold() else text
