# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _payment_fields(self, cr, uid, ui_paymentline, context=None):
        res = super(PosOrder, self)._payment_fields(cr, uid, ui_paymentline)
        res["statement_note"] = ui_paymentline.get("statement_note", False)
        return res

