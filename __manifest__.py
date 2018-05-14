# -*- coding: utf-8 -*-
{
    'name': "fit_import_knab_mt940_bank_statement",

    'summary': """Import KNAB (NL) MT940 Bank Statements.""",

    'description': """
         Add functionality to the default MT940 parser to handle KNAB (NL) MT940 export bank statement files.
    """,

    'author': "Fundament IT",
    'website': "https://www.fundament.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting &amp; Finance',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account_bank_statement_import_mt940_base',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/v_account_bank_statement_import_mt940_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}