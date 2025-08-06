# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
{
    'name': 'POS Customize (Enterprise)',
    'category': 'Point of Sale',
    'summary': 'POS Customize',
    'description': """
        This module Pos Customize.
    """,
    'author': 'Kyan Systems',
    'website': 'http://www.kyansys.sa',
    'price': 00.00,
    'currency': 'EUR',
    'version': '16.0.0',
    'depends': ['base', 'point_of_sale', 'pos_hr', 'hr', 'l10n_gcc_pos'],
    'images': [],
    "data": ['security/ir.model.access.csv',
             'views/sale_order_view.xml',
             'wizard/update_payment_wizard.xml'],
    'installable': True,
    'auto_install': False,
    'assets': {
        'point_of_sale._assets_pos': [ ],
    },
    'license': 'LGPL-3',
    'sequence': 1,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
