# Copyright (C) 2022 - TODAY, Open Source Integrators
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    portal_show_invoice = fields.Boolean(string="Show Invoice/Bills on Portal")