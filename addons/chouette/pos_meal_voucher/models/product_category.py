# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api


class ProductCategory(models.Model):
    _inherit = 'product.category'

    meal_voucher_ok = fields.Boolean(
        string="Meal Voucher",
        help="If checked, the products that belong to the category"
        " will be marked as 'can be paid with meal vouchers', by default."
    )

    @api.multi
    def button_apply_meal_voucher_settings(self):
        ProductTemplate = self.env["product.template"]
        for category in self:
            templates = ProductTemplate.with_context(
                active_test=False).search([('categ_id', '=', category.id)])
            templates.write({"meal_voucher_ok": category.meal_voucher_ok})
            category.child_id.write({"meal_voucher_ok": category.meal_voucher_ok})
            category.child_id.button_apply_meal_voucher_settings()

