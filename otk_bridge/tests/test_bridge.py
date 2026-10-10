from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestBridge(TransactionCase):
    def test_a_dry_load_reports_what_it_would_create(self):
        before = self.env["res.partner"].search_count([("name", "=", "Dry Run Supplier")])
        answer = self.env["otk.bridge"].dry_load(
            "res.partner", ["name", "is_company"], [["Dry Run Supplier", "1"]]
        )
        self.assertEqual(answer["messages"], [])
        self.assertEqual(len(answer["ids"]), 1)
        self.assertFalse(answer["committed"])
        after = self.env["res.partner"].search_count([("name", "=", "Dry Run Supplier")])
        self.assertEqual(after, before, "a dry run must leave the database untouched")

    def test_a_dry_load_returns_the_errors_the_real_load_would_raise(self):
        answer = self.env["otk.bridge"].dry_load(
            "res.partner", ["name", "country_id/id"], [["Broken", "base.no_such_country"]]
        )
        self.assertTrue(answer["messages"], "an unresolvable reference must be reported")

    def test_an_unknown_model_is_refused(self):
        from odoo.exceptions import UserError

        with self.assertRaises(UserError):
            self.env["otk.bridge"].dry_load("no.such.model", ["name"], [["x"]])
