# -*- coding: utf-8 -*-
# © Odoo SA (code reused from account_bank_statement_import)
# (originally licensed as LGPL)
# © 2017 Le Filament (<http://www.le-filament.com>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from openerp import api, models, _
from openerp.exceptions import UserError


class AccountBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'

    @api.model
    def auto_import_file(self, file_to_import):
        # Let the appropriate implementation module parse the file
        # and return the required data
        currency_code, account_number, stmts_vals = self._parse_file(
            open(file_to_import, 'r').read())
        # Check raw data
        super(AccountBankStatementImport, self)._check_parsed_data(stmts_vals)
        # Try to find the currency and journal in odoo
        currency, journal = super(
            AccountBankStatementImport,
            self)._find_additional_data(currency_code, account_number)
        # If no journal found, ask the user about creating one
        if not journal:
            # The active_id is passed in context so the wizard can call
            # import_file again once the journal is created
            return super(
                AccountBankStatementImport,
                self)._journal_creation_wizard(currency, account_number)
        if (not journal.default_debit_account_id
                or not journal.default_credit_account_id):
            raise UserError(_('You have to set a Default Debit Account and a \
                Default Credit Account for the journal: %s') % (journal.name,))
        # Prepare statement data to be used for bank statements creation
        stmts_vals = super(
            AccountBankStatementImport,
            self)._complete_stmts_vals(stmts_vals, journal, account_number)
        # Create the bank statements
        statement_ids, notifications = super(AccountBankStatementImport, self)\
            ._create_bank_statements(stmts_vals)
        statements = self.env['account.bank.statement'].browse(statement_ids)
        # Update Bank Statements balances
        for statement in statements:
            total_amt = statement['balance_end'] - statement['balance_start']
            statement['balance_end_real'] = statement['balance_start']
            statement['balance_start'] = statement['balance_end_real'] - \
                total_amt
        # Now that the import worked out, set it as the bank_statements_source
        # of the journal
        journal.bank_statements_source = 'file_import'
