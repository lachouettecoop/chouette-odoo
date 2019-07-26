# -*- coding: utf-8 -*-

# © 2017 Le Filament (<http://www.le-filament.com>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import json
from openerp import models, api
from openerp.tools.misc import formatLang


class account_journal(models.Model):
    _inherit = "account.journal"

    @api.one
    def _kanban_dashboard(self):
        datas = self.get_journal_dashboard_datas()
        datas.update(self.get_extra_journal_dashboard_datas())
        self.kanban_dashboard = json.dumps(datas)

    @api.multi
    def get_extra_journal_dashboard_datas(self):
        empty = 0
        bank_balance = 0.0
        last_statement_date = "0000-00-00"
        last_statement_amount = 0
        currency = self.currency_id or self.company_id.currency_id

        if self.type in ['cash', 'bank']:
            self.env.cr.execute(
                "SELECT sum(amount) FROM account_bank_statement_line \
                WHERE journal_id IN %s", (tuple(self.ids),))
            bank_balance_dict = self.env.cr.fetchone()
            # if bank_balance_dict[0] is not None:
            bank_balance = bank_balance_dict[0] if bank_balance_dict else 0.0

            self.env.cr.execute(
                "SELECT date, balance_end FROM account_bank_statement \
                WHERE journal_id in %s ORDER BY DATE DESC, ID DESC LIMIT 1",
                (tuple(self.ids),))
            query_result = self.env.cr.fetchone()
            # if query_result is not None
            last_statement_date = query_result[0] if query_result else "NA"
            last_statement_amount = query_result[1] if query_result else 0

        return {
            'empty': empty,
            'bank_balance': formatLang(
                self.env,
                bank_balance if bank_balance else 0.0,
                currency_obj=currency),
            'last_statement_date': last_statement_date,
            'last_statement_amount': formatLang(
                self.env,
                last_statement_amount,
                currency_obj=currency),
        }
