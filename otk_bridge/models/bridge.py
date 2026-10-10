"""A load that is undone before the request ends.

Loading master data into a live database is the one irreversible step in this
work, and the external API offers no transaction control: a load over JSON-2
commits. This model gives the loader the transaction it needs — it performs
the load, collects everything Odoo complains about, then rolls the cursor
back. The return value survives the rollback because it is a Python value,
already built by the time the cursor is discarded.
"""

from odoo import api, models
from odoo.exceptions import UserError


class OtkBridge(models.AbstractModel):
    _name = "otk.bridge"
    _description = "Workspace tooling bridge"

    @api.model
    def dry_load(self, model_name, fields, rows, context=None):
        if model_name not in self.env:
            raise UserError(f"unknown model: {model_name}")
        target = self.env[model_name]
        if context:
            target = target.with_context(**context)
        try:
            answer = target.load(fields, rows)
        finally:
            self.env.cr.rollback()
        return {
            "ids": answer.get("ids") or [],
            "messages": answer.get("messages") or [],
            "committed": False,
        }
