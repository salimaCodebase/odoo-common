{
    "name": "OTK Bridge",
    "summary": "Server-side helper for the workspace tooling: loads that roll back",
    "version": "1.0.0",
    "category": "Technical",
    "license": "LGPL-3",
    "depends": ["base"],
    # No access file: otk.bridge is an AbstractModel, so it has no rows to
    # protect — and the access file is the one thing that cannot be written
    # portably across 19 and 20 (ir.model.access.csv against ir.access.csv,
    # different model, different columns).
    "installable": True,
    "application": False,
}
