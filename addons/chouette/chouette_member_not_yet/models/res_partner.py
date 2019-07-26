# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# Some code from https://www.odoo.com/apps/modules/8.0/birth_date_age/
# Copyright (C) Sythil

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pytz
from openerp.exceptions import ValidationError
from openerp import models, fields, api, _



class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    @api.depends(
        'partner_owned_share_ids',
        'partner_owned_share_ids.category_id',
        'partner_owned_share_ids.category_id.is_worker_capital_category',
        'partner_owned_share_ids.owned_share')
    def _compute_is_worker_member(self):
        '''
        @Function to compute data for the field is_worker_member:
            - True if a member has shares in Worker Capital Category
        '''
        partner_owned_share_env = self.env['res.partner.owned.share']
        for partner in self:
            worker_shares = partner_owned_share_env.sudo().search_count(
                [('partner_id', '=', partner.id),
                 ('category_id.is_worker_capital_category', '=', True),
                 ('owned_share', '>', 0)])
            partner.is_worker_member = worker_shares and True or partner.customer

    @api.depends('cooperative_state')
    @api.multi
    def _compute_customer(self):
        for partner in self:
            partner.customer =\
                partner.cooperative_state in self.COOPERATIVE_STATE_CUSTOMER or (partner.active and partner.barcode)

