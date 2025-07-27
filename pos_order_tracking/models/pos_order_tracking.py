# from odoo import models, fields, api
#
#
# class POSOrderTracking(models.Model):
#     _name = 'pos.order.tracking'
#     _description = 'POS Order Tracking'
#     _rec_name = 'order_ref'
#
#     order_ref = fields.Char(string='Order Reference')
#     session_id = fields.Many2one('pos.session', string='Session')
#     date = fields.Datetime(string='Date')
#     receipt_number = fields.Char(string='Receipt Number')
#     customer_id = fields.Many2one('res.partner', string='Customer')
#     quantity = fields.Float(string='Quantity')
#     amount = fields.Float(string='Amount')
#     price = fields.Float(string='Price')
#
#
# class PosOrder(models.Model):
#     _inherit = 'pos.order'
#
#     @api.model
#     def create(self, values):
#         # Create the original POS order
#         order = super(PosOrder, self).create(values)
#
#         # Check for the specific product in order lines
#         for line in order.lines:
#             if line.product_id.id == 102944:  # Replace 3 with your specific product ID
#                 # Create tracking record
#                 print(order.name)
#                 self.env['pos.order.tracking'].create({
#                     'order_ref': order.name,
#                     'session_id': order.session_id.id,
#                     'date': order.date_order,
#                     'receipt_number': order.pos_reference,
#                     'customer_id': order.partner_id.id,
#                     'quantity': line.qty,
#                     'amount': line.price_subtotal,
#                     'price': line.price_unit,
#                 })
#         return order
from itertools import product

from odoo import models, fields, api


class POSOrderTracking(models.Model):
    _name = 'pos.order.tracking'
    _description = 'POS Order Tracking'
    _rec_name = 'order_ref'

    order_ref = fields.Char(string='Order Reference')
    session_id = fields.Many2one('pos.session', string='Session')
    date = fields.Datetime(string='Date')
    receipt_number = fields.Char(string='Receipt Number')
    customer_id = fields.Many2one('res.partner', string='Customer')
    quantity = fields.Float(string='Quantity')
    amount = fields.Float(string='Amount')
    price = fields.Float(string='Price')

    # def sync_pos_orders(self):
    #     # tracked_receipts = self.search([]).mapped('receipt_number')
    #     product = self.env['product.product'].browse(100765)
    #     print(product.name)
    #     order = self.env['pos.order'].browse(86481)
    #     for line in order.lines:
    #         print(line.product_id.id, line.product_id.name)
    #     target_lines = self.env['pos.order.line'].search([('product_id', '=', product.id)])
    #     print(target_lines)
    #
    #     for line in target_lines:
    #         order = line.order_id
    #         self.create({
    #             'order_ref': order.name,
    #             'session_id': order.session_id.id,
    #             'date': order.date_order,
    #             'receipt_number': order.pos_reference,
    #             'customer_id': order.partner_id.id if order.partner_id else False,
    #             'quantity': line.qty,
    #             'amount': line.price_subtotal,
    #             'price': line.price_unit,
    #         })

    def sync_pos_orders(self):
        """Sync POS orders for specific product"""
        PosOrder = self.env['pos.order']
        tracked_orders = self.search([]).mapped('receipt_number')
        # product = self.env['product.product'].browse(100765)
        domain = [('lines.product_id.id', '=', 100765), ('pos_reference', 'not in', tracked_orders)]
        pos_orders = PosOrder.search(domain)

        for order in pos_orders:
            for line in order.lines:
                if line.product_id.id == 100765:
                    print(line.product_id.id, 'lp')
                    self.create({
                        'order_ref': order.name,  # Now the order name will be available
                        'session_id': order.session_id.id,
                        'date': order.date_order,
                        'receipt_number': order.pos_reference,
                        'customer_id': order.partner_id.id if order.partner_id else False,
                        'quantity': line.qty,
                        'amount': line.price_subtotal,
                        'price': line.price_unit,
                    })