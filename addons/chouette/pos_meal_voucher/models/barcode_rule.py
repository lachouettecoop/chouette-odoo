# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import sets

from openerp import fields, models, api, _

class BarcodeRule(models.Model):
    _inherit = "barcode.rule"

    @api.model
    def _get_type_selection(self):
        types = sets.Set(super(BarcodeRule,self)._get_type_selection())
        types.update([
            ('meal_voucher_payment', _('Meal Voucher Payment'))
        ])
        return list(types)

