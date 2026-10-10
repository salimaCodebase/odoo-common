"""The three things otk_bridge promises, checked against the live server.

The module's own TransactionCase suite needs odoo-bin on a build, and SSH is
off for this project. These exercise the same three behaviours over the API.
"""
import sys
sys.path.insert(0, "/Users/truster/Projects/Odoo/toolkit/src")
from odoo_toolkit import connect
from odoo_toolkit.rpc import OdooError

odoo = connect()
ok = True

def check(label, condition, detail=""):
    global ok
    print(f"  {'ok  ' if condition else 'FAIL'} {label}{(' — ' + detail) if detail else ''}")
    ok = ok and condition

NAME = "Dry Run Supplier (otk_bridge check)"
before = odoo.call("res.partner", "search_count", domain=[("name", "=", NAME)])

print("1. a dry load reports what it would create, and creates nothing")
answer = odoo.call("otk.bridge", "dry_load",
                   model_name="res.partner", fields=["name", "is_company"],
                   rows=[[NAME, "1"]])
after = odoo.call("res.partner", "search_count", domain=[("name", "=", NAME)])
check("no messages", answer["messages"] == [], str(answer["messages"]))
check("one id reported", len(answer["ids"]) == 1, str(answer["ids"]))
check("committed is false", answer["committed"] is False)
check("database untouched", after == before, f"{before} before, {after} after")

print("2. a dry load returns the errors a real load would raise")
answer = odoo.call("otk.bridge", "dry_load",
                   model_name="res.partner", fields=["name", "country_id/id"],
                   rows=[["Broken", "base.no_such_country"]])
check("unresolvable reference reported", bool(answer["messages"]),
      str(answer["messages"])[:120])

print("3. an unknown model is refused")
try:
    odoo.call("otk.bridge", "dry_load",
              model_name="no.such.model", fields=["name"], rows=[["x"]])
    check("refused", False, "it did not raise")
except OdooError as failure:
    check("refused", "no.such.model" in str(failure), str(failure)[:100])

print("\nALL THREE HOLD" if ok else "\nSOMETHING FAILED")
sys.exit(0 if ok else 1)
