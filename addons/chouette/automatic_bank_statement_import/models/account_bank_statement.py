# -*- coding: utf-8 -*-

# © 2017 Le Filament (<http://www.le-filament.com>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from openerp import models, fields


class AccountBankStatement(models.Model):
    _name = 'account.bank.statement'
    _inherit = ['account.bank.statement']

    # Add a boolean field specifying whether the bank statement
    # has been treated or not
    active = fields.Boolean(required=True, default=True, string="A Traiter")
