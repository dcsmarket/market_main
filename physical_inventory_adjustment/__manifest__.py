# -*- coding: utf-8 -*-
{
    'name': "Inventory Adjustment",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Kyansys",
    'website': "https://www.kyansys.sa",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/physical_inventory_adjustment_view.xml',
        'report/physical_adjustment_report.xml',
        'data/sequence.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'physical_inventory_adjustment/static/src/js/adjustment_autofocus.js',
        ],
    },

}
