# -*- coding: utf-8 -*-
{
    'name': "Automate Schedule Actions",
    'version': '17.0.0.0',
    'category': 'Point of Sale',
    'summary': "",
    'description': """ 


    """,
    "author": "Kyan",
    "website": "http://kayanit.com/",
    'depends': ['base', 'point_of_sale', 'account_edi', 'account'],
    'data': [
        # 'views/inventory.xml',
        # 'views/pos_dashboard_views.xml',
        'data/ir_cron_data.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'automate_pos_order/static/src/xml/balance_control.xml',
            'automate_pos_order/static/src/xml/sale_details_button.xml',
            'automate_pos_order/static/src/js/close_pos_popup.js',
            'automate_pos_order/static/src/js/cash_opening_popup.js',

        ],
    },
    'license': 'OPL-1',
    "auto_install": False,
    "installable": True,
}
