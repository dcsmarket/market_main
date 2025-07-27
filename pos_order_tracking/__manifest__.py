{
    'name': 'POS Order Tracking',
    'version': '16.0',
    'category': 'Point of Sale',
    'summary': 'Track specific product orders from POS',
    'description': """
        This module tracks POS orders for specific products and stores their details.
    """,
    'depends': ['point_of_sale'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/pos_order_tracking_views.xml',
        'data/crone.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}