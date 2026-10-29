"""Phase 5 spike: what does ICA's shopping list accept and return?

Run it yourself (it asks for your login; nothing is written to disk):

    python3 spikes/ica_rows_spike.py

It creates one temporary list, tries the kinds of rows the integration will write
(quantities and units, a row without an amount, a long name), reads the list back, looks
the list up by title the way a retry does, and deletes the list. It touches nothing else.
Paste the printed output back; it contains no login details.
"""
import datetime as dt
import os
import random
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import getpass  # noqa: E402

import ica_spike as base  # noqa: E402
import requests  # noqa: E402

TITLE = "WeeklyMenu rows spike (temp)"

# (productName, quantity, unit): the shapes the integration writes
CASES = [
    ("nötfärs", 350.0, "g"),
    ("grädde", 1.5, "dl"),
    ("smör", 2.0, "msk"),
    ("tomater", 2.0, "förp"),
    ("ägg", 3.0, "st"),
    ("potatis", 1.2, "kg"),
    ("salladskål (inget antal)", 1.0, ""),  # a row without an amount
    ("persilja (antal 0)", 0.0, ""),
    ("gul lök", 2.0, None),  # unit missing entirely
    ("nötfärs gärna ICAs nötfärs 12% eller hushållsfärs", 230.0, "g"),  # long name
]


def make_row(name, quantity, unit):
    row = {
        "offlineId": str(uuid.uuid4()).upper(),
        "productName": name,
        "quantity": quantity,
        "sourceId": -random.randint(10**6, 10**9),
        "isStrikedOver": False,
        "recipes": [],
    }
    if unit is not None:
        row["unit"] = unit
    return row


def main():
    user = base.norm_pnr(os.environ.get("ICA_USER") or input("Personnummer: "))
    pw = os.environ.get("ICA_PASS") or getpass.getpass("ICA password (hidden): ")
    s = requests.Session()
    s.headers["User-Agent"] = base.UA
    tok = base.login(s, user, pw)
    print("1. login OK")

    lists = base.api(s, tok, "GET", base.SL).json()
    print("2. top-level keys of the lists answer:", sorted(lists))
    existing = lists.get("shoppingLists", [])
    if existing:
        print("   keys of one list:", sorted(existing[0]))
        print("   which of them look like an id:", [k for k in existing[0] if "id" in k.lower()])

    oid = str(uuid.uuid4()).upper()
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    base.api(s, tok, "POST", base.SL, {"offlineId": oid, "title": TITLE, "commentText": "",
                                       "sortingStore": 0, "rows": [], "latestChange": ts})
    print("3. temp list created")
    try:
        for name, quantity, unit in CASES:
            try:
                base.api(s, tok, "POST", "%s/%s/sync" % (base.SL, oid),
                         {"createdRows": [make_row(name, quantity, unit)]})
                print("   accepted: %r qty=%r unit=%r" % (name, quantity, unit))
            except SystemExit as err:
                print("   REJECTED: %r qty=%r unit=%r -> %s" % (name, quantity, unit, err))

        got = base.api(s, tok, "GET", "%s/%s" % (base.SL, oid)).json()
        print("4. list answer keys:", sorted(got))
        rows = got.get("rows", [])
        print("   row keys:", sorted(rows[0]) if rows else "(no rows)")
        for r in rows:
            print("   read back: %r qty=%r unit=%r" % (r.get("productName"), r.get("quantity"), r.get("unit")))

        found = [l for l in base.api(s, tok, "GET", base.SL).json().get("shoppingLists", [])
                 if str(l.get("title", "")).casefold() == TITLE.casefold()]
        print("5. found by title:", len(found), "| id keys:",
              {k: (v == oid) for k, v in (found[0].items() if found else []) if "id" in k.lower()})
    finally:
        base.api(s, tok, "DELETE", "%s/%s" % (base.SL, oid))
        print("6. temp list deleted")
    print("\nSPIKE RESULT: rows spike finished.")


if __name__ == "__main__":
    sys.exit(main())
