# Copyright (C) 2022, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountPaymentMethod(models.Model):
    _inherit = "account.payment.method"

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res["nacha_ccd"] = {
            "mode": "multi",
            "domain": [("type", "=", "bank")],
            "currency_ids": self.env.ref("base.USD").ids,
            "country_id": self.env.ref("base.us").id,
        }
        return res
