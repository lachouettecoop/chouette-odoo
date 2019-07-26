# -*- coding: utf-8 -*-

{
    'name': 'Automatic Import Bank Statement',
    'category': 'Banking addons',
    'version': '9.0.1.0.0',
    'license': 'GPL-3',
    'author': 'Remi CAZENAVE - Le Filament',
    'website': 'https://le-filament.com',
    'depends': [
        'account_bank_statement_import_ofx',
    ],
    'data': [
        'views/view_account_bank_statement_import.xml',
        'views/view_account_bank_statement.xml',
        'views/view_account_journal_dashboard.xml',
    ],
    'installable': True,
}
