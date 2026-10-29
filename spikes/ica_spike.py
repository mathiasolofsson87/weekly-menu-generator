"""Phase 0 spike: can we log in to ICA and write to a shopping list?

Flow ported from LazyTarget/ha-ica-todo via kanylbullen/ica-mcp (MIT).
Steps: login -> list shopping lists -> create temp list -> add 2 free-text rows
-> read back -> delete the temp list. Touches only the temp list it creates.
Credentials are read from ICA_USER/ICA_PASS or prompted (password hidden).
Nothing is written to disk; tokens stay in memory.
"""
import base64
import datetime as dt
import getpass
import hashlib
import json
import os
import random
import re
import sys
import uuid
from urllib.parse import parse_qs, urlparse

import requests

IMS = "https://ims.icagruppen.se"
API = "https://apimgw-pub.ica.se"
SL = "sverige/digx/mobile/shoppinglistservice/v1/shoppinglists"
ACR = "urn:se:curity:authentication:html-form:IcaCustomers"
REDIRECT = "icacurity://app"
UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) "
      "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148")
# Public client registration used by the ICA app (published in open-source clients).
DCR_ID = "ica-app-dcr-registration"
DCR_SECRET = "uxLHTBvZ-Z2fV-SbrHl1E-tz7vB3jQFrwAdSLlbVMMu1rxDdvJU0s8KGu9d1wLS4"


def norm_pnr(v):
    d = "".join(c for c in v if c.isdigit())
    if len(d) == 10:
        century = "20" if int(d[:2]) <= dt.date.today().year % 100 else "19"
        d = century + d
    return d


def qs(loc, key):
    vals = parse_qs(urlparse(loc).query).get(key)
    if not vals:
        raise SystemExit("missing %r in redirect" % key)
    return vals[0]


def login(s, user, pw):
    r = s.post(IMS + "/oauth/v2/token", data={
        "client_id": DCR_ID, "client_secret": DCR_SECRET,
        "grant_type": "client_credentials", "scope": "dcr", "response_type": "token"}, timeout=30)
    r.raise_for_status()
    boot = r.json()["access_token"]
    r = s.post(IMS + "/register", json={"software_id": "dcr-ica-app-template"},
               headers={"Authorization": "Bearer " + boot}, timeout=30)
    r.raise_for_status()
    client = r.json()
    verifier = re.sub("[^a-zA-Z0-9]+", "", base64.urlsafe_b64encode(os.urandom(40)).decode())
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().replace("=", "")
    r = s.get(IMS + "/oauth/v2/authorize", params={
        "client_id": client["client_id"], "scope": client["scope"], "redirect_uri": REDIRECT,
        "response_type": "code", "code_challenge": challenge, "code_challenge_method": "S256",
        "prompt": "login", "acr": ACR}, allow_redirects=False, timeout=30)
    r.raise_for_status()
    state = qs(r.headers["Location"], "state")
    s.get(r.headers["Location"], timeout=30).raise_for_status()
    r = s.post(IMS + "/authn/authenticate/IcaCustomers",
               data={"userName": user, "password": pw}, timeout=30)
    r.raise_for_status()
    m = re.search(r'name="token"[^>]*value="([^"]*)"', r.text) or \
        re.search(r'value="([^"]*)"[^>]*name="token"', r.text)
    if not m:
        raise SystemExit("Login failed: no token in response (wrong credentials, or account needs BankID).")
    r = s.post(IMS + "/oauth/v2/authorize",
               params={"client_id": client["client_id"], "forceAuthN": "true", "acr": ACR},
               data={"token": m.group(1), "state": state}, allow_redirects=False, timeout=30)
    r.raise_for_status()
    code = qs(r.headers["Location"], "code")
    r = s.post(IMS + "/oauth/v2/token", data={
        "code": code, "client_id": client["client_id"], "client_secret": client["client_secret"],
        "grant_type": "authorization_code", "scope": client["scope"], "response_type": "token",
        "code_verifier": verifier, "redirect_uri": REDIRECT}, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]


def api(s, tok, method, path, body=None):
    h = {"Authorization": "Bearer " + tok}
    data = None
    if body is not None:
        h["Content-Type"] = "application/json; charset=utf-8"
        data = json.dumps(body)
    r = s.request(method, API + "/" + path, headers=h, data=data, timeout=30)
    if r.status_code == 451:
        raise SystemExit("HTTP 451: ICA geo-blocks non-Swedish IPs.")
    if not r.ok:
        raise SystemExit("%s %s -> HTTP %s: %s" % (method, path, r.status_code, r.text[:300]))
    return r


def main():
    user = norm_pnr(os.environ.get("ICA_USER") or input("Personnummer: "))
    pw = os.environ.get("ICA_PASS") or getpass.getpass("ICA password (hidden): ")
    s = requests.Session()
    s.headers["User-Agent"] = UA
    tok = login(s, user, pw)
    print("1. login OK")
    lists = api(s, tok, "GET", SL).json().get("shoppingLists", [])
    print("2. your lists:", [l.get("title") for l in lists])
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    oid = str(uuid.uuid4()).upper()
    api(s, tok, "POST", SL, {"offlineId": oid, "title": "WeeklyMenu spike (temp)", "commentText": "",
                             "sortingStore": 0, "rows": [], "latestChange": ts})
    print("3. temp list created")
    try:
        rows = [{"offlineId": str(uuid.uuid4()).upper(), "productName": n, "quantity": q, "unit": u,
                 "sourceId": -random.randint(10**6, 10**9), "isStrikedOver": False, "recipes": []}
                for n, q, u in (("nötfärs", 350.0, "g"), ("gul lök", 2.0, "st"))]
        api(s, tok, "POST", "%s/%s/sync" % (SL, oid), {"createdRows": rows})
        got = api(s, tok, "GET", "%s/%s" % (SL, oid)).json()
        print("4. rows read back:", [(r.get("productName"), r.get("quantity"), r.get("unit"))
                                     for r in got.get("rows", [])])
    finally:
        api(s, tok, "DELETE", "%s/%s" % (SL, oid))
        print("5. temp list deleted")
    print("\nSPIKE RESULT: ICA login + shopping list write works.")


if __name__ == "__main__":
    sys.exit(main())
