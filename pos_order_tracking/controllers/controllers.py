# -*- coding: utf-8 -*-
# from odoo import http


# class PosOrderTracking(http.Controller):
#     @http.route('/pos_order_tracking/pos_order_tracking', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_order_tracking/pos_order_tracking/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_order_tracking.listing', {
#             'root': '/pos_order_tracking/pos_order_tracking',
#             'objects': http.request.env['pos_order_tracking.pos_order_tracking'].search([]),
#         })

#     @http.route('/pos_order_tracking/pos_order_tracking/objects/<model("pos_order_tracking.pos_order_tracking"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_order_tracking.object', {
#             'object': obj
#         })
