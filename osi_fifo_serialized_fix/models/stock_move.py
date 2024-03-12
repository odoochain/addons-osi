# Copyright (C) 2023, Open Source Integrators
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    def get_ji_ids(self, move, svl_ids):
        ji_ids = self.env["account.move.line"].search(
            [
                ("name", "ilike", move.picking_id.name),
                ("name", "ilike", move.product_id.name),
            ]
        )
        if ji_ids:
            if len(svl_ids) > 1:
                final_layers = []
                # If there are multiple layers, delete them and create correct ones
                for layer in move.stock_valuation_layer_ids:
                    layer.sudo().unlink()
                for svl_id in svl_ids:
                    val = move.product_id._prepare_out_svl_vals(
                        svl_id[1], self.env.user.company_id
                    )
                    val_obj = self.env["stock.valuation.layer"].browse(svl_id[0])
                    val["unit_cost"] = val_obj.unit_cost
                    val["company_id"] = self.env.user.company_id.id
                    val["lot_ids"] = [(6, 0, svl_id[2])]
                    val["account_move_id"] = ji_ids[0].move_id.id
                    # The qty of serial products is always 1, lots could be > 1
                    if svl_id[3].product_id.tracking == "lot":
                        val["quantity"] = svl_id[3].qty_done * -1
                    val["value"] = val_obj.unit_cost * val["quantity"]
                    final_layers.append(val)
                final_layers = self.env["stock.valuation.layer"].create(final_layers)
                move.write({"stock_valuation_layer_ids": [(6, 0, final_layers.ids)]})
                ji_ids[0].move_id.button_draft()
                ji_val = 0
                for sv_id in move.stock_valuation_layer_ids:
                    if sv_id.product_id == ji_ids[0].product_id:
                        ji_val += sv_id.value * -1
                # The Valuation Layers have been made, now edit the STJ Entries
                for ji_id in ji_ids:
                    if ji_id.credit != 0:
                        ji_id.with_context(check_move_validity=False).write(
                            {"credit": ji_val}
                        )
                    else:
                        ji_id.with_context(check_move_validity=False).write(
                            {"debit": ji_val}
                        )
                ji_ids[0].move_id.action_post()
            elif len(svl_ids) == 1:
                # Only 1 Valuation Layer, we can just change values
                if len(move.stock_valuation_layer_ids.ids) > 1:
                    svl = self.env["stock.valuation.layer"].browse(svl_ids[0][0])
                    val = move.stock_valuation_layer_ids[0]
                    val.unit_cost = -1 * svl.unit_cost
                    for layer in move.stock_valuation_layer_ids:
                        layer.sudo().unlink()
                    move.write({"stock_valuation_layer_ids": [6, 0, val.id]})
                else:
                    move.stock_valuation_layer_ids.lot_ids = [(6, 0, svl_ids[0][2])]
                    svl = self.env["stock.valuation.layer"].browse(svl_ids[0][0])
                    linked_svl = self.env["stock.valuation.layer"].search(
                        [("stock_valuation_layer_id", "=", svl.id)]
                    )
                    unit_cost = svl.unit_cost
                    for link_svl in linked_svl:
                        unit_cost += link_svl.value
                    move.stock_valuation_layer_ids.unit_cost = unit_cost
                    move.stock_valuation_layer_ids.value = (
                        move.stock_valuation_layer_ids.quantity
                        * move.stock_valuation_layer_ids.unit_cost
                    )
                    move.stock_valuation_layer_ids.remaining_value = (
                        move.stock_valuation_layer_ids.value
                    )
                ji_ids[0].move_id.button_draft()
                # The Valuation Layer has been changed,
                # now we have to edit the STJ Entry
                for ji_id in ji_ids:
                    amount = (
                        move.stock_valuation_layer_ids.unit_cost
                        # svl.unit_cost
                        * move.stock_valuation_layer_ids.stock_move_id.product_uom_qty
                    )
                    if ji_id.credit != 0:
                        ji_id.with_context(check_move_validity=False).write(
                            {"credit": amount}
                        )
                    else:
                        ji_id.with_context(check_move_validity=False).write(
                            {"debit": amount}
                        )
                ji_ids[0].move_id.action_post()

    def get_svl_ids(self, move):
        svl_ids = []
        # We need to get all of the valuation layers associated with this product
        test_vals = self.env["stock.valuation.layer"].search(
            [
                ("product_id", "=", move.product_id.id),
                ("stock_valuation_layer_id", "=", False),
            ],
            order="id desc",
        )
        for line_id in move.move_line_ids:
            for valuation in test_vals:
                # Filter so we only have the Layers we got from Incoming Moves
                if line_id.lot_id in valuation.lot_ids and valuation.value > 0:
                    if not self.check_found_vals(valuation.id, svl_ids):
                        svl_ids.append(
                            (
                                valuation.id,
                                1,
                                [line_id.lot_id.id],
                                line_id,
                            )
                        )
                        break
                    else:
                        self.increment_qty(valuation.id, svl_ids, line_id.lot_id.id)
        if len(svl_ids) == 0 and self.location_id.create_je is True:
            raise UserError(
                _("Need Check Stock Valution Layer For this Product :- %s")
                % (move.product_id.name)
            )
        self.get_ji_ids(move, svl_ids)

    def _action_done(self, cancel_backorder=False):
        res = super()._action_done(cancel_backorder)
        for move in self:
            # Only run code on outgoing moves with serial or lot products
            if (
                move.product_id.tracking in ["serial", "lot"]
                and move.picking_id.picking_type_id.code == "outgoing"
            ):
                self.get_svl_ids(move)
        return res

    def increment_qty(self, value_id, svl_ids, lot_id):
        index = 0
        for svl_id in svl_ids:
            if svl_id[0] == value_id:
                if lot_id not in svl_id[2]:
                    svl_id[2].append(lot_id)
                svl_ids[index] = (svl_id[0], svl_id[1] + 1, svl_id[2])
            index += 1

    def check_found_vals(self, value_id, svl_ids):
        for svl_id in svl_ids:
            if value_id == svl_id[0]:
                return True
        return False

    # Tag Incoming Valuation Layers with their lot_ids
    def _create_in_svl(self, forced_quantity=None):
        res = super()._create_in_svl(forced_quantity)
        for move in self:
            for layer in res:
                if layer.stock_move_id.id == move.id:
                    layer.lot_ids = [(6, 0, move.lot_ids.ids)]
        return res
